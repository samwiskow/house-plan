import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const model = await fetch('./model.json').then(r => { if (!r.ok) throw Error('House model could not be loaded'); return r.json(); });
const renderer = new THREE.WebGLRenderer({antialias:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.12;
renderer.domElement.setAttribute('aria-label','3D model of the courtyard house. Choose a view or drag to explore.');
document.querySelector('#scene').append(renderer.domElement);
const scene=new THREE.Scene();
scene.background=new THREE.Color('#e6e5dc');
scene.fog=new THREE.Fog('#e6e5dc',70,150);
const camera=new THREE.PerspectiveCamera(48,innerWidth/innerHeight,.05,200);
const orbit=new OrbitControls(camera,renderer.domElement);
orbit.enableDamping=true;orbit.dampingFactor=.12;orbit.minDistance=.25;orbit.maxDistance=75;orbit.maxPolarAngle=Math.PI*.49;
const hemisphere=new THREE.HemisphereLight('#fffcf1','#777765',1.6);scene.add(hemisphere);
const sun=new THREE.DirectionalLight('#fff1d0',3);
sun.position.set(-14,30,-18);sun.target.position.set(13,0,9);scene.add(sun,sun.target);
sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-30;sun.shadow.camera.right=30;sun.shadow.camera.top=30;sun.shadow.camera.bottom=-30;sun.shadow.camera.far=100;sun.shadow.normalBias=.055;sun.shadow.bias=-.0002;
const building=new THREE.Group(), roofs=new THREE.Group(), ceilings=new THREE.Group(), furnishing=new THREE.Group(), outdoor=new THREE.Group(), lights=new THREE.Group();
scene.add(building,roofs,ceilings,furnishing,outdoor,lights);
const palette=model.palette;
const materials=new Map();
function mat(name,transparent=false){
  const key=name+transparent;
  if(!materials.has(key))materials.set(key,new THREE.MeshStandardMaterial({color:palette[name]||name,roughness:transparent?.2:.86,metalness:name==='bronze'?.3:0,side:THREE.DoubleSide,transparent,opacity:transparent?.3:1,depthWrite:!transparent}));
  return materials.get(key);
}
function box(rect,bottom,top,material,parent=building){
  const [x,z,w,d]=rect;
  if(top<=bottom||w<=0||d<=0)return;
  const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,top-bottom,d),mat(material,material==='glass'));
  mesh.position.set(x+w/2,(bottom+top)/2,z+d/2);mesh.castShadow=material!=='glass';mesh.receiveShadow=true;parent.add(mesh);return mesh;
}
function face(vertices,material,parent=building){
  const shape=new THREE.BufferGeometry();
  const coords=[];
  for(let i=1;i<vertices.length-1;i++)for(const [x,z,y] of [vertices[0],vertices[i],vertices[i+1]])coords.push(x,y,z);
  shape.setAttribute('position',new THREE.Float32BufferAttribute(coords,3));shape.computeVertexNormals();
  const mesh=new THREE.Mesh(shape,mat(material,material==='glass'));mesh.receiveShadow=true;mesh.castShadow=material!=='glass';parent.add(mesh);return mesh;
}
function flat(points,height,material,parent=building,holes=[]){
  const shape=new THREE.Shape(points.map(([x,z])=>new THREE.Vector2(x,-z)));
  holes.forEach(points=>shape.holes.push(new THREE.Path(points.map(([x,z])=>new THREE.Vector2(x,-z)))));
  const geometry=new THREE.ShapeGeometry(shape);geometry.rotateX(-Math.PI/2);geometry.translate(0,height,0);
  const mesh=new THREE.Mesh(geometry,mat(material,material==='glass'));mesh.receiveShadow=true;mesh.castShadow=false;parent.add(mesh);return mesh;
}
const corners=([x,z,w,d])=>[[x,z],[x+w,z],[x+w,z+d],[x,z+d]];
box([-500,-500,1000,1000],-.15,-.07,'#a4ac91',outdoor).castShadow=false;
flat(model.outline,0,'#aea28c');
flat(model.courtyard,.02,'#bac5a2',outdoor);
model.paving.forEach(r=>box(r,.025,.045,'floor',outdoor));
model.rooms.forEach(room=>flat(room.polygon,.025,room.id==='S'?'#9b9280':room.category==='family'?'#d8cfbd':'floor'));
function within(point,poly){let result=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const[a,b]=poly[i],[c,d]=poly[j];if(((b>point[1])!==(d>point[1]))&&(point[0]<(c-a)*(point[1]-b)/(d-b)+a))result=!result;}return result;}
model.walls.forEach(w=>{
  const mesh=box(w.rect,w.bottom,w.top,w.material);
  if(w.material==='ivory')return;
  const[x,z,width,depth]=w.rect;
  mesh.material=[[x+width+.01,z+depth/2],[x-.01,z+depth/2],null,null,[x+width/2,z+depth+.01],[x+width/2,z-.01]].map(p=>mat(p&&within(p,model.outline)?'ivory':w.material));
});
model.roofInfill.forEach(w=>box(w.rect,w.bottom,w.top,w.material));
model.wetZones.forEach(r=>flat(corners(r),.032,'#c1d1c5'));
// The original roof study uses a pitched main block with low wing envelopes.
for(const x of [0,22.8])face([[x,12.8,3.7],[x,15.6,model.roofHeights.main_roof_ridge_m],[x,18.4,3.7]],'timber');
face([[.351,13.15,3.5],[.351,15.6,model.roofHeights.shared_ceiling_apex_m],[.351,18.05,3.5]],'ivory');
for(const roof of model.roofSurfaces){
  const mesh=face(roof.vertices.map(([x,z,h])=>[x,z,h+.018]),roof.material,roofs);mesh.name=roof.name;
  if(roof.material==='glass'){
    const edges=new THREE.EdgesGeometry(mesh.geometry);
    roofs.add(new THREE.LineSegments(edges,new THREE.LineBasicMaterial({color:palette.bronze})));
  }
}
// Flat ceilings remain over the private and service rooms; only the shared room is vaulted.
for(const room of model.rooms){
  if(['KL','OR'].includes(room.id))continue;
  flat(room.polygon,2.6,'ivory',ceilings,model.rooflights.filter(l=>l.room===room.id).map(l=>corners(l.rect)));
}
model.vaultedCeilingSurfaces.forEach(s=>face(s.vertices,'ivory',ceilings));
box([12.55,13.08,4,.14],3.1,3.5,'ivory',ceilings);
for(const light of model.rooflights){
  const lower=light.ceilingVertices,upper=light.roofVertices.map(([x,z,h])=>[x,z,h+.018]);
  const [x,z,w,d]=light.rect;
  const inset=upper.map(([a,b,h])=>[a+(a===x?.045:-.045),b+(b===z?.045:-.045),h+(upper[2][2]-upper[1][2])/d*(b===z?.045:-.045)]);
  for(let i=0;i<4;i++){
    const j=(i+1)%4;
    face([lower[i],lower[j],upper[j],upper[i]],'ivory',ceilings);
    face([upper[i],upper[j],inset[j],inset[i]],'bronze',roofs);
  }
}
for(const win of model.windows){
  const horizontal=win.orientation==='h';
  const x=horizontal?win.x:(win.x===0||win.x===12.2||win.x===16.2?win.x+.175:win.x-.175);
  const z=horizontal?(win.y===0?.175:win.y-.175):win.y;
  const r=horizontal?[x,z-.022,win.length,.044]:[x-.022,z,.044,win.length];
  box(r,.84,2.14,'glass');
  box(horizontal?[x,z-.035,win.length,.07]:[x-.035,z,.07,win.length],.81,.86,'bronze');
  box(horizontal?[x,z-.035,win.length,.07]:[x-.035,z,.07,win.length],2.12,2.17,'bronze');
  for(const t of [0,.5,1])box(horizontal?[x+t*win.length-.025,z-.045,.05,.09]:[x-.045,z+t*win.length-.025,.09,.05],.82,2.16,'bronze');
}
const doors=[];
for(const d of model.doors){
  if(d.kind==='opening')continue;
  const exterior=['OUT','COURT'].includes(d.from)||['OUT','COURT'].includes(d.to);
  const sliding=d.kind==='sliding'||d.kind==='pocket';
  const height=['O04','O06'].includes(d.id)?2.6:2.15;
  const group=new THREE.Group();building.add(group);
  const hinge=d.hingeEnd?d.width:0;
  group.position.set(d.x+(d.vertical?0:hinge),0,d.y+(d.vertical?hinge:0));
  const offset=d.hingeEnd?-d.width:0;
  const mesh=box(d.vertical?[-.028,offset,.056,d.width]:[offset,-.028,d.width,.056],.03,height,exterior&&sliding?'glass':'oak',group);
  const closed=d.vertical?new THREE.Vector2(0,d.hingeEnd?-1:1):new THREE.Vector2(d.hingeEnd?-1:1,0);
  const opened=d.vertical?new THREE.Vector2(d.side,0):new THREE.Vector2(0,d.side);
  const angle=Math.atan2(closed.y,closed.x)-Math.atan2(opened.y,opened.x);
  const state={data:d,group,angle,open:!exterior,progress:!exterior?1:0,origin:group.position.clone(),sliding};
  mesh.userData.door=state;doors.push(state);
  if(exterior&&sliding){
    for(const t of [0,.5,1])box(d.vertical?[d.x-.035,d.y+d.width*t-.025,.07,.05]:[d.x+d.width*t-.025,d.y-.035,.05,.07],0,height,'bronze');
    box(d.vertical?[d.x-.035,d.y,.07,d.width]:[d.x,d.y-.035,d.width,.07],height-.05,height,'bronze');
  }
}
function furnitureHeight(f){return f.heightM??({bed:.48,desk:.74,chair:.45,sofa:.46,table:.43,island:.92,kitchen:.9,basin:.83,wc:.48,bath:.58,bench:.45,plant:1.3,cabinet:.9,tall:2.25,stool:.65,diningchair:.46,stove:1.05}[f.kind]??.75);}
function legs(r,height,material,parent){const[x,z,w,d]=r;for(const a of [.06,w-.1])for(const b of [.06,d-.1])box([x+a,z+b,.04,.04],.04,height,material,parent);}
function makeFurniture(f,parent=furnishing){
  const group=new THREE.Group();group.userData.room=f.room;group.userData.name=f.name;parent.add(group);
  const[x,z,w,d]=f.rect,h=furnitureHeight(f),material=f.material||'oak';
  if(f.room==='GY'){
    if(f.name.includes('rack')){
      for(const a of [.06,w-.12])for(const b of [.06,d-.12])box([x+a,z+b,.06,.06],.05,2.2,'charcoal',group);
      box([x,z,w,.06],2.1,2.18,'charcoal',group);box([x,z+d-.06,w,.06],2.1,2.18,'charcoal',group);
      box([x,z+d/2,w,.04],1.3,1.34,'bronze',group);
    }else if(f.name==='Treadmill'){
      box(f.rect,.08,.22,'charcoal',group);box([x+.1,z+.2,w-.2,d-.32],.22,.23,'#525650',group);
      for(const a of [.08,w-.14])box([x+a,z+.15,.06,.06],.2,1.2,'charcoal',group);
      box([x+.08,z+.08,w-.16,.3],1.15,1.25,'charcoal',group);
    }else if(f.name==='Bench'){
      legs(f.rect,.4,'charcoal',group);box(f.rect,.4,.48,'charcoal',group);
    }else{
      legs(f.rect,.65,'charcoal',group);box(f.rect,.65,.71,'charcoal',group);
      for(let k=.15;k<d;k+=.25)box([x+.04,z+k,w-.08,.12],.71,.81,'charcoal',group);
    }
  }else if(f.room==='O'&&f.kind==='chair'){
    box([x+.05,z+.05,w-.1,d-.1],.43,.52,'charcoal',group);box([x+.04,z+d-.13,w-.08,.1],.5,1.03,'charcoal',group);
    box([x+w/2-.03,z+d/2-.03,.06,.06],.12,.43,'bronze',group);box([x,z+d/2-.035,w,.07],.09,.13,'charcoal',group);box([x+w/2-.035,z,.07,d],.09,.13,'charcoal',group);
  }else if(f.room==='S'&&f.kind==='cabinet'){
    const horizontal=w>d,extent=horizontal?w:d,bays=Math.ceil(extent/.8);
    box(f.rect,.04,.56,'darkOak',group);
    box(horizontal?[x,z,w,.035]:[x+w-.035,z,.035,d],.56,h,'darkOak',group);
    for(const level of [.6,1.02,1.44,1.86,2.28,2.56])box(f.rect,level,level+.035,'darkOak',group);
    for(let i=0;i<=bays;i++)box(horizontal?[x+extent*i/bays-.02,z,.04,d]:[x,z+extent*i/bays-.02,w,.04],.55,h,'darkOak',group);
    for(let bay=0;bay<bays;bay++)for(let shelf=0;shelf<5;shelf++){
      if(horizontal&&bay>=2&&bay<=3&&shelf<3)continue;
      for(let book=0;book<7;book++){
        const along=.08+bay*extent/bays+book*.074;
        if(along>extent-.06)continue;
        const rr=horizontal?[x+along,z+.04,.052,d-.075]:[x+.04,z+along,w-.075,.052];
        box(rr,.64+shelf*.42,.88+shelf*.42+(book%3)*.025,['#82745e','#5b6350','#af9570','#6b5143'][book%4],group);
      }
    }
    box(horizontal?[x-.025,z-.015,w+.05,d+.04]:[x-.025,z-.015,w+.05,d+.03],2.52,2.59,'darkOak',group);
    for(let k=.05;k<(horizontal?w:d);k+=.76)box(horizontal?[x+k,z+d-.025,.02,.032]:[x-.006,z+k,.032,.02],.1,.51,'bronze',group);
    if(horizontal)box([x+1.68,z+d-.045,1.22,.06],.72,1.43,'charcoal',group);
  }else if(['table','desk','diningchair','stool'].includes(f.kind)){
    legs(f.rect,h-.07,'oak',group);box(f.rect,h-.07,h,material,group);
    if(f.kind==='diningchair'){
      let rr=[x,z,w,.06];
      if(f.room==='KL')rr=[x+(x<8.35?0:w-.06),z,.06,d];
      if(f.facing)rr={south:[x,z,w,.06],north:[x,z+d-.06,w,.06],east:[x,z,.06,d],west:[x+w-.06,z,.06,d]}[f.facing];
      box(rr,h,.88,'oak',group);
    }
    if(f.kind==='desk'){
      const horizontal=w>d;
      box(horizontal?[x+w*.23,z+.06,w*.54,.045]:[x+w-.09,z+d*.23,.045,d*.54],h+.12,h+.52,'charcoal',group);
      box(horizontal?[x+w*.4,z+.14,w*.2,.14]:[x+w-.23,z+d*.4,.14,d*.2],h,h+.13,'bronze',group);
    }
  }else if(['sofa','bed','chair'].includes(f.kind)){
    box(f.rect,.08,h,material,group);
    if(f.kind==='bed'){
      const end=f.room==='P'?[x,z+d-.08,w,.08]:f.room==='C2'?[x,z,.08,d]:f.room?.startsWith('C')?[x+w-.08,z,.08,d]:[x,z,w,.08];
      box(end,.05,.98,'oak',group);
      const pillow=f.room==='P'?[x+.15,z+d-.48,w-.3,.32]:f.room==='C2'?[x+.12,z+.12,.35,d-.24]:f.room?.startsWith('C')?[x+w-.48,z+.12,.35,d-.24]:[x+.12,z+.12,w-.24,.35];
      box(pillow,h,h+.10,'porcelain',group);
      box([x+.04,z+.5,w-.08,Math.max(.1,d-.65)],h,h+.035,'#b8ac91',group);
    }else{
      let back=[x,z+d-.16,w,.16];
      if(f.room==='KL'&&f.kind==='sofa')back=[x+w-.16,z,.16,d];
      if(f.room==='O')back=[x,z,.14,d];
      if(f.facing)back={south:[x,z,w,.16],north:[x,z+d-.16,w,.16],east:[x,z,.16,d],west:[x+w-.16,z,.16,d]}[f.facing];
      box(back,h,.85,material,group);
      if(w>d){box([x,z,.12,d],h,.65,material,group);box([x+w-.12,z,.12,d],h,.65,material,group);}
      else if(f.kind==='sofa'){box([x,z,w,.12],h,.65,material,group);box([x,z+d-.12,w,.12],h,.65,material,group);}
    }
  }else if(['bath','basin'].includes(f.kind)){
    box(f.rect,.08,h,'porcelain',group);
    const count=f.name.toLowerCase().includes('double')?2:1;
    for(let i=0;i<count;i++)box([x+.07+i*w/count,z+.07,w/count-.14,d-.14],h,h+.005,'#aebbb4',group);
    box([x+.04,z+.04,.035,.09],h,h+.14,'bronze',group);
  }else{
    box(f.rect,.035,h,material,group);
    if(['island','kitchen'].includes(f.kind)){
      box([x-.025,z-.025,w+.05,d+.05],h,h+.035,'floor',group);
      for(let i=.6;i<w;i+=.6)box([x+i-.005,z+d+.001,.01,.008],.12,h-.06,'#c9beaa',group);
    }
    if(f.kind==='island')box([x+.45,z+.18,.65,.45],h+.036,h+.044,'charcoal',group);
    if(f.name==='Sink base')box([x+.1,z+.08,w-.2,d-.16],h+.036,h+.04,'#9eaba7',group);
    if(f.kind==='stove')box([x+w-.035,z+.06,.04,d-.12],.35,.75,'#5c6054',group);
    if(f.name==='Media unit')box([x+w-.01,z+.4,.04,1.35],.85,1.65,'charcoal',group);
  }
}
model.furniture.forEach(f=>makeFurniture(f));
model.outdoorFurniture.forEach(f=>makeFurniture(f,outdoor));
model.plantingBeds.forEach(({rect},i)=>{
  box(rect,.03,.12,'#87755c',outdoor);
  const[x,z,w,d]=rect;
  for(let k=0;k<Math.ceil(d/.48);k++){
    const plant=new THREE.Mesh(new THREE.IcosahedronGeometry(.28,1),mat(i?'#7c885e':'#899465'));
    plant.position.set(x+w*(.35+(k%2)*.3),.35,z+.22+k*.48);plant.scale.set(1,.85+(k%3)*.2,1);plant.castShadow=true;outdoor.add(plant);
  }
});
const practical=[];
for(const l of model.lights){
  const[x,z,h]=l.point;
  if(l.kind==='pillar')box([x-.09,z-.09,.18,.18],.03,.75,'bronze',lights);
  if(l.kind==='linear')box(l.axis==='x'?[x-l.length/2,z-.025,l.length,.05]:[x-.025,z-l.length/2,.05,l.length],h,h+.035,'porcelain',lights);
  if(l.kind==='chandelier'){
    box([x-.018,z-.018,.036,.036],h,4.4,'bronze',lights);
    for(let i=0;i<6;i++){
      const a=i*Math.PI/3,px=x+Math.cos(a)*.48,pz=z+Math.sin(a)*.48;
      const shade=new THREE.Mesh(new THREE.CylinderGeometry(.09,.14,.22,16),mat('porcelain'));
      shade.position.set(px,h-.04,pz);lights.add(shade);
      const arm=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,.48,8),mat('bronze'));
      arm.position.set((x+px)/2,h-.2,(z+pz)/2);arm.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),new THREE.Vector3(px-x,0,pz-z).normalize());lights.add(arm);
    }
  }
  if(l.kind==='ambient wall')box([x-.07,z-.07,.14,.14],h-.12,h+.12,'bronze',lights);
  if(l.kind==='pillar'||l.kind==='ambient wall'||l.kind==='chandelier'){
    const point=new THREE.PointLight('#ffd59b',0,l.kind==='chandelier'?8:4,2);point.position.set(x,h+.12,z);lights.add(point);practical.push(point);
  }
}
const interiorFill=[];
for(const [x,z,h] of [[3,16,3],[8.5,15.6,3.6],[12.5,16.5,3.2],[14.5,11.8,2.4],[20,10.8,2.3],[20,7.5,2.4]]){
  const light=new THREE.PointLight('#fff0d4',18,8,2);light.position.set(x,h,z);lights.add(light);interiorFill.push(light);
}
const views={
  overview:{position:[34,26,38],target:[13.5,0,9],title:'A house around a garden',note:'Low stone wings meet a taller timber shared room. Drag to orbit; scroll to move closer.'},
  arrival:{position:[35,9,38],target:[13.5,2,15.8],title:'Arriving at the house',note:'Entrance and boot room sit beside the kitchen, with the gym at the service end.'},
  courtyard:{position:[27,14,-18],target:[13,1.2,8.5],title:'The sheltered courtyard',note:'Dining and the glazed garden room make the strongest connection to the courtyard.'},
  garden:{position:[35,9,-8],target:[20.5,1.4,9],title:'The garden and service end',note:'Rear plant continues the gym block. The library takes daylight from a rooflight.'},
  living:{position:[13.65,1.62,17.05],target:[3.2,1.7,15.6],title:'One continuous shared room',note:'Ivory kitchen, forest-green island and warm oak beneath a continuous vault.'},
  dining:{position:[9.4,1.62,17.65],target:[14.6,1.6,11.3],title:'Dining toward the garden room',note:'The main floor and warm finishes continue into the open, glazed sitting area.'},
  library:{position:[18.4,1.55,11.8],target:[20.55,1.3,9.5],title:'A library with room for films',note:'Dark timber bookshelves, an integrated television and warm reading light. Rooflight shown as a reservation.'},
  office:{position:[19.2,2.0,9.05],target:[21.3,1.0,7.0],title:'One L-shaped desk, two setups',note:'A continuous corner worktop connects the professional and personal setups, with the sofa bed still usable.'},
  plan:{position:[13.575,35,9.21],target:[13.575,0,9.2],title:'The furnished plan',note:'Roof removed to see the layout. North is down; the courtyard opens south.'}
};
let currentView='overview',night=false,walking=false,roofOn=true;
const keys=new Set();
function setRoof(value){roofOn=value;roofs.visible=value;ceilings.visible=value;document.querySelector('#roof-toggle').textContent=value?'Roof on':'Roof off';document.querySelector('#roof-toggle').setAttribute('aria-pressed',String(value));}
function setNight(value){night=value;document.body.classList.toggle('night',value);scene.background.set(value?'#222f38':'#e6e5dc');scene.fog.color.copy(scene.background);hemisphere.intensity=value?.35:1.6;sun.intensity=value?.08:3;practical.forEach(l=>l.intensity=value?12:0);interiorFill.forEach(l=>l.intensity=value?28:18);document.querySelector('#light-toggle').textContent=value?'Evening':'Daylight';document.querySelector('#light-toggle').setAttribute('aria-pressed',String(value));}
function setWalking(value){walking=value;orbit.enabled=!value;keys.clear();document.querySelector('#walk-toggle').textContent=value?'Stop walking':'Walk';document.querySelector('#walk-toggle').setAttribute('aria-pressed',String(value));if(value){if(camera.position.y>3)camera.position.set(17.8,1.65,17.4);camera.position.y=1.65;document.querySelector('#view-note').textContent='Drag to look. Use WASD or arrow keys to walk; click a door to open it. Escape stops walking.';}else{const direction=new THREE.Vector3();camera.getWorldDirection(direction);orbit.target.copy(camera.position).addScaledVector(direction,3);}}
function setView(name){
  const view=views[name];currentView=name;setWalking(false);camera.position.set(...view.position);orbit.target.set(...view.target);if(!['living','dining','library','office'].includes(name))camera.position.sub(orbit.target).multiplyScalar(Math.max(1,.95/camera.aspect)).add(orbit.target);camera.fov=name==='plan'?38:['living','dining','library','office'].includes(name)?65:48;camera.updateProjectionMatrix();orbit.update();setRoof(name!=='plan');
  document.querySelector('#view-title').textContent=view.title;document.querySelector('#view-note').textContent=view.note;
  document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===name));document.querySelector('#office-control').hidden=name!=='office';
}
function setOffice(mode){
  furnishing.children.filter(g=>g.userData.room==='O').forEach(g=>{g.traverse(o=>{if(o.geometry)o.geometry.dispose();});furnishing.remove(g);});
  model.officeStates[mode].forEach(f=>makeFurniture(f));document.querySelector('#office-state').value=mode;
}
function canMove(x,z){
  if(x< -8||x>36||z< -12||z>28)return false;
  if(model.walls.some(w=>w.bottom<1.5&&w.top>.2&&x>w.rect[0]-.18&&x<w.rect[0]+w.rect[2]+.18&&z>w.rect[1]-.18&&z<w.rect[1]+w.rect[3]+.18))return false;
  return !doors.some(({data:d,open})=>!open&&(d.vertical?Math.abs(x-d.x)<.2&&z>d.y-.12&&z<d.y+d.width+.12:Math.abs(z-d.y)<.2&&x>d.x-.12&&x<d.x+d.width+.12));
}
let pointer=null;
renderer.domElement.addEventListener('pointerdown',e=>{pointer={x:e.clientX,y:e.clientY,moved:0};});
renderer.domElement.addEventListener('pointermove',e=>{if(!pointer)return;const dx=e.clientX-pointer.x,dy=e.clientY-pointer.y;pointer.moved+=Math.abs(dx)+Math.abs(dy);pointer.x=e.clientX;pointer.y=e.clientY;if(walking){const angles=new THREE.Euler().setFromQuaternion(camera.quaternion,'YXZ');angles.y-=dx*.004;angles.x=THREE.MathUtils.clamp(angles.x-dy*.004,-1.35,1.35);camera.quaternion.setFromEuler(angles);}});
renderer.domElement.addEventListener('pointerup',e=>{if(pointer&&pointer.moved<5){const ray=new THREE.Raycaster();ray.setFromCamera(new THREE.Vector2(e.clientX/innerWidth*2-1,1-e.clientY/innerHeight*2),camera);const hit=ray.intersectObjects(building.children,true)[0];if(hit?.object.userData.door&&hit.distance<8){hit.object.userData.door.open=!hit.object.userData.door.open;}}pointer=null;});
window.addEventListener('keydown',e=>{if(e.key==='Escape')setWalking(false);if(walking&&['w','a','s','d','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();keys.add(e.key);}});
window.addEventListener('keyup',e=>keys.delete(e.key));window.addEventListener('blur',()=>keys.clear());
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));
document.querySelector('#roof-toggle').addEventListener('click',()=>setRoof(!roofOn));document.querySelector('#light-toggle').addEventListener('click',()=>setNight(!night));document.querySelector('#walk-toggle').addEventListener('click',()=>setWalking(!walking));document.querySelector('#office-state').addEventListener('change',e=>setOffice(e.target.value));
window.addEventListener('resize',()=>{const old=Math.max(1,.95/camera.aspect);camera.aspect=innerWidth/innerHeight;if(!walking&&!['living','dining','library','office'].includes(currentView))camera.position.sub(orbit.target).multiplyScalar(Math.max(1,.95/camera.aspect)/old).add(orbit.target);camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);});
const clock=new THREE.Clock();
renderer.setAnimationLoop(()=>{
  const dt=Math.min(clock.getDelta(),.05);
  doors.forEach(s=>{s.progress+=(Number(s.open)-s.progress)*Math.min(1,dt*8);if(s.sliding){s.group.position.copy(s.origin);s.group.position[s.data.vertical?'z':'x']+=s.data.width*s.progress*(s.data.kind==='pocket'?s.data.pocketDirection:.48);}else s.group.rotation.y=s.angle*s.progress;});
  if(walking){
    const forward=(keys.has('w')||keys.has('ArrowUp')?1:0)-(keys.has('s')||keys.has('ArrowDown')?1:0),side=(keys.has('d')||keys.has('ArrowRight')?1:0)-(keys.has('a')||keys.has('ArrowLeft')?1:0);
    const direction=new THREE.Vector3();camera.getWorldDirection(direction);direction.y=0;direction.normalize();const right=new THREE.Vector3(-direction.z,0,direction.x),move=direction.multiplyScalar(forward).addScaledVector(right,side);if(move.lengthSq()>0)move.normalize().multiplyScalar(dt*2);if(canMove(camera.position.x+move.x,camera.position.z))camera.position.x+=move.x;if(canMove(camera.position.x,camera.position.z+move.z))camera.position.z+=move.z;
  }else orbit.update();
  renderer.render(scene,camera);
});
setView(new URLSearchParams(location.search).get('view')||'overview');
document.querySelector('#status').textContent=`26 spaces · ${model.metadata.giaM2.toFixed(2)} m² internal envelope`;
window.house={model,views,setView,setRoof,setNight,setOffice,setWalking,canMove,camera,scene,renderer,get state(){return{currentView,night,walking,roofOn,officeFurniture:furnishing.children.filter(g=>g.userData.room==='O').map(g=>g.userData.name)};},capture(name,evening=false){document.body.classList.add('capture');setView(name);setNight(evening);}};
