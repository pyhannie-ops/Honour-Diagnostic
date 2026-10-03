const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1800,height:1000}});
await p.goto('file://'+process.cwd()+'/before-after.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
await p.screenshot({path:'before-after-1800.png',fullPage:true});
await p.locator('.before').screenshot({path:'before-900.png'});await p.locator('.after').screenshot({path:'after-900.png'});
await b.close();})();
