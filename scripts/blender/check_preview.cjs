const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const base=process.env.BASE_URL||'http://127.0.0.1:4193/';
(async()=>{
 const browser=await chromium.launch({channel:'chromium',executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
  await page.goto(new URL('viewer-blender/',base).href);
  await page.waitForFunction(()=>window.blenderStudy,null,{timeout:120000});
  for(const view of ['arrival','garden','living','kitchen','parents','office','ground','first']){
   await page.selectOption('#view',view);
   const visible=await page.evaluate(()=>Object.fromEntries(['g','a','u','o','Roofs','Ceilings'].map(n=>[n,blenderStudy.model.getObjectByName(n).visible])));
   assert.deepEqual(visible,view==='ground'?{g:true,a:true,u:false,o:false,Roofs:false,Ceilings:false}:view==='first'?{g:false,a:false,u:true,o:true,Roofs:false,Ceilings:false}:{g:true,a:true,u:true,o:true,Roofs:true,Ceilings:true});
  }
  for(const width of [390,320]){
   await page.setViewportSize({width,height:844});
   await page.waitForFunction(()=>document.querySelector('canvas').getBoundingClientRect().width===innerWidth);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  }
  await page.selectOption('#view','arrival');
  await page.waitForTimeout(1000);
  const frame=await page.evaluate(()=>blenderStudy.renderer.info.render.frame);
  await page.waitForTimeout(300);
  assert.equal(await page.evaluate(()=>blenderStudy.renderer.info.render.frame),frame,'Idle preview must stop rendering');
  assert.deepEqual(errors,[]);
  console.log('Blender GLB loaded; eight views, floor cutaways, phone widths and idle rendering passed.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
