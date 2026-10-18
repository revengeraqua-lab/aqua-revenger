import * as THREE from 'three';
import { RoomEnvironment } from './vendor/three/RoomEnvironment.js';
import { makeBottle } from './bottle-3d.js';
import { makeWater } from './water-3d.js';
import { createBrandWorld } from './brand-world.js';
import { createStoryTimeline } from './story-timeline.js';

const track=document.querySelector('.scroll-story');
const stage=track.querySelector('.story-stage');
const mount=stage.querySelector('.scene-canvas');
const copies=[...stage.querySelectorAll('.story-copy')];
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const clamp=x=>Math.max(0,Math.min(1,x));
const phase=(p,a,b)=>{const t=clamp((p-a)/(b-a));return t*t*(3-2*t);};
let renderer,scene,camera,model,water,world;
const {state,timeline}=createStoryTimeline();
let target=0,current=0,frame=0,lastTime=0,flowTime=0;
let pointerX=0,pointerY=0;
let start=0,distance=1,inView=true,mobile=false;
let activeCopy=-1;
let paused=document.body.classList.contains('motion-paused');
const mouth=new THREE.Vector3();
const capClosed=new THREE.Vector3();
const capAnchor=new THREE.Vector3();

function measure() {
  mobile=innerWidth<=900;
  start=track.getBoundingClientRect().top+scrollY;
  distance=Math.max(1,track.offsetHeight-stage.offsetHeight);
  if(renderer){const w=stage.clientWidth,h=stage.clientHeight;renderer.setPixelRatio(Math.min(devicePixelRatio,mobile?1.25:1.5));renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}
  onScroll();
}
function onScroll() {
  target=reduced.matches?0:clamp((scrollY-start)/distance);
  const rect=track.getBoundingClientRect();
  inView=rect.bottom>0&&rect.top<innerHeight;
  requestFrame();
}
function requestFrame(){if(!frame&&!document.hidden)frame=requestAnimationFrame(render);}

function updateText(p) {
  const boundaries=[0,.22,.43,.64,.88,1];
  const index=p<.22?0:p<.43?1:p<.64?2:p<.88?3:4;
  copies.forEach((copy,i)=>{const alpha=(i===0?1:phase(p,boundaries[i]-.025,boundaries[i]+.025))*(i===4?1:1-phase(p,boundaries[i+1]-.025,boundaries[i+1]+.025));copy.style.opacity=alpha;copy.style.visibility=alpha>.001?"visible":"hidden";copy.style.transform=`translateY(${(1-alpha)*(p>boundaries[i]? -20:24)}px)`;});
  if(index!==activeCopy){
    copies.forEach((copy,i)=>{copy.classList.toggle('is-active',i===index);copy.setAttribute('aria-hidden',String(i!==index));for(const link of copy.querySelectorAll('a,button'))link.tabIndex=i===index?0:-1;});
    activeCopy=index;stage.dataset.chapter=String(index+1);
    stage.querySelector('.story-caption').textContent=['OUR ROOTS','MEET REVENGER','TWIST & RESET','YOUR REFRESHING MOMENT','FIND YOUR EVERYDAY'][index];
    stage.querySelector('.chapter-number').textContent=String(index+1).padStart(2,'0');
    stage.querySelectorAll('.story-steps span').forEach((step,i)=>step.classList.toggle('active',i===index));
  }
  stage.style.setProperty('--story-progress',p);
  stage.querySelector('.story-progress').setAttribute('aria-valuenow',String(Math.round(p*100)));
}

function render(now=0) {
  frame=0;
  const dt=Math.min((now-lastTime)/1000||1/60,.05);lastTime=now;
  const still=reduced.matches||paused;
  if(!paused)current=still?target:current+(target-current)*(1-Math.exp(-dt*11));
  if(Math.abs(target-current)<.00015&&!paused)current=target;
  const p=current;
  timeline.progress(p);
  const open=state.open,tilt=state.tilt,flow=state.flow;
  updateText(p);
  // Progressive enhancement retains the approved photographic fallback.
  stage.style.setProperty('--cap-lift',`${open*90}px`);
  stage.style.setProperty('--bottle-tilt',`${-9+tilt*72}deg`);
  stage.dataset.progress=p.toFixed(4);
  stage.dataset.cap=open.toFixed(4);
  stage.dataset.flow=flow.toFixed(4);
  stage.style.setProperty('--paper',state.paper);
  stage.style.setProperty('--roots-visibility',state.roots);
  stage.dataset.scene=state.paper>.55?'light':'dark';
  if(renderer) {
    const fov=36-state.zoom*2;
    if(Math.abs(camera.fov-fov)>.001){camera.fov=fov;camera.updateProjectionMatrix();}
    const halfWidth=Math.tan(camera.fov*Math.PI/360)*camera.position.z*camera.aspect;
    const desktopX=Math.min(2.1,1.65*camera.aspect/1.44)+tilt*.2;
    const desktopFit=Math.min(.84,(halfWidth-.2-desktopX)/2.42);
    const mobileFit=Math.min(1,camera.aspect/.46);
    let scale=mobile?(.73-tilt*.17)*(1-tilt*(1-mobileFit)):1-tilt*(1-desktopFit);
    scale+=state.zoom*(mobile?.05:.055);
    let x=mobile?.08-tilt*.07:desktopX;
    let y=mobile?-.72+tilt*.57:tilt*.65;
    y-=state.zoom*(mobile?.35:.65);
    const lineupFit=mobile?mobileFit:Math.min(1,camera.aspect/1.44);
    const lineupScale=(mobile?.30:.50)*lineupFit;
    x=THREE.MathUtils.lerp(x,(mobile?-.28:1.55)*lineupFit,state.lineup);
    y=THREE.MathUtils.lerp(y,(mobile?-2.35:-2.20)+lineupScale*2.35,state.lineup);
    scale=THREE.MathUtils.lerp(scale,lineupScale,state.lineup)*state.arrival;
    model.bottle.visible=state.arrival>.002;
    model.bottle.scale.setScalar(Math.max(.0001,scale));
    model.bottle.position.set(x,y-(1-state.arrival)*4,0);
    model.bottle.rotation.set(.025+(still?0:pointerY*.018),state.turn+(still?0:pointerX*.045),-.10*(1-state.lineup)+tilt*1.25);
    model.liquid.scale.y=1-state.fill*.06;
    model.bottle.updateWorldMatrix(true,true);
    capClosed.set(0,2.305,0);model.bottle.localToWorld(capClosed);
    capAnchor.set(mobile?.80:2.15,mobile?1.30:2.55,.08);
    model.cap.visible=state.arrival>.002;
    model.cap.position.copy(capClosed).lerp(capAnchor,open);
    model.cap.scale.setScalar(THREE.MathUtils.lerp(scale,mobile?.73:.90,open));
    model.cap.rotation.set(model.bottle.rotation.x*(1-open),model.bottle.rotation.y*(1-open)-open*Math.PI*3.5,model.bottle.rotation.z*(1-open)-open*.12);
    mouth.set(0,2.355,.01);model.bottle.localToWorld(mouth);
    if(!still)flowTime+=dt;
    water.update(mouth,state,flowTime,mobile);
    world.update(state,p,camera,mobile,model.bottle.position);
    camera.position.x=still?0:pointerX*.02;
    camera.position.y=still?0:pointerY*.02;
    camera.lookAt(0,0,0);
    renderer.render(scene,camera);
    if(!stage.classList.contains('is-webgl-ready'))stage.classList.add('is-webgl-ready');
  }
  if(inView&&!still&&(Math.abs(target-current)>.00015||flow>.005))requestFrame();
}

try {
  renderer=new THREE.WebGLRenderer({alpha:true,antialias:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
  renderer.setClearColor(0x063b2e,0);
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.1;
  renderer.domElement.setAttribute('aria-label','Scroll-controlled 3D Revenger bottle, opening cap and pouring water');
  renderer.domElement.setAttribute('role','img');
  mount.append(renderer.domElement);
  scene=new THREE.Scene();scene.background=new THREE.Color(0x06392e);
  camera=new THREE.PerspectiveCamera(36,1,.1,60);camera.position.z=10.2;
  const pmrem=new THREE.PMREMGenerator(renderer);
  const room=new RoomEnvironment();
  const env=pmrem.fromScene(room,.04).texture;
  room.dispose();pmrem.dispose();
  scene.environment=env;
  scene.add(new THREE.HemisphereLight(0xf5ffef,0x174f3e,1.1));
  const key=new THREE.DirectionalLight(0xfff9df,2.7);key.position.set(-3,5,6);scene.add(key);
  const rim=new THREE.DirectionalLight(0xb5f5ee,3.2);rim.position.set(5,1,-3);scene.add(rim);
  model=makeBottle(env);scene.add(model.bottle);
  model.bottle.remove(model.cap);scene.add(model.cap);
  water=makeWater(scene,env);
  world=createBrandWorld(scene,env,model.bottle,model.cap);
  stage.dataset.renderer='webgl';
  // Texture callbacks request a new frame without an always-running idle loop.
  THREE.DefaultLoadingManager.onLoad=requestFrame;
  renderer.domElement.addEventListener('webglcontextlost',event=>{event.preventDefault();stage.classList.remove('is-webgl-ready');stage.dataset.renderer='fallback';cancelAnimationFrame(frame);frame=0;renderer=null;});
}catch(error){
  renderer=null;stage.dataset.renderer='fallback';
  console.info('Revenger: photographic scroll experience active; WebGL unavailable.');
}

new ResizeObserver(measure).observe(stage);
addEventListener('scroll',onScroll,{passive:true});
addEventListener('resize',measure,{passive:true});
if(matchMedia('(pointer:fine)').matches){
  stage.addEventListener('pointermove',event=>{pointerX=(event.clientX/innerWidth-.5)*2;pointerY=(event.clientY/innerHeight-.5)*2;requestFrame();},{passive:true});
  stage.addEventListener('pointerleave',()=>{pointerX=0;pointerY=0;requestFrame();});
}
document.addEventListener('revenger:motion',()=>{paused=document.body.classList.contains('motion-paused');if(!paused)lastTime=0;requestFrame();});
document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;}else{lastTime=0;onScroll();}});
reduced.addEventListener('change',()=>{current=0;measure();});
measure();
