// Browser-level QA for hannieverse.com. Usage: see qa/README.md
const { chromium } = require('playwright');
const fs = require('fs');

const BASE = 'https://www.hannieverse.com';
const PAGES = ['/', '/our-philosophy', '/honour', '/hfs-arc', '/about-us', '/technical-writing',
  '/connections', '/book-online', '/booking-calendar/discovery-call',
  '/booking-calendar/honour-facilitator-package', '/booking-calendar/honour',
  '/booking-policy', '/privacy-policy', '/terms-conditions', '/refund-policy',
  '/payment-policy', '/disclaimer', '/copyright-policy', '/accessibility-statement'];
const VIEWPORTS = [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }];
const SUBMIT_FORMS = process.argv.includes('--submit-forms'); // sends real test messages
const OUT = 'qa-output';
const slug = p => (p === '/' ? 'home' : p.replace(/^\//, '').replace(/\//g, '_'));

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const report = [];

  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: vp.name === 'mobile' });
    for (const path of PAGES) {
      const page = await ctx.newPage();
      const consoleErrors = [], failedRequests = [];
      page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 200)); });
      page.on('pageerror', e => consoleErrors.push('PAGEERROR ' + e.message.slice(0, 200)));
      page.on('requestfailed', r => failedRequests.push(r.url().slice(0, 120)));
      const entry = { viewport: vp.name, path };
      try {
        const res = await page.goto(BASE + path, { waitUntil: 'networkidle', timeout: 45000 });
        entry.status = res.status();
        await page.waitForTimeout(1500);
        Object.assign(entry, await page.evaluate(() => {
          const imgs = [...document.images];
          const stretched = imgs.filter(i => i.naturalWidth && i.clientWidth && i.clientHeight &&
            Math.abs(i.naturalWidth / i.naturalHeight - i.clientWidth / i.clientHeight) > 0.15 &&
            getComputedStyle(i).objectFit === 'fill').map(i => i.src.slice(-60));
          const wide = [...document.querySelectorAll('body *')].filter(e => {
            const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 && r.width > 0;
          }).slice(0, 5).map(e => e.tagName + '.' + String(e.className).slice(0, 40));
          return {
            horizontalOverflowPx: document.documentElement.scrollWidth - innerWidth,
            overflowingElements: wide,
            brokenImages: imgs.filter(i => i.complete && !i.naturalWidth).map(i => i.src.slice(-80)),
            stretchedImages: stretched,
            imagesWithoutAlt: imgs.filter(i => !i.alt).length,
            placeholderText: (document.body.innerText.match(/lorem|ipsum|placeholder|TODO|TBD/gi) || []),
          };
        }));
        // check every same-site link and outbound link status
        const links = await page.$$eval('a[href^="http"]', as => [...new Set(as.map(a => a.href))]);
        entry.badLinks = [];
        for (const l of links.filter(l => !/parastorage|wix\.com|wixstatic/.test(l))) {
          try {
            const r = await page.request.get(l, { timeout: 20000 });
            if (r.status() >= 400) entry.badLinks.push(`${r.status()} ${l.slice(0, 110)}`);
          } catch (e) { entry.badLinks.push(`ERR ${l.slice(0, 110)}`); }
        }
      } catch (e) { entry.error = e.message.slice(0, 150); }
      entry.consoleErrors = [...new Set(consoleErrors)];
      entry.failedRequests = [...new Set(failedRequests)].slice(0, 8);
      await page.screenshot({ path: `${OUT}/${vp.name}_${slug(path)}.png`, fullPage: true }).catch(() => {});
      report.push(entry);
      await page.close();
    }
    await ctx.close();
  }

  if (SUBMIT_FORMS) {
    for (const path of ['/', '/technical-writing']) {
      const ctx = await browser.newContext(); const page = await ctx.newPage();
      await page.goto(BASE + path, { waitUntil: 'networkidle' });
      const entry = { form: path };
      try {
        await page.getByLabel(/first name/i).first().fill('QA');
        await page.getByLabel(/last name/i).first().fill('Test');
        await page.getByLabel(/company name/i).first().fill('QA Test - please ignore');
        await page.getByLabel(/email/i).first().fill('qa-test@example.com');
        await page.getByLabel(/message/i).first().fill('Automated QA test, please ignore.');
        await page.getByRole('button', { name: /submit/i }).first().click();
        await page.waitForTimeout(4000);
        entry.result = (await page.locator('body').innerText()).match(/thank|success|sent|received|error|failed/i)?.[0] || 'NO CONFIRMATION SEEN';
        await page.screenshot({ path: `${OUT}/form_${slug(path)}.png` });
      } catch (e) { entry.error = e.message.slice(0, 150); }
      report.push(entry); await ctx.close();
    }
  }

  fs.writeFileSync(`${OUT}/report.json`, JSON.stringify(report, null, 2));
  for (const r of report) {
    const flags = [];
    if (r.error) flags.push('LOAD ERROR: ' + r.error);
    if (r.status >= 400) flags.push('HTTP ' + r.status);
    if (r.horizontalOverflowPx > 0) flags.push(`overflow ${r.horizontalOverflowPx}px (${(r.overflowingElements || []).join(', ')})`);
    if (r.brokenImages?.length) flags.push('broken images: ' + r.brokenImages.join(', '));
    if (r.stretchedImages?.length) flags.push('stretched: ' + r.stretchedImages.join(', '));
    if (r.placeholderText?.length) flags.push('placeholder text: ' + r.placeholderText.join(', '));
    if (r.badLinks?.length) flags.push('bad links: ' + r.badLinks.join(' | '));
    if (r.consoleErrors?.length) flags.push('console: ' + r.consoleErrors.join(' | '));
    if (r.form) flags.push(`FORM ${r.form}: ${r.result || r.error}`);
    console.log(`${r.viewport || 'form'} ${r.path || ''} ${flags.length ? '\n   - ' + flags.join('\n   - ') : 'OK'}`);
  }
  await browser.close();
})();
