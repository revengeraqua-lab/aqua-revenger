import * as THREE from 'three';

// A water photograph is gently refracted on a real plane. The opening contains
// no floating logo or oversized droplet; the water itself sets the scene.
export function createBrandWorld(scene,environment,sourceBottle,sourceCap) {
  const texture=new THREE.TextureLoader().load('/static/images/hero-water.png');
  texture.colorSpace=THREE.SRGBColorSpace;
  const material=new THREE.MeshBasicMaterial({map:texture,toneMapped:false,depthWrite:false});
  const uniforms={uWaterBlend:{value:1},uTime:{value:0},uStudio:{value:new THREE.Color(0x063a2c)}};
  material.onBeforeCompile=shader=>{
    Object.assign(shader.uniforms,uniforms);
    shader.fragmentShader=shader.fragmentShader
      .replace('#include <common>','#include <common>\nuniform float uWaterBlend;\nuniform float uTime;\nuniform vec3 uStudio;')
      .replace('#include <map_fragment>',`#ifdef USE_MAP
        vec2 liquidUv = vMapUv;
        liquidUv.x += sin(vMapUv.y * 24.0 + uTime * .32) * .0018 * uWaterBlend;
        liquidUv.y += sin(vMapUv.x * 31.0 - uTime * .24) * .0012 * uWaterBlend;
        diffuseColor *= texture2D(map, clamp(liquidUv, .001, .999));
        #endif`)
      .replace('#include <opaque_fragment>',`float halo = 1.0 - smoothstep(.0, .7, length(vMapUv - vec2(.72,.5)));
        vec3 studio = uStudio * (.87 + halo * .13);
        outgoingLight=mix(studio,outgoingLight,uWaterBlend);
        #include <opaque_fragment>`);
  };
  const backdrop=new THREE.Mesh(new THREE.PlaneGeometry(1,1),material);
  backdrop.position.z=-6;backdrop.renderOrder=-2;scene.add(backdrop);
  const lineup=[];
  for(let i=0;i<3;i++) {
    const clone=sourceBottle.clone(true);
    const cap=sourceCap.clone(true);cap.position.set(0,2.305,0);cap.rotation.set(0,0,0);cap.scale.setScalar(1);clone.add(cap);
    scene.add(clone);lineup.push(clone);
  }
  const lightColor=new THREE.Color(0xf1f2e7),darkColor=new THREE.Color(0x063a2c);
  let lastAspect=0;
  function update(state,p,camera,mobile,mainPosition,time=0) {
    const halfH=Math.tan(camera.fov*Math.PI/360)*(camera.position.z+6);
    const width=halfH*2*camera.aspect;
    backdrop.scale.set(width,halfH*2,1);
    // Cover the viewport without stretching the water texture.
    if(lastAspect!==camera.aspect) {
      const imageAspect=1931/814;
      const x=Math.min(1,camera.aspect/imageAspect),y=Math.min(1,imageAspect/camera.aspect);
      texture.repeat.set(x,y);texture.offset.set((1-x)*.5,(1-y)*.5);
      lastAspect=camera.aspect;
    }
    uniforms.uWaterBlend.value=state.roots;
    uniforms.uTime.value=time;
    scene.background.copy(darkColor).lerp(lightColor,state.paper);
    uniforms.uStudio.value.copy(scene.background);
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
