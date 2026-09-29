# Site QA script

Runs on your own computer (Mac, Windows or Linux). You need Node.js 18+ (https://nodejs.org).

```bash
cd qa
npm init -y
npm install playwright
npx playwright install chromium
node site-qa.js
```

Takes a few minutes. It prints a per-page summary, and writes screenshots (desktop and phone) plus `report.json` to `qa/qa-output/`.

To also submit the two enquiry forms (this sends real test messages to your inbox):

```bash
node site-qa.js --submit-forms
```

The booking calendars are not automated. Test the Discovery Call and Facilitator Package by hand, through to the confirmation email.

Then paste the console output here (and any screenshots that look wrong).
