import * as THREE from 'three';

// Fit the complete model (including its release space) into a viewport-safe
// region. Projection accounts for perspective and the visitor's 360° turn.
export function createBottleFraming() {
  const corners=Array.from({length:8},()=>new THREE.Vector3());
  const point=new THREE.Vector3(),center=new THREE.Vector3(),destination=new THREE.Vector3();
  function bounds(bottle,width,height,top){
    bottle.updateWorldMatrix(true,true);
    let left=Infinity,right=-Infinity,upper=Infinity,bottom=-Infinity;
    for(let i=0;i<8;i++) {
      corners[i].set(i&1?.79:-.79,i&2?top:-2.43,i&4?.79:-.79);
      point.copy(corners[i]).applyMatrix4(bottle.matrixWorld).project(camera);
      const x=(point.x+1)*width/2,y=(1-point.y)*height/2;
      left=Math.min(left,x);right=Math.max(right,x);upper=Math.min(upper,y);bottom=Math.max(bottom,y);
    }
    return {left,right,top:upper,bottom};
  }
  let camera;
  return ({bottle,viewCamera,width,height,headerBottom,mobile,open})=>{
    camera=viewCamera;
    const rect={left:width*(mobile?.035:.53),right:width*(mobile?.965:.955),top:mobile?Math.max(headerBottom+24,height*.43):headerBottom+26,bottom:height*.925};
    // Include enough neck-axis headroom for both screw release and lift.
    const top=2.55+Math.min(open/.74,1)*.57;
    for(let i=0;i<4;i++) {
      const b=bounds(bottle,width,height,top);
      const fit=Math.min(1,(rect.right-rect.left)/(b.right-b.left),(rect.bottom-rect.top)/(b.bottom-b.top));
      if(fit<.999){bottle.scale.multiplyScalar(fit*.985);continue;}
      const dx=b.left<rect.left?rect.left-b.left:b.right>rect.right?rect.right-b.right:0;
      const dy=b.top<rect.top?rect.top-b.top:b.bottom>rect.bottom?rect.bottom-b.bottom:0;
      if(Math.abs(dx)+Math.abs(dy)<.1)break;
      center.copy(bottle.position).project(camera);
      destination.copy(center);destination.x+=dx*2/width;destination.y-=dy*2/height;
      center.unproject(camera);destination.unproject(camera);
      bottle.position.add(destination.sub(center));
    }
    return bounds(bottle,width,height,top);
  };
}
