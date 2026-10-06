const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const base=process.env.BASE_URL||'http://127.0.0.1:4190/tmp/pages/';
(async()=>{const chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||(fs.existsSync(chrome)?chrome:undefined),args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});try{
 const p=await browser.newPage({viewport:{width:1400,height:1000}});p.setDefaultTimeout(60000);const errors=[],requests=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)errors.push(r.url()+' '+r.status())});p.on('request',r=>requests.push(r.url()));
 const out=path.resolve(__dirname,'../tmp/site-review');fs.mkdirSync(out,{recursive:true});
 await p.goto(base);await p.locator('img').evaluateAll(images=>Promise.all(images.map(i=>i.decode())));assert.equal(await p.title(),'House models');assert(!(await p.evaluate(()=>window.house)));assert(!requests.some(r=>r.includes('three.')||r.includes('model.json')),'Index loads a 3D model');
 for(const a of await p.locator('main a:not([aria-hidden])').all()){const r=await p.request.get(new URL(await a.getAttribute('href'),base).href);assert.equal(r.status(),200);}
 for(const width of [1400,390,320]){await p.setViewportSize({width,height:1000});await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));await p.setViewportSize({width,height:await p.evaluate(()=>Math.max(1000,document.documentElement.scrollHeight))});await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));await p.screenshot({path:path.join(out,'index-'+width+'.png')});assert(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)));assert(await p.locator('img').evaluateAll(images=>images.every(i=>i.complete&&i.naturalWidth>0)));}
 await p.getByRole('link',{name:'Explore the L-house',exact:true}).click();await p.waitForFunction(()=>window.house);assert(p.url().startsWith(base+'viewer-l-house/'));
 for(const [route,label] of [['viewer-l-house','L-house'],['viewer','Courtyard house']]){
  if(route==='viewer'){await p.getByRole('navigation',{name:'House models',exact:true}).getByRole('link',{name:label,exact:true}).click();await p.waitForFunction(()=>window.house);}
  assert.equal(await p.locator('.model-nav [aria-current=page]').textContent(),label);
  for(const width of [1400,390,320]){await p.setViewportSize({width,height:1000});await p.waitForFunction(()=>Math.abs(house.camera.aspect-innerWidth/innerHeight)<.001);await p.screenshot({path:path.join(out,route+'-'+width+'.png')});assert(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)));const links=await p.locator('.model-nav a').evaluateAll(as=>as.map(a=>({r:a.getBoundingClientRect().right,l:a.getBoundingClientRect().left})));assert(links.every(r=>r.l>=0&&r.r<=width));}
 }
 await p.getByRole('link',{name:'All models',exact:true}).click();assert.equal(await p.title(),'House models');assert.deepEqual(errors,[]);console.log('Passed: index, both model pages, cross-navigation, PDF links, local assets and 1400/390/320 layouts.');
 }finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
