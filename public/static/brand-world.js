import * as THREE from 'three';

export function createBrandWorld(scene,environment,sourceBottle,sourceCap) {
  const texture=new THREE.TextureLoader().load('/static/images/forest-stream.png');
  texture.colorSpace=THREE.SRGBColorSpace;
  const forestMaterial=new THREE.MeshBasicMaterial({map:texture,toneMapped:false,depthWrite:false});
  const forestUniforms={uForestBlend:{value:.92},uStudio:{value:new THREE.Color(0x063a2c)}};
  forestMaterial.onBeforeCompile=shader=>{
    Object.assign(shader.uniforms,forestUniforms);
    shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nuniform float uForestBlend;\nuniform vec3 uStudio;').replace('#include <opaque_fragment>','outgoingLight=mix(uStudio,outgoingLight,uForestBlend);\n#include <opaque_fragment>');
  };
  const forest=new THREE.Mesh(new THREE.PlaneGeometry(1,1),forestMaterial);
  forest.position.z=-6;forest.renderOrder=-2;scene.add(forest);
  const typeCanvas=document.createElement('canvas');typeCanvas.width=2048;typeCanvas.height=360;
  const ctx=typeCanvas.getContext('2d');ctx.fillStyle='#124b36';ctx.font='700 260px Arial';ctx.textAlign='center';ctx.fillText('REVENGER',1024,275);
  const typeMap=new THREE.CanvasTexture(typeCanvas);typeMap.colorSpace=THREE.SRGBColorSpace;
  const typography=new THREE.Mesh(new THREE.PlaneGeometry(12,2.1),new THREE.MeshBasicMaterial({map:typeMap,transparent:true,opacity:.055,depthWrite:false}));
  typography.position.set(.4,.15,-2);scene.add(typography);
  const drop=new THREE.Group();
  const waterMaterial=new THREE.MeshPhysicalMaterial({color:0xf0fff9,transmission:.94,roughness:.025,thickness:.65,ior:1.333,envMap:environment,envMapIntensity:1.5,clearcoat:1});
  const profile=new THREE.SplineCurve([new THREE.Vector2(.008,-.78),new THREE.Vector2(.48,-.65),new THREE.Vector2(.71,-.2),new THREE.Vector2(.62,.34),new THREE.Vector2(.35,.78),new THREE.Vector2(.008,1.38)]).getPoints(64);
  profile.forEach(p=>p.x=Math.max(.005,p.x));
  drop.add(new THREE.Mesh(new THREE.LatheGeometry(profile,72),waterMaterial));scene.add(drop);
  const lineup=[];
  for(let i=0;i<3;i++) {
    const clone=sourceBottle.clone(true);
    const cap=sourceCap.clone(true);cap.position.set(0,2.305,0);cap.rotation.set(0,0,0);cap.scale.setScalar(1);clone.add(cap);
    scene.add(clone);lineup.push(clone);
  }
  const lightColor=new THREE.Color(0xf1f2e7),darkColor=new THREE.Color(0x063a2c);
  function update(state,p,camera,mobile,mainPosition) {
    const halfH=Math.tan(camera.fov*Math.PI/360)*(camera.position.z+6);
    const width=halfH*2*camera.aspect;
    forest.scale.set(width,Math.max(halfH*2,width*1.25),1);
    forest.position.y=.7-state.roots*.45;
    forestUniforms.uForestBlend.value=state.roots*.92;forest.visible=state.roots>.001;
    scene.background.copy(darkColor).lerp(lightColor,state.paper);
    forestUniforms.uStudio.value.copy(scene.background);
    typography.visible=state.paper>.01;typography.material.opacity=state.paper*.055;
    drop.visible=state.roots>.01;
    drop.position.set(mobile?.45:1.8,mobile?-.65:.10,0);
    drop.scale.setScalar((mobile?.52:.9)*(.5+state.roots*.5));
    drop.rotation.set(.08,p*3,-.08);drop.position.y+=Math.sin(p*8)*.12;
    const fit=mobile?Math.min(1,camera.aspect/.46):Math.min(1,camera.aspect/1.44);
    const desktopPositions=[.35,2.65,3.8];
    const mobilePositions=[-.88,.32,.92];
    const sizes=(mobile?[.24,.36,.42]:[.37,.63,.70]).map(size=>size*fit);
    lineup.forEach((b,i)=>{
      b.visible=state.lineup>.004;
      b.scale.setScalar(sizes[i]*state.lineup);
      b.position.set((mobile?mobilePositions[i]:desktopPositions[i])*fit,(mobile?-2.35:-2.20)+sizes[i]*2.35,(-.18-i*.04));
      b.position.y-=(1-state.lineup)*1.5;
      b.rotation.set(0,(i-1)*.10,(i-1)*-.045*state.lineup);
    });
  }
  return {update};
}
