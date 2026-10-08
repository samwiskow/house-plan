const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..'),out=path.join(root,'tmp/blender-source');
const base=process.env.BASE_URL||'http://127.0.0.1:4193/';
(async()=>{fs.mkdirSync(path.join(out,'textures'),{recursive:true});const browser=await chromium.launch({channel:'chromium',executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});try{
 const page=await browser.newPage({viewport:{width:600,height:400}});
 let source=fs.readFileSync(path.join(root,'viewer-l-house/main.js'),'utf8');
 if(!source.includes('batchStatic(group,doors.map(s=>s.group));'))throw Error('Static batch call changed');
 source=source.replace('batchStatic(group,doors.map(s=>s.group));','void group;');
 source+='\nwindow.house.blender={building,roofs,ceilings,outdoor,floorGroups,ceilingGroups,materials};';
 await page.route('**/viewer-l-house/main.js',route=>route.fulfill({contentType:'text/javascript',body:source}));
 await page.goto(new URL('viewer-l-house/',base).href);await page.waitForFunction(()=>window.house?.blender);
 const result=await page.evaluate(()=>{
  const {building,roofs,ceilings,outdoor,floorGroups,ceilingGroups,materials}=house.blender;
  building.name='Structure';roofs.name='Roofs';ceilings.name='Ceilings';outdoor.name='Site';
  for(const [id,g]of Object.entries(ceilingGroups))g.name='Ceiling '+id;
  const materialNames=new Map([...materials].map(([name,material])=>[material.uuid,name.replace(/false$|true$/,'')]));
  const materialData={},textures={},geometries={};let next=0;
  function texture(t){if(!t)return null;if(!textures[t.uuid])textures[t.uuid]={image:t.image.toDataURL('image/png'),color:t.colorSpace==='srgb'};return t.uuid;}
  function material(m){if(!materialData[m.uuid])materialData[m.uuid]={name:materialNames.get(m.uuid)||'Privacy glass',color:m.color?.toArray()||[1,1,1],roughness:m.roughness??1,metalness:m.metalness??0,opacity:m.opacity,transparent:m.transparent,map:texture(m.map),normalMap:texture(m.normalMap),roughnessMap:texture(m.roughnessMap),normalScale:m.normalScale?.toArray()};return m.uuid;}
  function node(o){if(o.isMesh&&o.material.type==='MeshBasicMaterial')return null;
   const item={id:'n'+next++,name:o.name||o.type,type:o.type,matrix:o.matrix.toArray(),room:o.userData.room,children:[]};
   if(o.isMesh){const g=o.geometry,id=g.uuid;if(!geometries[id])geometries[id]={type:g.type,position:Array.from(g.attributes.position.array),normal:g.attributes.normal?Array.from(g.attributes.normal.array):null,uv:g.attributes.uv?Array.from(g.attributes.uv.array):null,index:g.index?Array.from(g.index.array):null};item.geometry=id;item.material=material(o.material);item.castShadow=o.castShadow;}
   const door=house.doors.find(d=>d.group===o);if(door)item.door={...door.data,progress:door.progress};
   item.children=o.children.map(node).filter(Boolean);return item;
  }
  const snapshot=roots=>{house.scene.updateMatrixWorld(true);return roots.map(node);};
  house.setView('overview');const normal=snapshot([building,roofs,ceilings,outdoor]);
  house.setPantry('enclosed');const enclosed=snapshot([floorGroups.g]);
  house.setPantry('default');document.getElementById('office').value='guest';document.getElementById('office').dispatchEvent(new Event('change'));const guest=snapshot([floorGroups.o]);
  return{normal,enclosed,guest,geometries,materials:materialData,textures,model:house.model,views:house.views};
 });
 for(const [id,t]of Object.entries(result.textures)){fs.writeFileSync(path.join(out,'textures',id+'.png'),Buffer.from(t.image.split(',')[1],'base64'));t.path='textures/'+id+'.png';delete t.image;}
 result.provenance={modelSha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'viewer-l-house/model.json'))).digest('hex'),units:'metres',source:'L01 measured browser scene; individual objects retained before batching'};
 fs.writeFileSync(path.join(out,'scene.json'),JSON.stringify(result));console.log(JSON.stringify({path:out,geometries:Object.keys(result.geometries).length,materials:Object.keys(result.materials).length,textures:Object.keys(result.textures).length}));
 }finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
