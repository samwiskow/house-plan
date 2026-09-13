const assert=require('node:assert/strict');
const path=require('node:path');
const fs=require('node:fs');
const baseURL=process.env.BASE_URL||'http://127.0.0.1:4186/';
const localChrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const root=path.resolve(__dirname,'..');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||(fs.existsSync(localChrome)?localChrome:undefined),headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 fs.mkdirSync(path.join(root,'tmp/pdfs'),{recursive:true});
 try { const page=await browser.newPage({viewport:{width:1400,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',route=>route.request().url().startsWith(baseURL)?route.continue():route.abort());
 await page.goto(new URL('viewer/',baseURL).href);await page.waitForFunction(()=>window.house);
 assert.equal(await page.evaluate(()=>house.model.rooms.length),26);
 const physical=await page.evaluate(async()=>{
  const THREE=await import(new URL('viewer/vendor/three.module.js',location.origin+location.pathname.split('viewer/')[0]).href);
  house.scene.updateMatrixWorld(true);
  const ray=new THREE.Raycaster();
  const openings=house.model.rooflights.map(light=>{
   const [x,z,w,d]=light.rect;ray.set(new THREE.Vector3(x+w/2,1,z+d/2),new THREE.Vector3(0,1,0));
   const hits=ray.intersectObjects(house.scene.children,true).filter(h=>h.object.isMesh&&h.point.y>2.5);
   return hits.length>0&&hits.every(h=>h.object.material.transparent);
  });
  const chairBacks=[];
  house.scene.traverse(o=>{
   if(!['Dining north','Dining south'].includes(o.userData.name))return;
   const back=o.children.find(c=>c.isMesh&&c.geometry.parameters.height>.3&&c.position.y>.6);
   const north=o.userData.name==='Dining north';
   chairBacks.push(back&&Math.abs(back.position.z-(north?5.63:7.77))<.01);
  });
  return {openings,chairBacks};
 });
 assert.equal(physical.openings.length,6);assert(physical.openings.every(Boolean),'Rooflight blocked by opaque roof or ceiling');
 assert.equal(physical.chairBacks.length,8);assert(physical.chairBacks.every(Boolean),'Outdoor dining chair faces away from table');
 const book=await page.request.get(new URL('output/pdf/house-design-book.pdf',baseURL).href);assert.equal(book.status(),200);assert.equal((await book.body()).subarray(0,4).toString(),'%PDF');

 await page.getByRole('button',{name:'Plan',exact:true}).click();assert.equal(await page.evaluate(()=>house.state.roofOn),false);
 await page.getByRole('button',{name:'Office',exact:true}).click();
 await page.getByLabel('Office use').selectOption('Night');
 let furniture=await page.evaluate(()=>house.state.officeFurniture);assert(furniture.some(n=>n.toLowerCase().includes('open')));assert(furniture.includes('Professional workspace'));assert(furniture.includes('Personal workspace'));assert(!furniture.includes('Sofa bed closed'));
 await page.getByLabel('Office use').selectOption('Personal');assert((await page.evaluate(()=>house.state.officeFurniture)).includes('Sofa bed closed'));
 await page.getByRole('button',{name:'Daylight',exact:true}).click();assert.equal(await page.evaluate(()=>house.state.night),true);
 await page.getByRole('button',{name:'Evening',exact:true}).click();
 await page.getByRole('button',{name:'Shared room',exact:true}).click();
 await page.getByRole('button',{name:'Walk',exact:true}).click();const before=await page.evaluate(()=>house.camera.position.toArray());
 await page.keyboard.down('w');await page.waitForFunction(before=>house.camera.position.distanceTo({x:before[0],y:before[1],z:before[2]})>.05,before,{timeout:15000});await page.keyboard.up('w');const after=await page.evaluate(()=>house.camera.position.toArray());assert.notDeepEqual(before,after);
 assert.equal(await page.evaluate(()=>house.canMove(.175,5)),false);assert.equal(await page.evaluate(()=>house.canMove(17.8,17.4)),true);
 await page.keyboard.press('Escape');assert.equal(await page.evaluate(()=>house.state.walking),false);
 await page.evaluate(()=>{house.camera.position.set(18.1,1.65,20.5);house.setWalking(true);house.camera.position.set(18.1,1.65,20.5);house.camera.lookAt(18.1,1.1,18.225);});
 await page.evaluate(()=>house.renderer.render(house.scene,house.camera));await page.mouse.click(700,500);
 assert.equal(await page.evaluate(()=>{let open;house.scene.traverse(o=>{if(o.userData.door?.data.id==='D15')open=o.userData.door.open;});return open;}),true);
 await page.getByRole('button',{name:'Whole house',exact:true}).click();
 await page.screenshot({path:path.join(root,'tmp/pdfs/viewer-desktop.png')});
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(root,'tmp/pdfs/viewer-mobile.png')});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);assert.equal(overflow,false);
 assert.deepEqual(errors,[]);console.log('Passed rooflight rays, outdoor chair orientation, PDF download, local-only load, view controls, office states, day/evening, walking, door interaction, wall collision and mobile overflow checks');
 } finally { await browser.close(); }
})();
