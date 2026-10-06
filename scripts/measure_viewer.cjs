const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const baseURL=process.env.BASE_URL||'http://127.0.0.1:4186/';
const label=process.argv[2]||'current';
const output=path.join(root,'tmp/fidelity',label);
const localChrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
 fs.mkdirSync(output,{recursive:true});
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||(fs.existsSync(localChrome)?localChrome:undefined),headless:true,args:['--enable-gpu']});
 try {
  const page=await browser.newPage({deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',route=>route.request().url().startsWith(baseURL)?route.continue():route.abort());
  const report={deviceScaleFactor:1,samples:[]};
  for(const [device,viewport] of [['desktop',{width:1400,height:1000}],['mobile',{width:390,height:844}]]){
   await page.setViewportSize(viewport);
   await page.goto(new URL('viewer/',baseURL).href);await page.waitForFunction(()=>window.house);
   for(const [view,evening] of [['living',false],['dining',false],['dining',true],['courtyard',false]]){
    await page.evaluate(([view,evening])=>house.capture(view,evening),[view,evening]);
    await page.waitForTimeout(600);
    const metrics=await page.evaluate(async()=>{
     const {renderer,scene,camera}=house,gl=renderer.getContext();
     renderer.render(scene,camera);gl.finish();
     const durations=[];
     for(let i=0;i<12;i++){
      await new Promise(requestAnimationFrame);
      const start=performance.now();renderer.render(scene,camera);gl.finish();durations.push(performance.now()-start);
     }
     durations.sort((a,b)=>a-b);
     const debug=gl.getExtension('WEBGL_debug_renderer_info');
     return {backend:debug?gl.getParameter(debug.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),medianMs:Math.round(durations[6]*10)/10,p95Ms:Math.round(durations[11]*10)/10,drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,geometries:renderer.info.memory.geometries,textures:renderer.info.memory.textures,glError:gl.getError(),contextLost:gl.isContextLost()};
    });
    report.samples.push({device,viewport,view,evening,...metrics});
    await page.screenshot({path:path.join(output,`${device}-${view}${evening?'-evening':''}.png`)});
   }
  }
  if(errors.length||report.samples.some(s=>s.glError||s.contextLost))throw Error(JSON.stringify({errors,samples:report.samples}));
  fs.writeFileSync(path.join(output,'measurements.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));
 } finally {await browser.close();}
})();
