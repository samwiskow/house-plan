const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const base=process.env.BASE_URL||'http://127.0.0.1:4190/';
const root=path.resolve(__dirname,'..'),out=path.join(root,'tmp/performance',process.argv[2]||'current');
(async()=>{fs.mkdirSync(out,{recursive:true});const chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||(fs.existsSync(chrome)?chrome:undefined),args:['--enable-gpu']});
 try{const page=await browser.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1}),samples=[];
 for(const [route,views] of [['viewer',['overview','living']],['viewer-l-house',['overview','ground','living']]]){
  await page.goto(new URL(route+'/',base).href);await page.waitForFunction(()=>window.house);
  for(const view of views){await page.evaluate(view=>house.capture(view),view);await page.waitForTimeout(500);
   const metrics=await page.evaluate(async()=>{const {renderer,scene,camera}=house,gl=renderer.getContext();renderer.render(scene,camera);gl.finish();const times=[];
    for(let i=0;i<8;i++){await new Promise(requestAnimationFrame);const start=performance.now();renderer.render(scene,camera);gl.finish();times.push(performance.now()-start);}times.sort((a,b)=>a-b);
    const ext=gl.getExtension('WEBGL_debug_renderer_info');return {backend:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),medianMs:times[4],drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,geometries:renderer.info.memory.geometries,textures:renderer.info.memory.textures};});
   samples.push({route,view,...metrics});await page.screenshot({path:path.join(out,route+'-'+view+'.png')});
  }
 }
 fs.writeFileSync(path.join(out,'measurements.json'),JSON.stringify({viewport:[1200,800],deviceScaleFactor:1,samples},null,2)+'\n');console.log(JSON.stringify(samples));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
