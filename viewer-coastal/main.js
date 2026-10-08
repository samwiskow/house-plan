import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from '../viewer/vendor/GLTFLoader.js';
import {HDRLoader} from '../viewer/vendor/HDRLoader.js';
import {batchStatic} from '../viewer-l-house/batch_static.js';
const $=id=>document.getElementById(id);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setSize(innerWidth,innerHeight);
renderer.toneMapping=THREE.AgXToneMapping;renderer.toneMappingExposure=1.35;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;renderer.shadowMap.autoUpdate=false;
$('scene').append(renderer.domElement);
const scene=new THREE.Scene();scene.background=new THREE.Color('#cbd8dc');
const camera=new THREE.PerspectiveCamera(50,innerWidth/innerHeight,.035,1600);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;orbit.maxDistance=180;orbit.minDistance=.25;
const hemi=new THREE.HemisphereLight('#cbd5dd','#907e62',.35);scene.add(hemi);
const sun=new THREE.DirectionalLight('#ffd39a',1.2);sun.position.set(-32,12,-82);sun.target.position.set(10,0,8);scene.add(sun.target);sun.castShadow=true;sun.shadow.mapSize.set(4096,4096);
Object.assign(sun.shadow.camera,{left:-40,right:40,top:40,bottom:-40,near:.5,far:120});sun.shadow.normalBias=.018;sun.shadow.bias=-.0001;scene.add(sun);
let pending=false,model,showerDoor,showerOpenQuaternion,pantryDoor,pantryClosedQuaternion,view='garden',mode='all';
function render(){pending=false;orbit.update();renderer.render(scene,camera);}
function requestRender(){if(!pending){pending=true;requestAnimationFrame(render);}}
orbit.addEventListener('change',requestRender);
const report=await fetch('../output/blender/coastal-house/model-report.json').then(r=>{if(!r.ok)throw Error('Model report missing');return r.json();});
const names={'arrival':'Arrival','garden':'Garden elevation','coastal-plot':'Coastal plot','ground-cutaway':'Ground-floor cutaway','first-cutaway':'First-floor cutaway','parents-bedroom':'Parents bedroom','suite-gallery':'Suite gallery','dressing':'Dressing room','bathroom':'Parents bathroom','bathroom-shower':'Twin showers and wall controls','guest-room':'Guest room with inset shutters','rooflights':'Rooflights clear of the valley','bathroom-vanity':'Bathroom vanity','family-bedroom':'Family bedroom','library':'Library','gym':'Gym','office':'Office','combined-room':'Kitchen, dining and living','entrance-hall':'Open entrance stair','under-stair':'Useful space below the stairs','pantry':'Full-depth kitchen pantry','kitchen-storage':'Double fridge and kitchen storage','utility':'Stone-floored utility','bathroom-shower-closed':'Enclosed shower with wall controls','terrace':'Sheltered terrace','sea-sunset':'Golden hour over the beach','coffee-station':'Pantry coffee station'};
for(const [key,label]of Object.entries(names)){$('view').add(new Option(label,key));}
function setFloor(value){mode=value;model.traverse(o=>{if(!o.name.startsWith('VIEW'))return;const {level,part}=o.userData;o.visible=part!=='option'&&(mode==='all'||(!['ceilings','roof'].includes(part)&&(mode==='ground'?!['u','o'].includes(level):!['g','a'].includes(level))));});$('floor').value=mode;renderer.shadowMap.needsUpdate=true;requestRender();}
function point(p){return[p[0],p[2],-p[1]];}
function setView(name){view=name;if(pantryDoor){if(name==='pantry')pantryDoor.quaternion.identity();else pantryDoor.quaternion.copy(pantryClosedQuaternion);}if(showerDoor){if(name==='bathroom-shower-closed')showerDoor.quaternion.identity();else showerDoor.quaternion.copy(showerOpenQuaternion);}const[p,t,lens,floor]=report.views[name];camera.position.set(...point(p));orbit.target.set(...point(t));camera.fov=2*THREE.MathUtils.radToDeg(Math.atan(24/(2*lens)));camera.updateProjectionMatrix();if(!['coffee-station','entrance-hall','under-stair','pantry','kitchen-storage','utility','bathroom-shower-closed','parents-bedroom','suite-gallery','dressing','bathroom','bathroom-shower','guest-room','bathroom-vanity','family-bedroom','library','gym','office','combined-room'].includes(name))camera.position.sub(orbit.target).multiplyScalar(Math.max(1,1.5/camera.aspect)).add(orbit.target);setFloor(floor);orbit.update();$('view').value=name;$('status').textContent=`${names[name]} · Drag to orbit · Scroll to zoom. Proposed section and assumed coastal plot.`;requestRender();}
try{
 const sky=await new HDRLoader().loadAsync('../output/blender/coastal-house/coastal-golden-hour.hdr');sky.mapping=THREE.EquirectangularReflectionMapping;scene.background=sky;const pmrem=new THREE.PMREMGenerator(renderer);scene.environment=pmrem.fromEquirectangular(sky).texture;scene.environmentIntensity=.75;pmrem.dispose();
 const gltf=await new GLTFLoader().loadAsync('../output/blender/coastal-house/coastal-house.glb',e=>{if(e.total)$('loading').textContent=`Loading the detailed model… ${Math.round(e.loaded/e.total*100)}%`;});
 model=gltf.scene;scene.add(model);model.traverse(o=>{if(o.userData.door_type==='shower'){showerDoor=o;showerOpenQuaternion=o.quaternion.clone();}if(o.userData.door_type==='pantry'){pantryDoor=o;pantryClosedQuaternion=o.quaternion.clone();}});
 model.traverse(o=>{if(!o.isMesh)return;const materials=Array.isArray(o.material)?o.material:[o.material];const glass=materials.some(m=>m.transmission>0);o.castShadow=!glass;o.receiveShadow=!glass;for(const m of materials){if(m.name.includes('mirror'))m.metalness=.95;}});
 for(const group of [...model.children]){
  if(!group.name.startsWith('VIEW')||['shower-door','pantry-door'].includes(group.userData.part))continue;
  const meshes=[];group.traverse(o=>{if(o.isMesh)meshes.push(o);});
  const compatible=new Map();
  for(const mesh of meshes){
   const key=Object.entries(mesh.geometry.attributes).map(([name,a])=>`${name}:${a.itemSize}:${a.normalized}`).sort().join('|');
   if(!compatible.has(key)){const batch=new THREE.Group();group.add(batch);compatible.set(key,batch);}
   compatible.get(key).attach(mesh);
  }
  for(const batch of compatible.values())batchStatic(batch);
 }
 $('loading').hidden=true;setView('garden');
 window.coastalHouse={scene,model,renderer,camera,report,setView,setFloor,requestRender,get state(){return{view,mode};}};
}catch(error){$('loading').textContent='The local model could not load. Open the rendered views above.';throw error;}
$('view').addEventListener('change',e=>setView(e.target.value));$('floor').addEventListener('change',e=>setFloor(e.target.value));$('reset').addEventListener('click',()=>setView(view));
window.addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);requestRender();});
