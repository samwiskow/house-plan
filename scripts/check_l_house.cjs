const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const base=process.env.BASE_URL||'http://127.0.0.1:4190/';
const root=path.resolve(__dirname,'..'),output=path.join(root,'tmp/l-house');
(async()=>{fs.mkdirSync(output,{recursive:true});const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||(fs.existsSync('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':undefined),headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});try{
 const page=await browser.newPage({viewport:process.env.CI?{width:900,height:640}:{width:1440,height:1000}});page.setDefaultTimeout(60000);const errors=[],external=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url()+' '+r.status())});
 await page.route('**/*',route=>{if(route.request().url().startsWith(base))return route.continue();external.push(route.request().url());return route.abort();});
 await page.goto(base+'viewer-l-house/');await page.waitForFunction(()=>window.house);await page.waitForTimeout(700);
 const source=JSON.parse(fs.readFileSync(path.join(root,'studies/l-house-booklet/plans.json')));
 const exported=await page.evaluate(()=>house.model);
 for(const k of ['default','enclosed']){assert.deepEqual(exported[k].rooms,source[k].rooms);assert.deepEqual(exported[k].furniture,source[k].furniture);for(const d of source[k].doors)assert.deepEqual(exported[k].doors.find(n=>n.id===d.id),d);}
 for(const view of Object.keys(await page.evaluate(()=>house.views))){await page.locator('#view').selectOption(view);await page.waitForTimeout(220);await page.screenshot({path:path.join(output,view+'.png')});}
 await page.locator('#view').selectOption('first');assert(await page.evaluate(()=>{const g=house.scene.getObjectByName('Stairs');for(let p=g;p;p=p.parent)if(!p.visible)return false;return g.children.length>0;}),'First floor hides stairs');
 for(const view of ['ground','first']){await page.locator('#view').selectOption(view);await page.waitForFunction(()=>!house.renderer.shadowMap.needsUpdate);assert(await page.evaluate(()=>{house.setWalking(true);return house.renderer.shadowMap.needsUpdate;}),'Walking from a cutaway must refresh roof shadows');await page.waitForFunction(()=>!house.renderer.shadowMap.needsUpdate);await page.keyboard.press('Escape');}
 await page.locator('#view').selectOption('ground');assert.equal(await page.evaluate(()=>house.state.floorMode),'ground');assert.equal(await page.evaluate(()=>house.state.roofOn),false);
 await page.locator('#pantry').selectOption('default');assert(await page.evaluate(()=>house.canMove(12.625,6.95,0)),'Default pantry passage blocked');
 await page.locator('#pantry').selectOption('enclosed');assert(!(await page.evaluate(()=>house.canMove(12.625,6.95,0))),'Enclosed pantry wall missing');
 await page.screenshot({path:path.join(output,'enclosed-pantry.png')});
 await page.locator('#pantry').selectOption('default');
 await page.evaluate(()=>{const d=house.doors.find(s=>s.data.id==='Kitchen to pantry');d.open=false;house.requestRender();});
 await page.waitForFunction(()=>house.doors.find(s=>s.data.id==='Kitchen to pantry').progress===0);assert(!(await page.evaluate(()=>house.canMove(10.825,6.75,0))));
 await page.evaluate(()=>house.toggleDoor(house.doors.find(s=>s.data.id==='Kitchen to pantry')));await page.waitForFunction(()=>house.doors.find(s=>s.data.id==='Kitchen to pantry').progress===1);assert(await page.evaluate(()=>house.canMove(10.825,6.75,0)));
 await page.locator('#view').selectOption('kitchen');await page.locator('#walk').click();
 await page.evaluate(()=>{house.setPose(9.4,6.75);house.camera.lookAt(10.825,1.5,6.75);house.requestRender();});
 await page.waitForFunction(()=>house.doorAt()?.data.id==='Kitchen to pantry');
 await page.locator('canvas').focus();await page.keyboard.press('Space');
 await page.waitForFunction(()=>house.doors.find(s=>s.data.id==='Kitchen to pantry').progress===0);
 await page.locator('#door').click();assert(await page.evaluate(()=>house.doors.find(s=>s.data.id==='Kitchen to pantry').open),'Door button must open the aimed pantry door');await page.waitForFunction(()=>house.doors.find(s=>s.data.id==='Kitchen to pantry').progress===1);
 await page.locator('#mouse-look').click();await page.waitForFunction(()=>document.pointerLockElement===house.renderer.domElement);
 assert(await page.evaluate(()=>document.activeElement===house.renderer.domElement),'Mouse look must keep keyboard input on the model');
 const lockedFrom=await page.evaluate(()=>house.camera.position.toArray());await page.keyboard.down('s');await page.waitForFunction(before=>Math.hypot(house.camera.position.x-before[0],house.camera.position.z-before[2])>.12,lockedFrom);await page.keyboard.up('s');
 await page.evaluate(()=>{house.setPose(9.4,6.75);house.camera.lookAt(10.825,1.5,6.75);house.requestRender();});await page.waitForFunction(()=>house.doorAt()?.data.id==='Kitchen to pantry');
 await page.evaluate(()=>{window.lockedClickEvents=[];for(const type of ['pointerdown','pointerup','click'])document.addEventListener(type,e=>lockedClickEvents.push({type,target:e.target.id||e.target.tagName}),{once:true,capture:true});});
 await page.mouse.down();await page.mouse.up();const lockedClick=await page.evaluate(()=>({open:house.doors.find(s=>s.data.id==='Kitchen to pantry').open,aim:house.doorAt()?.data.id,locked:document.pointerLockElement?.tagName,events:lockedClickEvents}));assert(!lockedClick.open,'Locked click must close the aimed pantry door: '+JSON.stringify(lockedClick));await page.waitForFunction(()=>house.doors.find(s=>s.data.id==='Kitchen to pantry').progress===0);
 await page.keyboard.press('Space');await page.waitForFunction(()=>house.doors.find(s=>s.data.id==='Kitchen to pantry').progress===1);
 await page.keyboard.press('Escape');await page.waitForFunction(()=>!house.state.walking&&document.pointerLockElement===null);
 const stairs=await page.evaluate(()=>{
  const out=[];
  for(const stair of house.model.stairs){const{x,z}=stair;const points=[[x+.5,z-.3],[x+.5,z+.2],[x+.5,z+1.7],[x+.5,z+2.35],[x+1.9,z+2.35],[x+1.9,z+1.6],[x+1.9,z+.1],[x+1.9,z-.35]];house.setPose(...points[0],0);
   const follow=targets=>{for(const [a,b]of targets){for(let i=0;i<800&&Math.hypot(a-house.camera.position.x,b-house.camera.position.z)>.025;i++){const dx=a-house.camera.position.x,dz=b-house.camera.position.z,len=Math.hypot(dx,dz);house.move(dx/len*Math.min(.035,len),dz/len*Math.min(.035,len));}if(Math.hypot(a-house.camera.position.x,b-house.camera.position.z)>.06)return {target:[a,b],actual:house.camera.position.toArray(),feet:house.state.feet};}return null;};
   const up=follow(points.slice(1)),height=house.state.feet,down=up?null:follow(points.slice(0,-1).reverse());out.push({id:stair.id,up,height,down,final:house.state.feet});
  }return out;
 });
 fs.writeFileSync(path.join(output,'stairs.json'),JSON.stringify(stairs,null,2));
 for(const s of stairs){assert.equal(s.up,null,JSON.stringify(s));assert.equal(s.height,3,JSON.stringify(s));assert.equal(s.down,null,JSON.stringify(s));assert.equal(s.final,0,JSON.stringify(s));}
 await page.locator('#view').selectOption('office');await page.locator('#office').selectOption('guest');assert.equal(await page.evaluate(()=>house.state.officeState),'guest');assert(await page.evaluate(()=>house.fixtures.some(f=>f.name==='Office sofa bed'&&f.rect[2]===2.2)));await page.screenshot({path:path.join(output,'office-guest.png')});
 await page.locator('#light').click();assert(await page.evaluate(()=>house.state.night));await page.screenshot({path:path.join(output,'evening.png')});await page.locator('#light').click();
 await page.locator('#view').selectOption('living');await page.locator('#walk').click();assert(await page.evaluate(()=>house.state.walking));
 const before=await page.evaluate(()=>house.camera.position.toArray());await page.keyboard.down('s');await page.waitForFunction(before=>Math.hypot(house.camera.position.x-before[0],house.camera.position.z-before[2])>.12,before);await page.keyboard.up('s');
 const dir=await page.evaluate(()=>house.camera.getWorldDirection(house.camera.position.clone()).toArray());await page.keyboard.down('ArrowLeft');await page.waitForFunction(dir=>house.camera.getWorldDirection(house.camera.position.clone()).distanceTo({x:dir[0],y:dir[1],z:dir[2]})>.15,dir);await page.keyboard.up('ArrowLeft');
 await page.keyboard.press('Escape');assert(!(await page.evaluate(()=>house.state.walking)));
 await page.evaluate(()=>{house.setPose(10.1,10.8,3);});assert(!(await page.evaluate(()=>house.canMove(-1,10.8,3))),'Upper floor allows walking into the air');assert(!(await page.evaluate(()=>house.canMove(.175,4.8,0))),'Solid wall accepts movement');
 const pdf=await page.request.get(base+'output/pdf/l-house-design-booklet.pdf');assert.equal(pdf.status(),200);
 for(const width of [390,320]){await page.setViewportSize({width,height:844});await page.waitForFunction(()=>Math.abs(house.camera.aspect-innerWidth/innerHeight)<.001);await page.locator('#view').selectOption('overview');assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)));await page.screenshot({path:path.join(output,'mobile-'+width+'.png')});}
 assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
 fs.writeFileSync(path.join(output,'browser-checks.json'),JSON.stringify({rooms:33,sourceGeometry:'unchanged',stairs,errors,external,viewports:[process.env.CI?900:1440,390,320],pantryOptions:'pass',doorCollision:'pass',walkControls:'pass',cutawayShadows:'pass',lockedMouseControls:'pass',officeGuest:'pass'},null,2));
 console.log('Passed: plan agreement, views, pantry options, operating doors, cutaway shadows, locked mouse controls, both stairs up/down, walking, upper-floor edge, office guest state, lighting, PDF link, responsive controls, local-only assets.');
 }finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
