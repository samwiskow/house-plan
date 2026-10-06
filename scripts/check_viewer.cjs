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
 try { const page=await browser.newPage({viewport:process.env.CI?{width:900,height:640}:{width:1400,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
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
   let back;o.traverse(c=>{if(c.name==='Chair back')back=c;});
   const north=o.userData.name==='Dining north';
   chairBacks.push(back&&Math.abs(new THREE.Box3().setFromObject(back).getCenter(new THREE.Vector3()).z-(north?5.635:7.765))<.01);
  });
  const mappedSurfaces=[],roofNormals=[],roofNames=new Set(house.model.roofSurfaces.map(r=>r.name));
  house.scene.traverse(o=>{
   if(!o.isMesh)return;
   if(roofNames.has(o.name)){const normals=o.geometry.getAttribute('normal');roofNormals.push(Array.from({length:normals.count},(_,i)=>normals.getY(i)>.5).every(Boolean));}
   const materials=Array.isArray(o.material)?o.material:[o.material];
   if(!materials.some(m=>m.map))return;
   const uv=o.geometry.getAttribute('uv');mappedSurfaces.push(Boolean(uv)&&Array.from(uv.array).every(Number.isFinite));
  });
  const wallSamples=[];
  for(const wall of house.model.walls.filter(w=>w.material==='stone'&&w.rect[1]===0&&w.bottom===0)){
   ray.set(new THREE.Vector3(wall.rect[0]+wall.rect[2]/2,Math.min(1,wall.top/2),-1),new THREE.Vector3(0,0,1));
   const hit=ray.intersectObjects(house.scene.children,true).find(h=>h.object.isMesh&&h.point.z<.01);
   if(hit?.uv)wallSamples.push([hit.point.x,hit.uv.x]);
  }
  return {openings,chairBacks,mappedSurfaces,wallSamples,roofNormals};
 });
 assert(physical.roofNormals.length>6&&physical.roofNormals.every(Boolean),'Roof normals point inward and produce self-shadow artefacts');
 assert(physical.mappedSurfaces.length>100&&physical.mappedSurfaces.every(Boolean),'Textured surface has missing or invalid UV coordinates');
 assert(physical.wallSamples.length>1,'Missing wall samples');
 const [firstX,firstU]=physical.wallSamples[0];
 for(const [x,u] of physical.wallSamples)assert(Math.abs((u-firstU)-(x-firstX)/2.4)<.001,'Stone courses change scale or alignment across wall pieces');
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
 await page.evaluate(()=>house.renderer.render(house.scene,house.camera));const viewport=page.viewportSize();await page.mouse.click(viewport.width/2,viewport.height/2);
 assert.equal(await page.evaluate(()=>{let open;house.scene.traverse(o=>{if(o.userData.door?.data.id==='D15')open=o.userData.door.open;});return open;}),true);
 await page.getByRole('button',{name:'Whole house',exact:true}).click();
 await page.screenshot({path:path.join(root,'tmp/pdfs/viewer-desktop.png'),timeout:60000});
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(root,'tmp/pdfs/viewer-mobile.png'),timeout:60000});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);assert.equal(overflow,false);
 assert.deepEqual(errors,[]);console.log('Passed texture mapping and stone scale, rooflight rays, outdoor chair orientation, PDF download, local-only load, view controls, office states, day/evening, walking, door interaction, wall collision and mobile overflow checks');
 } finally { await browser.close(); }
})();
