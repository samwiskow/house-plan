import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {batchStatic} from './batch_static.js';

const $=id=>document.getElementById(id);
let model;
try{const r=await fetch('./model.json');if(!r.ok)throw Error(r.status);model=await r.json();}catch(e){$('note').textContent='The model could not load. Serve the project folder and reload.';throw e;}
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setSize(innerWidth,innerHeight);
renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.shadowMap.autoUpdate=false;
renderer.domElement.tabIndex=0;renderer.domElement.setAttribute('aria-label','L-house 3D model. Drag to orbit, or use Walk to explore inside.');$('scene').append(renderer.domElement);
const scene=new THREE.Scene();scene.background=new THREE.Color('#e4e9df');scene.fog=new THREE.Fog('#e4e9df',180,350);
const camera=new THREE.PerspectiveCamera(52,innerWidth/innerHeight,.06,450);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;orbit.minDistance=.5;orbit.maxDistance=220;orbit.maxPolarAngle=Math.PI*.485;
const hemi=new THREE.HemisphereLight('#fff8e4','#7b8061',1.8);scene.add(hemi);
const sun=new THREE.DirectionalLight('#fff0cf',3.2);sun.position.set(-18,35,-28);sun.target.position.set(10,0,7);scene.add(sun,sun.target);
sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-32,right:32,top:32,bottom:-32,far:100});sun.shadow.normalBias=.035;sun.shadow.bias=-.00015;
const building=new THREE.Group(),roofs=new THREE.Group(),ceilings=new THREE.Group(),outdoor=new THREE.Group(),lights=new THREE.Group();scene.add(building,roofs,ceilings,outdoor,lights);
const palette={stone:'#d9c8ac',timber:'#ac8155',oak:'#c6a477',darkOak:'#644a31',floor:'#ded3bd',ivory:'#eee7da',roof:'#755a3e',green:'#294d38',oatmeal:'#cbbba2',worktop:'#e7ddca',soil:'#756447',grass:'#8f9d72',leaf:'#5d774e',bronze:'#92714e',glass:'#b9d2ca'};
const materials=new Map();
function canvasTexture(draw,width=256,height=256,color=true){
  const canvas=document.createElement('canvas');canvas.width=width;canvas.height=height;
  draw(canvas.getContext('2d'),width,height);
  const texture=new THREE.CanvasTexture(canvas);texture.wrapS=THREE.RepeatWrapping;texture.wrapT=THREE.RepeatWrapping;
  texture.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
  if(color)texture.colorSpace=THREE.SRGBColorSpace;return texture;
}
THREE.MathUtils.seededRandom(261006);
const random=()=>THREE.MathUtils.seededRandom();
function noiseTexture(base,variation=.04,color=true){
  return canvasTexture((ctx,w,h)=>{
    ctx.fillStyle=base;ctx.fillRect(0,0,w,h);
    const image=ctx.getImageData(0,0,w,h);
    for(let i=0;i<image.data.length;i+=4){const n=(random()-.5)*255*variation;for(let c=0;c<3;c++)image.data[i+c]+=n;}
    ctx.putImageData(image,0,0);
  },256,256,color);
}
function woodTexture(base='#c6a477',dark='#87623e',boards=false){
  return canvasTexture((ctx,w,h)=>{
    ctx.fillStyle=base;ctx.fillRect(0,0,w,h);
    for(let i=0;i<w;i+=2){
      ctx.strokeStyle=dark;ctx.globalAlpha=.04+random()*.16;ctx.lineWidth=.5+random();ctx.beginPath();
      for(let y=0;y<=h;y+=8)ctx.lineTo(i+Math.sin(y*.012+i*.04)*3+Math.sin(y*.027+i)*1.2,y);ctx.stroke();
    }
    ctx.globalAlpha=1;
    if(boards)for(let x=0;x<w;x+=w/4){ctx.fillStyle='#6c4d31';ctx.fillRect(x,0,2,h);ctx.fillStyle='#d0b086';ctx.fillRect(x+2,0,1,h);}
  },512,512);
}
function masonryTexture(paving=false){
  return canvasTexture((ctx,w,h)=>{
    ctx.fillStyle=paving?'#c9bca4':'#b4a48b';ctx.fillRect(0,0,w,h);
    const rows=paving?3:4,columns=paving?2:4,cw=w/columns,ch=h/rows;
    for(let row=0;row<rows;row++)for(let col=-1;col<columns;col++){
      const x=col*cw+(row%2)*cw/2,y=row*ch,gap=paving?1:3,tone=Math.round(random()*10);
      ctx.fillStyle=`rgb(${216+tone},${200+tone},${174+tone})`;ctx.fillRect(x+gap,y+gap,cw-gap*2,ch-gap*2);
      ctx.strokeStyle=paving?'#e4d7c0':'#eadbc0';ctx.lineWidth=1;ctx.strokeRect(x+gap+1,y+gap+1,cw-gap*2-2,ch-gap*2-2);
      for(let i=0;i<100;i++){ctx.fillStyle=i%2?'#fff8e9':'#99866a';ctx.globalAlpha=.04+random()*.07;ctx.beginPath();ctx.ellipse(x+gap+random()*(cw-gap*2),y+gap+random()*(ch-gap*2),1+random()*4,.5+random()*2,random()*Math.PI,0,Math.PI*2);ctx.fill();}
      ctx.globalAlpha=1;
    }
  },512,512);
}
function fabricTexture(){
  return canvasTexture((ctx,w,h)=>{
    ctx.fillStyle='#cbbba2';ctx.fillRect(0,0,w,h);
    for(let i=0;i<w;i+=3){ctx.fillStyle=i%2?'#decdb4':'#b8a88f';ctx.globalAlpha=.3;ctx.fillRect(i,0,1,h);ctx.fillRect(0,i,w,1);}
    ctx.globalAlpha=1;
  });
}
function reliefTexture(source){
  return canvasTexture((ctx,w,h)=>{
    ctx.drawImage(source.image,0,0,w,h);
    const input=ctx.getImageData(0,0,w,h),output=ctx.createImageData(w,h);
    const height=(x,y)=>input.data[((y+h)%h*w+(x+w)%w)*4]/255;
    for(let y=0;y<h;y++)for(let x=0;x<w;x++){
      const i=(y*w+x)*4,n=new THREE.Vector3((height(x-1,y)-height(x+1,y))*2,(height(x,y-1)-height(x,y+1))*2,1).normalize();
      output.data[i]=(n.x*.5+.5)*255;output.data[i+1]=(n.y*.5+.5)*255;output.data[i+2]=(n.z*.5+.5)*255;output.data[i+3]=255;
    }
    ctx.putImageData(output,0,0);
  },256,256,false);
}
const surfaceMaps={
  stone:masonryTexture(),timber:woodTexture('#b79364','#765334',true),oak:woodTexture(),darkOak:woodTexture('#695039','#352317'),floor:masonryTexture(true),worktop:noiseTexture('#e7ddca',.035),
  ivory:noiseTexture('#eee7da',.018),roof:woodTexture('#74573a','#4a3929',.035),green:noiseTexture('#294d38',.025),oatmeal:fabricTexture(),soil:noiseTexture('#6f5741',.2),grass:noiseTexture('#8f9d72',.12),leaf:noiseTexture('#5d774e',.12)
};
const surfaceProfiles={};
for(const [name,roughness,tile] of [['stone',.88,[2.4,1.2]],['timber',.72,[.6,2.4]],['oak',.58,[.6,1.2]],['darkOak',.6,[.6,1.2]],['floor',.82,[1.8,1.8]],['worktop',.66,[1,1]],['ivory',.85,[1,1]],['roof',.76,[2.4,2.4]],['green',.74,[.5,.5]],['oatmeal',.95,[.12,.12]],['soil',1,[.5,.5]],['grass',1,[3,3]],['leaf',.88,[.15,.15]]]){
  surfaceProfiles[name]={color:'#ffffff',roughness,map:surfaceMaps[name],roughnessMap:noiseTexture('#e0e0e0',.08,false),tile};
  if(['stone','timber','oak','darkOak','floor','oatmeal'].includes(name))surfaceProfiles[name].normalMap=reliefTexture(surfaceMaps[name]);
}
function mapSurface(geometry,material,offset=[0,0,0]){
  const tile=surfaceProfiles[material]?.tile;if(!tile)return geometry;
  const positions=geometry.getAttribute('position'),normals=geometry.getAttribute('normal'),uv=[];
  for(let i=0;i<positions.count;i++){
    const x=positions.getX(i)+offset[0],y=positions.getY(i)+offset[1],z=positions.getZ(i)+offset[2],ny=Math.abs(normals.getY(i));
    const [u,v]=ny>.5?[x,z/ny]:Math.abs(normals.getX(i))>.5?[z,y]:[x,y];
    uv.push(u/tile[0],v/tile[1]);
  }
  geometry.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));return geometry;
}
const environmentTexture=canvasTexture((ctx,w,h)=>{
  const sky=ctx.createLinearGradient(0,0,0,h);sky.addColorStop(0,'#7e9ab2');sky.addColorStop(.46,'#c9d7d2');sky.addColorStop(1,'#e3d8c1');ctx.fillStyle=sky;ctx.fillRect(0,0,w,h);
  ctx.fillStyle='#fff0c6';ctx.globalAlpha=.8;ctx.beginPath();ctx.arc(w*.73,h*.27,34,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
},512,256);environmentTexture.mapping=THREE.EquirectangularReflectionMapping;scene.environment=new THREE.PMREMGenerator(renderer).fromEquirectangular(environmentTexture).texture;scene.environmentIntensity=.55;environmentTexture.dispose();
function mat(name,transparent=false){
  const key=name+transparent;
  if(!materials.has(key)){
    const {tile,...profile}=surfaceProfiles[name]||{};
    const options={color:palette[name]||name,roughness:transparent?.16:profile.roughness??.8,metalness:name==='bronze'?.62:0,side:THREE.DoubleSide,transparent,opacity:transparent?.28:1,depthWrite:!transparent,...profile};
    if(profile.normalMap)options.normalScale=new THREE.Vector2(name==='stone'?.55:.2,name==='stone'?.55:.2);
    if(name==='glass')Object.assign(options,{color:'#ffffff',opacity:.16,roughness:.04,metalness:0,ior:1.5,envMapIntensity:1.2,forceSinglePass:true});
    const Material=name==='glass'?THREE.MeshPhysicalMaterial:THREE.MeshStandardMaterial;
    materials.set(key,new Material(options));
  }
  return materials.get(key);
}
function box(rect,bottom,top,material,parent=building){
  const [x,z,w,d]=rect;
  if(top<=bottom||w<=0||d<=0)return;
  const mesh=new THREE.Mesh(mapSurface(new THREE.BoxGeometry(w,top-bottom,d),material,[x+w/2,(bottom+top)/2,z+d/2]),mat(material,material==='glass'));
  mesh.position.set(x+w/2,(bottom+top)/2,z+d/2);mesh.castShadow=material!=='glass'&&parent!==lights;mesh.receiveShadow=true;parent.add(mesh);return mesh;
}
function roundedBox(rect,bottom,top,material,parent=building,radius=.045){
  let [x,z,w,d]=rect;if(top<=bottom||w<=0||d<=0)return;
  const bevel=Math.min(radius*.45,w*.2,d*.2,(top-bottom)*.2);
  x+=bevel;z+=bevel;w-=bevel*2;d-=bevel*2;
  const r=Math.min(radius,w/2,d/2),shape=new THREE.Shape();
  shape.moveTo(-w/2+r,-d/2);shape.lineTo(w/2-r,-d/2);shape.quadraticCurveTo(w/2,-d/2,w/2,-d/2+r);shape.lineTo(w/2,d/2-r);shape.quadraticCurveTo(w/2,d/2,w/2-r,d/2);shape.lineTo(-w/2+r,d/2);shape.quadraticCurveTo(-w/2,d/2,-w/2,d/2-r);shape.lineTo(-w/2,-d/2+r);shape.quadraticCurveTo(-w/2,-d/2,-w/2+r,-d/2);
  const geometry=new THREE.ExtrudeGeometry(shape,{depth:top-bottom-bevel*2,curveSegments:4,bevelEnabled:true,bevelSegments:1,steps:1,bevelSize:bevel,bevelThickness:bevel});geometry.rotateX(-Math.PI/2);geometry.translate(x+w/2,bottom+bevel,z+d/2);
  const mesh=new THREE.Mesh(mapSurface(geometry,material),mat(material,material==='glass'));mesh.castShadow=material!=='glass'&&parent!==lights;mesh.receiveShadow=true;parent.add(mesh);return mesh;
}
const contactMaterial=new THREE.MeshBasicMaterial({color:'#60513d',map:canvasTexture((ctx,w,h)=>{
  const gradient=ctx.createRadialGradient(w/2,h/2,0,w/2,h/2,w/2);gradient.addColorStop(0,'rgba(255,255,255,.35)');gradient.addColorStop(.5,'rgba(255,255,255,.15)');gradient.addColorStop(1,'rgba(255,255,255,0)');ctx.fillStyle=gradient;ctx.fillRect(0,0,w,h);
}),transparent:true,depthWrite:false});
function contactPatch(rect,parent=building){
  const [x,z,w,d]=rect;const mesh=new THREE.Mesh(new THREE.PlaneGeometry(w*1.25,d*1.25),contactMaterial);
  mesh.rotation.x=-Math.PI/2;mesh.position.set(x+w/2,.05,z+d/2);parent.add(mesh);return mesh;
}
function face(vertices,material,parent=building){
  const shape=new THREE.BufferGeometry();
  const coords=[],points=parent===roofs?[...vertices].reverse():vertices;
  for(let i=1;i<points.length-1;i++)for(const [x,z,y] of [points[0],points[i],points[i+1]])coords.push(x,y,z);
  shape.setAttribute('position',new THREE.Float32BufferAttribute(coords,3));shape.computeVertexNormals();
  const mesh=new THREE.Mesh(mapSurface(shape,material),mat(material,material==='glass'));mesh.receiveShadow=true;mesh.castShadow=material!=='glass'&&parent!==ceilings;parent.add(mesh);return mesh;
}
function flat(points,height,material,parent=building,holes=[]){
  const shape=new THREE.Shape(points.map(([x,z])=>new THREE.Vector2(x,-z)));
  holes.forEach(points=>shape.holes.push(new THREE.Path(points.map(([x,z])=>new THREE.Vector2(x,-z)))));
  const geometry=new THREE.ShapeGeometry(shape);geometry.rotateX(-Math.PI/2);geometry.translate(0,height,0);
  const mesh=new THREE.Mesh(mapSurface(geometry,material),mat(material,material==='glass'));mesh.receiveShadow=true;mesh.castShadow=false;parent.add(mesh);return mesh;
}
const corners=([x,z,w,d])=>[[x,z],[x+w,z],[x+w,z+d],[x,z+d]];
const within=(x,z,p)=>{let yes=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const a=p[i],b=p[j];if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;};
const rectHit=(x,z,r,pad=0)=>x>r[0]-pad&&x<r[0]+r[2]+pad&&z>r[1]-pad&&z<r[1]+r[3]+pad;
const floorGroups={},ceilingGroups={},doors=[],fixtures=[],stairGroup=new THREE.Group();
stairGroup.name='Stairs';building.add(stairGroup);
let data=model.default,pantry='default',floorMode='all',roofOn=true,night=false,walking=false,officeState='work',currentView='overview',feet=0,dirty=true;
let framePending=false,last=0;
const requestRender=()=>{dirty=true;if(!framePending){framePending=true;requestAnimationFrame(animate);}};
for(const id of ['g','u','a','o']){floorGroups[id]=new THREE.Group();floorGroups[id].name=id;building.add(floorGroups[id]);ceilingGroups[id]=new THREE.Group();ceilings.add(ceilingGroups[id]);}
function cylinder(x,y,z,r,height,material,parent,rx=0,rz=0){const mesh=new THREE.Mesh(new THREE.CylinderGeometry(r,r,height,20),mat(material));mesh.position.set(x,y,z);mesh.rotation.set(rx,0,rz);mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;}
function rail(a,b,parent,material='bronze',radius=.027){const av=new THREE.Vector3(...a),bv=new THREE.Vector3(...b),v=bv.clone().sub(av);const mesh=new THREE.Mesh(new THREE.CylinderGeometry(radius,radius,v.length(),8),mat(material));mesh.position.copy(av.add(bv).multiplyScalar(.5));mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());parent.add(mesh);return mesh;}
function chair(x,z,w,d,base,parent,angle=0,stool=false){const g=new THREE.Group();g.position.set(x+w/2,base,z+d/2);g.rotation.y=angle;parent.add(g);const b=stool?.68:.44;roundedBox([-w/2,-d/2,w,d],b,b+.09,'oatmeal',g);if(!stool)roundedBox([-w/2,-d/2,w,.085],b+.09,.92,'green',g);for(const xx of [-w*.36,w*.36])for(const zz of [-d*.36,d*.36])box([xx-.022,zz-.022,.044,.044],0,b,'oak',g);return g;}
function car(r,parent,base=0){const[x,z,w,d]=r;const group=new THREE.Group();parent.add(group);roundedBox([x+.12,z+.1,w-.24,d-.2],base+.25,base+.87,'#30473c',group,.14);roundedBox([x+1.25,z+.28,w-2.25,d-.56],base+.85,base+1.4,'#30473c',group,.15);box([x+1.34,z+.265,w-2.44,.025],base+.94,base+1.29,'#344844',group);box([x+1.34,z+d-.29,w-2.44,.025],base+.94,base+1.29,'#344844',group);for(const xx of [x+.95,x+w-1])for(const zz of [z+.1,z+d-.1]){cylinder(xx,base+.34,zz,.33,.19,'#292c24',group,Math.PI/2);cylinder(xx,base+.34,zz+(zz<z+d/2?-.105:.105),.19,.025,'bronze',group,Math.PI/2);}for(const zz of [z+.3,z+d-.65])box([x+w-.12,zz,.07,.35],base+.55,base+.68,'#f8ecd5',group);return group;}
function furnish(it,parent){
 const[x,z,w,d]=it.r,n=it.name.toLowerCase(),base=model.levels[it.floor],g=new THREE.Group();g.name=it.name;g.userData.room=it.roomId;parent.add(g);const B=(r,lo,hi,m)=>box(r,base+lo,base+hi,m,g),R=(r,lo,hi,m)=>roundedBox(r,base+lo,base+hi,m,g);
 const shadow=contactPatch(it.r,g);shadow.position.y=base+.045;
 let height=.9,solid=true;
 if(it.kind==='car'){car(it.r,g,base);height=1.5;}
 else if(it.kind==='bed'){
  R([x,z,w,d],.15,.38,'oak');R([x+.04,z+.04,w-.08,d-.08],.38,.62,'ivory');
  const side=w>d;R(side?[x+.65,z+.06,w-.73,d-.12]:[x+.06,z+.65,w-.12,d-.73],.62,.69,'green');
  for(const q of [.12,.55])R(side?[x+.1,z+d*q,.43,d*.32]:[x+w*q,z+.1,w*.32,.43],.62,.78,'oatmeal');
  B(side?[x,z,.09,d]:[x,z,w,.09],.2,1.05,'oak');height=1.05;
 }else if(it.kind==='chair'){g.remove(shadow);let angle=0;if(n==='dining chair'){if(z>7)angle=Math.PI;if(x<1.5)angle=-Math.PI/2;if(x>4.3)angle=Math.PI/2;}if(n==='desk chair')angle=Math.PI;chair(x,z,w,d,base,g,angle,n.includes('island'));height=.95;
 }else if(it.kind==='sofa'){
  const along=d>w;R([x,z,w,d],.12,.34,'oak');R([x+.06,z+.06,w-.12,d-.12],.34,.57,'oatmeal');
  R(along?[x,z,.19,d]:[x,z+d-.19,w,.19],.38,.99,'green');
  for(const q of [0,1])R(along?[x,z+q*(d-.16),w,.16]:[x+q*(w-.16),z,.16,d],.32,.78,'green');height=1;
 }else if(it.kind==='bath'||n==='bath'){
  const h=n.includes('soaking')?.7:.59;B([x,z,w,d],.07,h,'ivory');B([x+.09,z+.09,w-.18,d-.18],h-.25,h-.07,'#99b4a9');for(const r of [[x,z,w,.08],[x,z+d-.08,w,.08],[x,z,.08,d],[x+w-.08,z,.08,d]])B(r,h-.02,h+.035,'worktop');rail([x+w-.12,base+h+.12,z+.14],[x+w-.12,base+h+.34,z+.14],g);height=h;
 }else if(it.kind==='wc'){
  R([x+w*.2,z,w*.6,d*.25],.12,.81,'ivory');R([x+w*.1,z+d*.22,w*.8,d*.72],.12,.4,'ivory');R([x+w*.08,z+d*.22,w*.84,d*.72],.4,.45,'worktop');height=.8;
 }else if(it.kind==='basin'){
  B(it.r,.16,.82,'oak');B([x-.01,z-.01,w+.02,d+.02],.82,.88,'worktop');const along=w>d;
  for(const q of n.includes('double')||n.includes('two basins')?[.27,.73]:[.5]){const cx=along?x+w*q:x+w/2,cz=along?z+d/2:z+d*q;R([cx-(along?.25:.17),cz-(along?.17:.25),along?.5:.34,along?.34:.5],.88,.98,'ivory');rail([cx,base+.93,cz-.15],[cx,base+1.15,cz-.15],g);}
  height=.98;
 }else if(it.kind==='glass'){
  B(it.r,.05,2.05,'glass');height=2.05;
 }else if(it.kind==='wet'){
  B(it.r,.02,.045,'worktop');const cx=x+w/2;rail([cx,base+.8,z+.08],[cx,base+2.15,z+.08],g);rail([cx,base+2.15,z+.08],[cx,base+2.15,z+.42],g);B([cx-.12,z+.29,.24,.24],2.12,2.15,'bronze');solid=false;
 }else if(it.kind==='table'){
  height=n.includes('island')?.92:n.includes('coffee')?.4:.75;
  if(n.includes('island')){B([x+.06,z+.06,w-.12,d-.12],.08,height-.06,'oak');for(let i=0;i<4;i++)B([x+.1+i*(w-.2)/4,z+.06,.014,d-.12],.13,height-.12,'bronze');}
  else for(const xx of [x+.07,x+w-.12])for(const zz of [z+.07,z+d-.12])B([xx,zz,.05,.05],.04,height-.06,'oak');
  R([x,z,w,d],height-.06,height,n.includes('island')?'worktop':'oak');
  if(n.includes('desk')||n.includes('worktop')){const along=w>d;B(along?[x+w*.2,z+.06,w*.55,.055]:[x+w-.07,z+d*.18,.055,d*.6],height+.12,height+.62,'#273b31');B([x+w*.4,z+d*.35,.15,.15],height,height+.16,'bronze');B([x+w*.2,z+d*.55,w*.6,d*.3],height,height+.025,'#3c4736');}
 }else if(n.includes('divider')||n.includes('privacy return')){height=n.includes('privacy')?1.35:2.7;B(it.r,0,height,'ivory');}
 else if(n.includes('washer')||n.includes('dryer')){
  B(it.r,.02,.88,'ivory');cylinder(x+w/2,base+.46,z+d+.004,.22,.022,'bronze',g,Math.PI/2);cylinder(x+w/2,base+.46,z+d+.019,.18,.024,'#344742',g,Math.PI/2);B([x+.08,z+d,.2,.01],.74,.79,'#273b31');height=.88;
 }else if(n.includes('rack /')){
  for(const xx of [x+.08,x+w-.12])for(const zz of [z+.08,z+d-.12])B([xx,zz,.055,.055],.03,2.25,'#3b4433');B([x,z,w,.06],2.2,2.26,'#3b4433');rail([x,base+1.3,z+.6],[x+w,base+1.3,z+.6],g);for(const xx of [x+.15,x+w-.15])cylinder(xx,base+1.3,z+.6,.22,.13,'#292c24',g,0,Math.PI/2);height=2.25;
 }else if(n.includes('treadmill')){B(it.r,.05,.19,'#394535');B([x+.1,z+.1,w-.2,d-.2],.19,.22,'#242d24');for(const zz of [z+.1,z+d-.12])rail([x+.3,base+.2,zz],[x+.3,base+1.2,zz],g);B([x+.12,z+.1,.32,d-.2],1.15,1.22,'#394535');height=1.22;
 }else if(n.includes('dumbbell')){B(it.r,.1,.8,'#3b4433');for(let i=0;i<7;i++)cylinder(x+w/2,base+.9,z+.13+i*.27,.1,w*.8,'#292c24',g,0,Math.PI/2);height=1.05;
 }else if(n.includes('cylinder')){cylinder(x+w/2,base+1.05,z+d/2,Math.min(w,d)*.47,2,'ivory',g);height=2.05;
 }else if(n.includes('shelv')||n.includes('wardrobe')||n.includes('cupboard')||n.includes('storage')||n.includes('coats')){
  height=n.includes('coats')?1.9:2.25;const along=w>d;
  if(n.includes('wardrobe')||n.includes('cupboard')){B(it.r,.05,height,'oak');const count=Math.max(2,Math.round(Math.max(w,d)/.55));for(let i=1;i<count;i++)B(along?[x+w*i/count,z+d-.018,.012,.025]:[x+w-.018,z+d*i/count,.025,.012],.09,height-.06,'bronze');}
  else{for(let i=0;i<5;i++){B([x,z,w,d],.12+i*.46,.16+i*.46,'oak');if(i>0)for(let j=0;j<Math.floor(Math.max(w,d)/.18);j++)B(along?[x+.04+j*.18,z+.05,.12,d*.7]:[x+.05,z+.04+j*.18,w*.7,.12],.16+(i-1)*.46,.49+(i-1)*.46,j%3?'oatmeal':'green');}B(along?[x,z,w,.025]:[x,z,.025,d],.05,height,'darkOak');}
 }else if(n.includes('media')){B(it.r,.05,.42,'oak');B([x+w-.01,z+.5,.03,d-1],.82,1.9,'#172720');height=1.9;}
 else if(n.includes('bench')||n.includes('bedside')){height=n.includes('work')?.92:.46;B(it.r,.05,height,'oak');}
 else{B(it.r,.08,.86,'oak');B([x,z,w,d],.86,.92,'worktop');height=.92;}
 if(solid)fixtures.push({rect:it.r,bottom:base,top:base+height,name:it.name,room:it.roomId});
 return g;
}
function addWindow(win){const parent=floorGroups[win.floor],base=model.levels[win.floor],x=win.x,z=win.y,w=win.w,hor=win.axis==='h';
 const pane=hor?[x,z-.015,w,.03]:[x-.015,z,.03,w];box(pane,base+win.sill,base+win.head,'glass',parent);
 for(const level of [win.sill,win.head-.055])box(hor?[x,z-.055,w,.11]:[x-.055,z,.11,w],base+level,base+level+.055,'bronze',parent);
 for(const t of [0,w/2,w-.045])box(hor?[x+t,z-.055,.045,.11]:[x-.055,z+t,.11,.045],base+win.sill,base+win.head,'bronze',parent);
 if(win.private)box(pane,base+win.sill,base+win.head,'#dbe6d2',parent).material=privacyMaterial;
}
const privacyMaterial=new THREE.MeshStandardMaterial({color:'#dbe6d2',transparent:true,opacity:.68,roughness:.75,side:THREE.DoubleSide});
function addDoor(d,previous){
 const base=model.levels[d.floor],group=new THREE.Group();group.position.set(d.x,base,d.y);floorGroups[d.floor].add(group);group.name=d.id;
 const initial=['Front entrance','Boot to hall','Boot to link','Link to lobby','Proposed drive entrance','Hall to kitchen','Kitchen to laundry','Laundry to boot','Landing to dressing','Dressing to bedroom','Bedroom to ensuite','Lobby to workshop','Workshop to parking','Lobby to gym','Office','Kitchen divider','Living to terrace','Dining to terrace','Garage door'].includes(d.id);
 const state={data:d,group,open:previous?.open??initial,progress:previous?.progress??Number(initial),parts:[]};
 const h=d.axis==='h',r=h?[0,-.022,d.w,.044]:[-.022,0,.044,d.w];
 if(d.style==='garage'){
  for(let i=0;i<5;i++){const part=new THREE.Group();box([-.025,0,.05,d.w],-.225,.225,'oak',part);group.add(part);state.parts.push(part);}
 }else if(d.style==='telescopic'){
  for(let i=0;i<2;i++){const part=new THREE.Group();box([-.022,0,.044,d.w/2],0,2.35,'oak',part);group.add(part);state.parts.push(part);}
 }else{
  box(r,.03,2.12,d.style==='slider'?'glass':'oak',group);
  if(d.style==='slider'){for(const xx of [0,d.w/2,d.w-.04])box([xx,-.03,.04,.06],.02,2.14,'bronze',group);}
  else{box(h?[d.w-.13,-.045,.09,.08]:[-.045,d.w-.13,.08,.09],.95,.985,'bronze',group);if(d.id==='Kitchen to pantry')for(const t of [.55,1.2,1.85])box(h?[.04,-.026,d.w-.08,.006]:[-.026,.04,.006,d.w-.08],t,t+.01,'bronze',group);}
 }
 group.traverse(o=>{if(o.isMesh)o.userData.door=state;});doors.push(state);positionDoor(state);
}
function positionDoor(s){const d=s.data,p=s.progress,h=d.axis==='h';
 if(d.style==='pocket'){s.group.position.set(d.x-(h?d.w*p:0),model.levels[d.floor],d.y-(h?0:d.w*p));}
 else if(d.style==='slider'){s.group.position.set(d.x+d.w*p,model.levels[d.floor],d.y-.23);}
 else if(d.style==='telescopic')s.parts.forEach((part,i)=>{part.position.z=(1-p)*i*d.w/2-p*d.w/2;part.position.x=i*.05;});
 else if(d.style==='garage')s.parts.forEach((part,i)=>{const distance=(i+.5)*.45+p*2.6,r=.32;if(distance<2.13){part.position.set(0,distance,0);part.rotation.z=0;}else if(distance<2.13+r*Math.PI/2){const a=(distance-2.13)/r;part.position.set(r*(1-Math.cos(a)),2.13+r*Math.sin(a),0);part.rotation.z=-a;}else{part.position.set(r+distance-2.13-r*Math.PI/2,2.45,0);part.rotation.z=-Math.PI/2;}});
 else s.group.rotation.y=(h?-d.side:d.side)*p*Math.PI/2;
}
function makeStair(s){const parent=stairGroup,{x,z}=s;
 for(let i=0;i<7;i++){box([x,z+i*.27,1,.27],i*.1875,(i+1)*.1875,'oak',parent);box([x+1.4,z+i*.27,1,.27],1.5+(6-i)*.1875,1.5+(7-i)*.1875,'oak',parent);}
 box([x,z+1.89,2.4,1],1.32,1.5,'oak',parent);
 for(const xx of [x+1,x+1.4]){const right=xx>x+1.1;for(let i=0;i<8;i++){const zz=z+i*.27,hh=right?3-i*.1875:(i+1)*.1875;rail([xx,hh,zz],[xx,hh+.9,zz],parent,'bronze',.016);}rail([xx,right?3.9:1.0875,z],[xx,2.4,z+1.89],parent);}
 rail([x+1,2.4,z+2.4],[x+1.4,2.4,z+2.4],parent);
}
function disposeGroup(g){for(const child of [...g.children]){child.traverse(o=>o.geometry?.dispose());g.remove(child);}}
function rebuild(){
 const old=new Map(doors.map(s=>[s.data.id,s]));doors.length=0;fixtures.length=0;disposeGroup(stairGroup);
 for(const id of Object.keys(floorGroups)){disposeGroup(floorGroups[id]);disposeGroup(ceilingGroups[id]);}
 data=model[pantry];
 for(const r of data.rooms){const base=model.levels[r.floor],g=floorGroups[r.floor];if(!['U12','O3'].includes(r.id))flat(r.p,base+.025,['U3','U7','U8','U9','G3','G6','A1','A4','O2'].includes(r.id)?'floor':'oak',g);if(!['G9','A3'].includes(r.id))flat(r.p,base+2.7,'ivory',ceilingGroups[r.floor]);}
 for(const w of data.walls){const base=model.levels[w.floor];box(w.rect,base+w.bottom,base+w.top,w.external?(base?'timber':'stone'):'ivory',floorGroups[w.floor]);if(w.top===2.7)box(w.rect,base+2.7,base+(base?2.9:3),w.external?(base?'timber':'stone'):'ivory',floorGroups[w.floor]);}
 for(const f of data.furniture)furnish(f,floorGroups[f.floor]);
 for(const r of [{name:'Office sofa bed',r:[19.4,18.1,officeState==='guest'?2.2:.9,1.9],kind:officeState==='guest'?'bed':'sofa',roomId:'O4',floor:'o'},{name:'Office chair',r:officeState==='guest'?[23.5,16.9,.65,.65]:[23.7,15.25,.65,.65],kind:'chair',roomId:'O4',floor:'o'}])furnish(r,floorGroups.o);
 for(const win of model.windows)addWindow(win);
 for(const d of data.doors)addDoor(d,old.get(d.id));
 for(const s of model.stairs)makeStair(s);
 for(const r of data.rooms){if(['G9','U12','A3','O3'].includes(r.id))continue;const[x,z]=r.label;const b=model.levels[r.floor];cylinder(x,b+2.65,z,.14,.035,'#f6e8c6',floorGroups[r.floor]);}
 for(const group of [...Object.values(floorGroups),...Object.values(ceilingGroups),stairGroup])batchStatic(group,doors.map(s=>s.group));
 applyVisibility();renderer.shadowMap.needsUpdate=true;requestRender();
}
function clipped(poly,fn){const out=[];for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],fa=fn(...a),fb=fn(...b);if(fa>=-1e-8)out.push(a);if((fa>0)!==(fb>0)){const t=fa/(fa-fb);out.push([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])]);}}return out;}
function roofPlane(points,height){if(points.length<3)return;face(points.map(([x,z])=>[x,z,height(x,z)]),'roof',roofs);}
function makeRoofs(){
 const west=(x)=>5.91+2.05*(1-Math.abs(x-3.45)/3.63),east=(x,z)=>5.91+2.05*(1-Math.abs(z-9.9)/5.08);
 roofPlane(corners([-.18,-.18,3.63,15.16]),west);
 roofPlane(corners([3.45,-.18,3.63,4.999999]),west);
 for(const [z,d]of [[4.82,5.08],[9.9,5.08]]){
  const overlap=corners([3.45,z,3.63,d]);roofPlane(clipped(overlap,(x,z)=>west(x)-east(x,z)),west);roofPlane(clipped(overlap,(x,z)=>east(x,z)-west(x)),east);roofPlane(corners([7.08,z,9.3,d]),east);
 }
 for(const z of [0,14.8])face([[0,z,5.7],[6.9,z,5.7],[3.45,z,west(3.45)]],'timber');
 face([[16.2,5,5.7],[16.2,14.8,5.7],[16.2,9.9,east(16.2,9.9)]],'timber');
 function gable(x,z,w,d,eave,ridge){roofPlane(corners([x-.15,z-.15,w/2+.15,d+.3]),xx=>eave+(ridge-eave)*(xx-x+.15)/(w/2+.15));roofPlane(corners([x+w/2,z-.15,w/2+.15,d+.3]),xx=>ridge-(ridge-eave)*(xx-x-w/2)/(w/2+.15));for(const zz of [z,z+d])face([[x,zz,eave-.2],[x+w,zz,eave-.2],[x+w/2,zz,ridge]],'timber');}
 gable(18.7,11.45,7.2,9.35,5.9,7.75);gable(18.7,7.3,7.2,4.15,2.9,4.0);
 roofPlane(corners([16.08,11.23,2.74,2.64]),(x,z)=>2.92-(z-11.23)*.07);
 roofPlane(corners([22.08,4.03,3.94,3.39]),(x,z)=>2.9-(z-4.03)*.035);
 roofPlane(corners([18.55,20.8,7.5,.55]),(x,z)=>2.9-(z-20.8)*.16);
 // Gable infill belongs to the roof so floor cutaways stay open.
 for(const mesh of [...building.children])if(mesh.isMesh)roofs.add(mesh);
}
function sitePoint([x,z]){return[x-6,z-28];}
box([-80,-80,180,180],-.18,-.1,'grass',outdoor).castShadow=false;
flat(corners([-6,-28,40,65]),-.04,'grass',outdoor);
flat(model.site.forecourt.map(sitePoint),.006,'floor',outdoor);
for(const b of model.site.visitor_bays){const[x,z,w,d]=b;flat(corners([x-6,z-28,w,d]),.007,'floor',outdoor);}
for(const r of [[0,-4,16.2,4],[6.9,0,9.3,5],[-3.2,15,21.9,1.5],[-3.2,15,1.5,4.7],[16.3,13.6,2.4,1.4],[26.5,2.5,1.5,20.2],[18.7,21.2,9.3,1.5]])flat(corners(r),.014,'floor',outdoor);
flat(corners([-10,37,48,6]),-.035,'#91856b',outdoor);
for(const [x,w]of [[-6,12.25],[12.25,15.75]])box([x,36.93,w,.14],0,.42,'stone',outdoor);
for(const x of [6.25,12.25])box([x-.12,36.76,.24,.24],0,1.3,'stone',outdoor);
function tree(x,z,r){const g=new THREE.Group();g.position.set(x,0,z);outdoor.add(g);cylinder(0,1.4,0,.13,2.8,'darkOak',g);for(const [dx,dy,dz,k]of [[0,3.4,0,1],[-.55,3,-.4,.68],[.6,3.2,.45,.75],[.1,4.1,.1,.65]]){const mesh=new THREE.Mesh(new THREE.IcosahedronGeometry(r*k,2),mat('leaf'));mesh.position.set(dx,dy,dz);mesh.scale.y=.9;mesh.castShadow=true;g.add(mesh);}}
for(const[x,z,r]of [[-1,-23,1.9],[12,-23,1.8],[27,-22,2.3],[-1.5,-9,1.5],[29,-9,2.1],[30,7,1.6]])tree(x,z,r);
for(const r of [[-5,-27,38,1],[-5,-26,1,54],[32,-26,1,54]]){box(r,-.01,.16,'soil',outdoor);box(r,.12,1.25,'leaf',outdoor);}
car([-2.9,20.025,5.1,2.15],outdoor);car([-2.9,22.825,5.1,2.15],outdoor);
roundedBox([8,-2.6,2.4,1],.7,.76,'oak',outdoor);for(const x of [8.2,9,9.8]){chair(x,-3.3,.5,.5,0,outdoor);chair(x,-1.4,.5,.5,0,outdoor,Math.PI);}
for(const r of [[1,-2.8,2.3,.85],[4,-2.8,2.3,.85]]){roundedBox(r,.18,.45,'oatmeal',outdoor);box([r[0],r[1],r[2],.12],.4,.8,'oak',outdoor);}
for(const r of [[6.8,.4,.55,3.8],[15.25,.4,.55,3.8]]){box(r,.05,.55,'stone',outdoor);box([r[0]+.07,r[1]+.07,r[2]-.14,r[3]-.14],.55,.85,'leaf',outdoor);}
makeRoofs();
const practical=[];for(const[x,z,b]of [[3.5,5.5,0],[9,7,0],[11.5,11,0],[3.5,2,3],[14,9,3],[23,17,3],[22.3,10,0]]){const l=new THREE.PointLight('#ffdb9e',0,7,2);l.position.set(x,b+2.45,z);lights.add(l);practical.push(l);}
const views={
 overview:{p:[52,40,59],t:[12,1,4],note:'Drag to orbit. Scroll to move closer. The rear garden is 28 m deep.',floor:'all'},
 arrival:{p:[-1,9,38],t:[13,2.8,11],note:'The drive serves the house-facing garage. Visitor bays sit beside the walking path.',floor:'all'},
 garden:{p:[15,7,-17],t:[9,3,6],note:'Proposed stone and timber, with two connected roof forms and garden terraces.',floor:'all'},
 ground:{p:[24,33,28],t:[12,0,10],note:'Ground-floor cutaway. Compare the two pantry arrangements.',floor:'ground'},
 first:{p:[24,34,28],t:[12,3,10],note:'First-floor cutaway. All four family bedrooms and the office remain upstairs.',floor:'first'},
 living:{p:[3.3,1.65,8.35],t:[3.2,1.3,2],note:'Living and dining, looking towards the main garden. Eye height 1.65 m.',floor:'all',inside:true},
 kitchen:{p:[10.35,1.65,8.7],t:[8.0,1.2,5.8],note:'The kitchen divider and concealed pantry door can be opened. Pantry choice is below.',floor:'all',inside:true},
 parents:{p:[5.3,4.65,3.75],t:[2.9,4.25,1.6],note:'Bedroom, dressing room and private ensuite. Two doors slide into wall pockets.',floor:'all',inside:true},
 office:{p:[22.15,4.65,19.7],t:[24.0,4.0,15.5],note:'Both desks remain in place when the guest bed opens.',floor:'all',inside:true},
 garage:{p:[29,17,25],t:[22.3,0,14],note:'Garage cutaway: workshop, gym and office stair stay usable with the car parked.',floor:'ground'}
};
function applyVisibility(){for(const f of Object.keys(floorGroups)){const visible=floorMode==='all'||(floorMode==='ground'?model.levels[f]===0:model.levels[f]===3);floorGroups[f].visible=visible;ceilingGroups[f].visible=visible&&floorMode==='all'&&roofOn;}roofs.visible=floorMode==='all'&&roofOn;$('floor').value=floorMode;$('roof').textContent=roofOn&&floorMode==='all'?'Roofs on':'Roofs off';$('roof').setAttribute('aria-pressed',String(roofOn&&floorMode==='all'));}
function setRoof(on){roofOn=on;if(on)floorMode='all';applyVisibility();renderer.shadowMap.needsUpdate=true;requestRender();}
function setFloor(value){setWalking(false);floorMode=value;applyVisibility();renderer.shadowMap.needsUpdate=true;requestRender();}
function setView(name){setWalking(false);currentView=name;const v=views[name];camera.position.set(...v.p);orbit.target.set(...v.t);camera.fov=v.inside?62:52;camera.updateProjectionMatrix();if(!v.inside)camera.position.sub(orbit.target).multiplyScalar(Math.max(1,.92/camera.aspect)).add(orbit.target);floorMode=v.floor;roofOn=v.floor==='all';applyVisibility();orbit.update();$('view').value=name;$('note').textContent=v.note;$('office-field').hidden=name!=='office';renderer.shadowMap.needsUpdate=true;requestRender();}
function setNight(value){night=value;hemi.intensity=value?.42:1.8;sun.intensity=value?.12:3.2;scene.background.set(value?'#273c38':'#e4e9df');scene.fog.color.copy(scene.background);practical.forEach(l=>l.intensity=value?30:3);renderer.toneMappingExposure=value?1.25:1.05;$('light').textContent=value?'Evening':'Daylight';$('light').setAttribute('aria-pressed',String(value));document.body.classList.toggle('night',value);renderer.shadowMap.needsUpdate=true;requestRender();}
function setPantry(value){if(walking)setWalking(false);pantry=value;$('pantry').value=value;rebuild();$('note').textContent=value==='default'?'Short divider and 1.05 m open passage. Both shopping routes remain.':'Enclosed pantry: direct kitchen access, with the utility separate.';}
function setOffice(value){if(walking)setWalking(false);officeState=value;rebuild();}
function stairHeight(s,x,z){const d=z-s.z;if(d<0||d>2.89||x<s.x||x>s.x+2.4)return null;if(d>=1.89)return 1.5;if(x<s.x+1)return Math.min(1.3125,(Math.floor(d/.27)+1)*.1875);if(x>s.x+1.4)return Math.min(3,1.5+(Math.floor((1.89-d)/.27)+1)*.1875);return null;}
function surfaceHeight(x,z,previous){for(const s of model.stairs)if(rectHit(x,z,[s.x,s.z,2.4,2.89]))return stairHeight(s,x,z);if(previous>1.5){return data.rooms.some(r=>model.levels[r.floor]===3&&!['U12','O3'].includes(r.id)&&within(x,z,r.p))||data.doors.some(d=>model.levels[d.floor]===3&&rectHit(x,z,d.axis==='h'?[d.x,d.y-.22,d.w,.44]:[d.x-.22,d.y,.44,d.w]))||data.openings.some(([f,a,b,axis,w])=>model.levels[f]===3&&rectHit(x,z,axis==='h'?[a,b-.22,w,.44]:[a-.22,b,.44,w]))?3:null;}return x>-6&&x<34&&z>-28&&z<39?0:null;}
function segmentDistance(x,z,a,b){const dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));return Math.hypot(x-a[0]-dx*t,z-a[1]-dz*t);}
function doorSegment(s){const d=s.data,p=s.progress,h=d.axis==='h';if(d.style==='garage')return p>.8?null:[[d.x,d.y],[d.x,d.y+d.w]];if(d.style==='telescopic')return p>.99?null:[[d.x,d.y],[d.x,d.y+d.w*(1-p)]];if(d.style==='slider')return p>.99?null:[[d.x+d.w*p,d.y-.23],[d.x+d.w,d.y-.23]];if(d.style==='pocket')return p>.99?null:[[d.x,d.y],[d.x+(h?d.w*(1-p):0),d.y+(h?0:d.w*(1-p))]];const a=(h?-d.side:d.side)*p*Math.PI/2;return [[d.x,d.y],[d.x+(h?Math.cos(a):-Math.sin(-a))*d.w,d.y+(h?-Math.sin(a):Math.cos(a))*d.w]];}
function canMove(x,z,previous=feet){const h=surfaceHeight(x,z,previous);if(h===null||Math.abs(h-previous)>.24)return false;const rad=.21;
 for(const w of data.walls){const base=model.levels[w.floor];if(base+w.top>h+.08&&base+w.bottom<h+1.72&&rectHit(x,z,w.rect,rad))return false;}
 for(const f of fixtures)if(f.top>h+.1&&f.bottom<h+1.72&&rectHit(x,z,f.rect,rad))return false;
 for(const s of doors){const b=model.levels[s.data.floor];if(b>h+1.7||b+2.15<h+.08)continue;const seg=doorSegment(s);if(seg&&segmentDistance(x,z,...seg)<rad+.02)return false;}
 return true;
}
function move(dx,dz){const dist=Math.hypot(dx,dz),steps=Math.max(1,Math.ceil(dist/.04));for(let i=0;i<steps;i++){const nx=camera.position.x+dx/steps,nz=camera.position.z+dz/steps;if(canMove(nx,nz)){feet=surfaceHeight(nx,nz,feet);camera.position.x=nx;camera.position.z=nz;}else{if(canMove(nx,camera.position.z)){feet=surfaceHeight(nx,camera.position.z,feet);camera.position.x=nx;}if(canMove(camera.position.x,nz)){feet=surfaceHeight(camera.position.x,nz,feet);camera.position.z=nz;}}}camera.position.y=feet+1.65;requestRender();}
const keys=new Set(),ray=new THREE.Raycaster();let pointer=null,activeDoor=null;
function setWalking(value){walking=value;keys.clear();pointer=null;orbit.enabled=!value;document.body.classList.toggle('walking',value);$('walking').hidden=!value;$('aim').hidden=!value;$('touch-walk').hidden=!value;$('walk').textContent=value?'Stop':'Walk';$('walk').setAttribute('aria-pressed',String(value));
 if(value){const v=views[currentView];if(!v.inside){const upstairs=floorMode==='first';camera.position.set(upstairs?9.8:11.8,upstairs?4.65:1.65,upstairs?10.4:12.6);camera.lookAt(upstairs?7:11.8,upstairs?4.65:1.65,upstairs?10.4:9.5);}feet=camera.position.y>3?3:0;camera.position.y=feet+1.65;floorMode='all';roofOn=true;applyVisibility();renderer.shadowMap.needsUpdate=true;renderer.domElement.focus({preventScroll:true});}
 else{if(document.pointerLockElement)document.exitPointerLock();orbit.target.copy(camera.position).add(camera.getWorldDirection(new THREE.Vector3()).multiplyScalar(4));}
 requestRender();
}
function visibleObject(o){for(let p=o;p;p=p.parent)if(!p.visible)return false;return true;}
function doorAt(cursor=new THREE.Vector2()){
 scene.updateMatrixWorld(true);camera.updateMatrixWorld(true);ray.setFromCamera(cursor,camera);
 const hit=ray.intersectObjects(building.children,true).find(h=>visibleObject(h.object)&&!h.object.material?.transparent);let result=hit?.distance<3?hit.object.userData.door:null,near=Math.min(3,hit?.distance??3);
 for(const s of doors){if(!visibleObject(s.group))continue;const d=s.data,axis=d.axis==='h'?'z':'x',origin=ray.ray.origin,dir=ray.ray.direction;if(Math.abs(dir[axis])<.0001)continue;const distance=((axis==='x'?d.x:d.y)-origin[axis])/dir[axis];if(distance<0||distance>near+.04)continue;const p=ray.ray.at(distance,new THREE.Vector3()),along=d.axis==='h'?p.x-d.x:p.z-d.y,b=model.levels[d.floor];if(along>=0&&along<=d.w&&p.y>b&&p.y<b+2.3){result=s;near=distance;}}
 return result;
}
function toggleDoor(s){if(!s)return;s.open=!s.open;requestRender();}
function look(dx,dy){const e=new THREE.Euler().setFromQuaternion(camera.quaternion,'YXZ');e.y-=dx*.0038;e.x=THREE.MathUtils.clamp(e.x-dy*.0038,-1.25,1.25);camera.quaternion.setFromEuler(e);requestRender();}
renderer.domElement.addEventListener('pointerdown',e=>{if(e.button!==0)return;pointer={x:e.clientX,y:e.clientY,moved:0};if(document.pointerLockElement!==renderer.domElement)renderer.domElement.setPointerCapture(e.pointerId);renderer.domElement.focus({preventScroll:true});});
renderer.domElement.addEventListener('pointermove',e=>{if(!pointer||document.pointerLockElement)return;const dx=e.clientX-pointer.x,dy=e.clientY-pointer.y;pointer.moved+=Math.abs(dx)+Math.abs(dy);pointer.x=e.clientX;pointer.y=e.clientY;if(walking)look(dx,dy);});
renderer.domElement.addEventListener('pointerup',e=>{if(pointer&&pointer.moved<5){const r=renderer.domElement.getBoundingClientRect();toggleDoor(document.pointerLockElement===renderer.domElement?doorAt():doorAt(new THREE.Vector2((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1)));}pointer=null;});
renderer.domElement.addEventListener('pointercancel',()=>pointer=null);
document.addEventListener('mousemove',e=>{if(walking&&document.pointerLockElement===renderer.domElement)look(e.movementX,e.movementY);});
document.addEventListener('pointerlockchange',()=>{if(!document.pointerLockElement&&walking)setWalking(false);});
$('mouse-look').addEventListener('click',async()=>{renderer.domElement.focus({preventScroll:true});try{await renderer.domElement.requestPointerLock();}catch{$('note').textContent='Mouse look is unavailable. Drag to look while using the movement keys.';}});
window.addEventListener('keydown',e=>{if(e.key==='Escape'){setWalking(false);return;}if(!walking||e.target.closest('button,select,input,a')||e.ctrlKey||e.metaKey||e.altKey)return;if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d','W','A','S','D','Shift',' '].includes(e.key)){e.preventDefault();if(e.key===' '&&!e.repeat)toggleDoor(doorAt());else keys.add(e.key.toLowerCase());requestRender();}});
window.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));window.addEventListener('blur',()=>keys.clear());document.addEventListener('visibilitychange',()=>{if(document.hidden)keys.clear();});
for(const button of document.querySelectorAll('[data-key]')){button.addEventListener('pointerdown',e=>{e.preventDefault();keys.add(button.dataset.key.toLowerCase());requestRender();button.setPointerCapture(e.pointerId);});for(const event of ['pointerup','pointercancel','lostpointercapture'])button.addEventListener(event,()=>keys.delete(button.dataset.key.toLowerCase()));}
$('door').addEventListener('click',()=>toggleDoor(doorAt()));$('view').addEventListener('change',e=>setView(e.target.value));$('floor').addEventListener('change',e=>setFloor(e.target.value));$('pantry').addEventListener('change',e=>setPantry(e.target.value));$('office').addEventListener('change',e=>setOffice(e.target.value));$('roof').addEventListener('click',()=>setRoof(!(roofOn&&floorMode==='all')));$('light').addEventListener('click',()=>setNight(!night));$('walk').addEventListener('click',()=>setWalking(!walking));
orbit.addEventListener('change',requestRender);window.addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);requestRender();});
rebuild();setView('overview');setNight(false);$('status').textContent='L01 · Measured plan · 33 rooms';
function animate(now){framePending=false;const dt=Math.min((now-last)/1000,.06);last=now;let changed=false;
 for(const s of doors){const target=Number(s.open);if(Math.abs(s.progress-target)>.001){s.progress=THREE.MathUtils.damp(s.progress,target,10,dt);if(Math.abs(s.progress-target)<.001)s.progress=target;positionDoor(s);changed=true;}}
 if(changed){renderer.shadowMap.needsUpdate=true;dirty=true;}
 if(walking){const turn=(keys.has('arrowleft')?1:0)-(keys.has('arrowright')?1:0);if(turn)look(-turn*dt*350,0);const f=(keys.has('w')||keys.has('arrowup')?1:0)-(keys.has('s')||keys.has('arrowdown')?1:0),s=(keys.has('d')?1:0)-(keys.has('a')?1:0);if(f||s){const direction=camera.getWorldDirection(new THREE.Vector3());direction.y=0;direction.normalize();const right=new THREE.Vector3(-direction.z,0,direction.x),v=direction.multiplyScalar(f).add(right.multiplyScalar(s)).normalize().multiplyScalar(dt*(keys.has('shift')?3.5:2.0));move(v.x,v.z);}activeDoor=doorAt();$('door').disabled=!activeDoor;$('door').textContent=activeDoor?(activeDoor.open?'Close door':'Open door'):'Point at a door';}
 else orbit.update();
 if(dirty){renderer.render(scene,camera);dirty=false;}
 if(changed||(walking&&keys.size))requestRender();
}
window.house={model,scene,camera,renderer,doors,fixtures,views,setView,setFloor,setRoof,setNight,setPantry,setOffice,setWalking,canMove,move,surfaceHeight,stairHeight,toggleDoor,doorAt,requestRender,get state(){return{pantry,floorMode,roofOn,night,walking,officeState,currentView,feet};},setPose(x,z,h=0){feet=h;camera.position.set(x,h+1.65,z);requestRender();},capture(name){setView(name);document.body.classList.add('capture');requestRender();}};
