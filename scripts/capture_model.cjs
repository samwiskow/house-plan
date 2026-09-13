const path=require('node:path');
const root=path.resolve(__dirname,'..');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:{width:1800,height:1150},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:4186/viewer/');await page.waitForFunction(()=>window.house);
 for(const name of ['overview','courtyard','arrival','living','dining','library','office','garden','plan']){
  await page.evaluate(name=>window.house.capture(name),name);await page.waitForTimeout(600);await page.screenshot({path:path.join(root,`output/design/book-views/${name}.png`)});
 }
 await page.evaluate(()=>window.house.capture('dining',true));await page.waitForTimeout(600);await page.screenshot({path:path.join(root,'output/design/book-views/evening.png')});
 await page.evaluate(()=>window.house.capture('courtyard',true));await page.waitForTimeout(600);await page.screenshot({path:path.join(root,'output/design/book-views/evening-court.png')});
 if(errors.length)throw Error(errors.join('\n'));
 console.log('Captured 11 views without browser errors');await browser.close();
})();
