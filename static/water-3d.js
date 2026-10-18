import * as THREE from 'three';

export function makeWater(scene,environment) {
  const waterMaterial=new THREE.MeshPhysicalMaterial({color:0xe0fff5,roughness:.04,transmission:.88,thickness:.07,ior:1.333,clearcoat:1,envMap:environment,envMapIntensity:1.1,transparent:true,opacity:1});
  const stream=new THREE.Mesh(new THREE.BufferGeometry(),waterMaterial);stream.renderOrder=4;scene.add(stream);
  const droplets=new THREE.InstancedMesh(new THREE.SphereGeometry(1,8,6),waterMaterial,26);scene.add(droplets);
  const glass=new THREE.Group();scene.add(glass);
  const glassMaterial=new THREE.MeshPhysicalMaterial({color:0xffffff,roughness:.025,transmission:1,thickness:.035,ior:1.5,envMap:environment,envMapIntensity:1.5,side:THREE.DoubleSide});
  const profile=[[.01,0],[.42,0],[.47,.035],[.515,1.16],[.49,1.17],[.445,.10],[.01,.10]].map(([x,y])=>new THREE.Vector2(x,y));
  glass.add(new THREE.Mesh(new THREE.LatheGeometry(profile,80),glassMaterial));
  const rim=new THREE.Mesh(new THREE.TorusGeometry(.503,.012,10,80),glassMaterial);rim.rotation.x=Math.PI/2;rim.position.y=1.165;glass.add(rim);
  const fillMaterial=new THREE.MeshPhysicalMaterial({color:0xe0f6ed,transmission:.94,thickness:.8,roughness:.025,ior:1.333,envMap:environment,envMapIntensity:.8});
  const fill=new THREE.Mesh(new THREE.CylinderGeometry(.467,.445,1,64),fillMaterial);glass.add(fill);
  const surface=new THREE.Mesh(new THREE.CircleGeometry(.465,64),new THREE.MeshBasicMaterial({color:0xd6f8ee,transparent:true,opacity:.16,side:THREE.DoubleSide}));surface.rotation.x=-Math.PI/2;glass.add(surface);
  const rings=[];
  for(let i=0;i<2;i++){const ring=new THREE.Mesh(new THREE.TorusGeometry(.36,.005,6,64),new THREE.MeshBasicMaterial({color:0xf3fffb,transparent:true,opacity:.3}));ring.rotation.x=-Math.PI/2;scene.add(ring);rings.push(ring);}
  let curve,lastKey='';const dummy=new THREE.Object3D();
  function update(mouth,state,time,mobile) {
    const amount=state.flow;
    const glassScale=(mobile?.67:1)*state.glass;
    const cupX=mouth.x+(mobile?.10:-.08);
    glass.visible=state.glass>.005;glass.position.set(cupX,-2.42,.25);glass.scale.setScalar(glassScale);
    const fillHeight=.05+state.fill*.80;
    fill.scale.y=fillHeight;fill.position.y=.10+fillHeight/2;surface.position.y=.105+fillHeight;
    const end=new THREE.Vector3(cupX,-2.42+glassScale*(.105+fillHeight),.25);
    stream.visible=amount>.005;droplets.visible=stream.visible;
    if(stream.visible){
      const key=[mouth.x,mouth.y,mouth.z,end.y].map(v=>v.toFixed(3)).join(',');
      if(key!==lastKey){
        curve=new THREE.CatmullRomCurve3([mouth.clone(),mouth.clone().add(new THREE.Vector3(-.09,-.22,.015)),new THREE.Vector3((mouth.x+end.x)/2,(mouth.y+end.y)/2,.15),end]);
        const old=stream.geometry;stream.geometry=new THREE.TubeGeometry(curve,38,.023,8,false);old.dispose();lastKey=key;
      }
      waterMaterial.opacity=amount;
      for(let i=0;i<26;i++){
        const t=(i/26+time*.52)%1,point=curve.getPoint(t);point.x+=Math.sin(i*2.4+time*2)*.019*t;
        dummy.position.copy(point);const r=(.009+(i%4)*.003)*amount;dummy.scale.set(r,r*1.8,r);dummy.updateMatrix();droplets.setMatrixAt(i,dummy.matrix);
      }
      droplets.instanceMatrix.needsUpdate=true;
    }
    rings.forEach((ring,i)=>{const t=(time*.65+i/2)%1;ring.visible=amount>.005;ring.position.copy(end);ring.position.y+=.008;ring.scale.setScalar((.2+t*.7)*glassScale);ring.material.opacity=(1-t)*.28*amount;});
  }
  return {update};
}
