import * as THREE from 'three';

export function batchStatic(root,excluded=[]){
 const skip=new Set(excluded),batches=new Map();
 root.updateWorldMatrix(true,true);
 const inverse=new THREE.Matrix4().copy(root.matrixWorld).invert();
 function visit(object){
  if(skip.has(object))return;
  if(object.isMesh&&!object.material.transparent&&!Array.isArray(object.material)){
   const key=[object.material.id,object.castShadow,object.receiveShadow].join(':');
   if(!batches.has(key))batches.set(key,[]);
   batches.get(key).push(object);
  }
  for(const child of object.children)visit(child);
 }
 visit(root);
 for(const meshes of batches.values()){
  if(meshes.length<2)continue;
  const parts=meshes.map(mesh=>{
   const part=mesh.geometry.index?mesh.geometry.toNonIndexed():mesh.geometry.clone();
   part.applyMatrix4(new THREE.Matrix4().multiplyMatrices(inverse,mesh.matrixWorld));return part;
  });
  const geometry=new THREE.BufferGeometry();
  for(const name of Object.keys(parts[0].attributes)){
   const attributes=parts.map(part=>part.getAttribute(name)),first=attributes[0];
   if(attributes.some(a=>!a||a.itemSize!==first.itemSize))throw Error('Incompatible static geometry');
   const merged=new first.array.constructor(attributes.reduce((n,a)=>n+a.array.length,0));
   let offset=0;for(const attribute of attributes){merged.set(attribute.array,offset);offset+=attribute.array.length;}
   geometry.setAttribute(name,new THREE.BufferAttribute(merged,first.itemSize,first.normalized));
  }
  geometry.computeBoundingBox();geometry.computeBoundingSphere();
  const mesh=new THREE.Mesh(geometry,meshes[0].material);mesh.name='Static surfaces';
  mesh.castShadow=meshes[0].castShadow;mesh.receiveShadow=meshes[0].receiveShadow;root.add(mesh);
  for(const original of meshes){original.removeFromParent();original.geometry.dispose();}
  for(const part of parts)part.dispose();
 }
}
