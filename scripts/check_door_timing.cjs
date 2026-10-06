const assert=require('node:assert/strict'),fs=require('node:fs');
const {chromium}=require('playwright');
(async()=>{const chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||(fs.existsSync(chrome)?chrome:undefined),args:process.env.CI?['--use-angle=swiftshader','--enable-unsafe-swiftshader']:['--enable-gpu']});try{
 const page=await browser.newPage({viewport:{width:400,height:300}});page.setDefaultTimeout(60000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{const raf=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=callback=>raf(()=>setTimeout(()=>{const frameAt=performance.now();callback(frameAt);if(window.doorSamples&&window.house){const door=house.doors.find(s=>s.data.id==='Kitchen to pantry');doorSamples.push({progress:door.progress,elapsed:frameAt-doorStarted});}},250));});
 await page.goto(new URL('viewer-l-house/',process.env.BASE_URL||'http://127.0.0.1:4190/').href);await page.waitForFunction(()=>window.house&&!house.renderer.shadowMap.needsUpdate,undefined,{polling:50});await page.waitForTimeout(1000);
 await page.evaluate(()=>{window.doorSamples=[];window.doorStarted=performance.now();house.toggleDoor(house.doors.find(s=>s.data.id==='Kitchen to pantry'));});
 await page.waitForFunction(()=>doorSamples.length>=4,undefined,{polling:50});const samples=await page.evaluate(()=>doorSamples.slice(0,4));
 assert(samples[0].progress>0,'Door must advance on the first delayed frame');if(samples[0].elapsed<600)assert(samples[0].progress<1,'Opening after idle must animate');assert.equal(samples[3].progress,1,'Door should finish within four 250ms-spaced frames');assert.deepEqual(errors,[]);console.log('Passed: door timing remains correct at low frame rates and after idle.',samples);
 }finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
