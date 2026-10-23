import * as THREE from 'three';

const phase=(p,a,b)=>{const t=THREE.MathUtils.clamp((p-a)/(b-a),0,1);return t*t*(3-2*t);};

// Keep screw rotation separate from orientation blending. Quaternion slerp
// alone takes the shortest path and cannot describe multiple unscrewing turns.
export function createCapMotion() {
  const axis=new THREE.Vector3(),closed=new THREE.Vector3(),lifted=new THREE.Vector3(),parked=new THREE.Vector3();
  const difference=new THREE.Vector3();
  const yAxis=new THREE.Vector3(0,1,0),spin=new THREE.Quaternion(),orientation=new THREE.Quaternion();
  const parkOrientation=new THREE.Quaternion().setFromEuler(new THREE.Euler(.08,0,-.12));
  return function update({bottle,cap,open,scale,mobile,camera,height,headerBottom}) {
    const screw=phase(open,0,.55),lift=phase(open,.55,.74),park=phase(open,.74,1);
    const rise=.30*screw+.27*lift;
    // Stay coaxial and at the bottle's scale until the threads are cleared.
    const capScale=THREE.MathUtils.lerp(scale,mobile?.73:.90,park);
    const radius=.40*capScale;
    const halfHeight=Math.tan(camera.fov*Math.PI/360)*(camera.position.z-.08);
    const safeTop=halfHeight*(1-2*(headerBottom+30)/height);
    bottle.updateWorldMatrix(true,true);
    axis.copy(yAxis).applyQuaternion(bottle.quaternion).normalize();
    closed.set(0,2.305,0);bottle.localToWorld(closed);
    lifted.copy(closed).addScaledVector(axis,rise*scale);
    // Reserve space for the axial release and the small departure arc too.
    const arc=Math.sin(park*Math.PI)*.08;
    const overflow=Math.max(0,lifted.y+radius+arc-safeTop);
    if(overflow>0) {
      bottle.position.y-=overflow;bottle.updateWorldMatrix(true,true);
      closed.set(0,2.305,0);bottle.localToWorld(closed);
      lifted.copy(closed).addScaledVector(axis,rise*scale);
    }
    const safeRight=halfHeight*camera.aspect-radius-.16;
    parked.set(Math.min(mobile?.80:2.15,safeRight),Math.min(mobile?1.30:2.55,safeTop-radius-arc),.08);
    cap.position.copy(lifted).lerp(parked,park);cap.position.y+=arc;
    cap.scale.setScalar(capScale);
    orientation.copy(bottle.quaternion).slerp(parkOrientation,park);
    spin.setFromAxisAngle(yAxis,-screw*Math.PI*3.5);
    cap.quaternion.copy(orientation).multiply(spin);
    return {screw,lift,park,rise,lateral:difference.copy(cap.position).sub(closed).cross(axis).length()};
  };
}
