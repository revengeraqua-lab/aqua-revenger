import * as THREE from 'three';

// The photograph's printed label is wrapped onto a real cylindrical mesh.
// Clear PET, molded ribs, threads, liquid, condensation and cap are geometry.
export function makeBottle(environment) {
  const bottle = new THREE.Group();
  const plastic = new THREE.MeshPhysicalMaterial({
    color: 0xffffff, roughness: .065, metalness: 0, transmission: 1,
    thickness: .035, ior: 1.46, clearcoat: .6, clearcoatRoughness: .045,
    envMap: environment, envMapIntensity: 1.2, side: THREE.FrontSide,
  });
  const emerald = new THREE.MeshStandardMaterial({color:0x075137,roughness:.29,metalness:.15,envMap:environment,envMapIntensity:1.1});
  const gold = new THREE.MeshStandardMaterial({color:0xd4bc70,roughness:.25,metalness:.8,envMap:environment});
  const points = [[.02,-2.28],[.45,-2.28],[.62,-2.23],[.69,-2.1]];
  for (let i=0;i<=96;i++) {
    const y=-2.08+i*3.34/96;
    let r=.694;
    if(y<-.77 || y>.69) r+=.022*Math.cos((y+2.05)*31)+.009*Math.sin(y*57);
    points.push([r,y]);
  }
  points.push([.68,1.32],[.64,1.44],[.55,1.61],[.42,1.79],[.29,1.94],[.25,2.05],[.25,2.34],[.217,2.34],[.217,2.05]);
  const shell=new THREE.Mesh(new THREE.LatheGeometry(points.map(([r,y])=>new THREE.Vector2(r,y)),96),plastic);
  shell.renderOrder=3;
  bottle.add(shell);
  // Project the approved product photograph onto the front surface of the
  // bottle mesh. Its fine wet-plastic detail bends with the actual geometry.
  const detailGeometry=new THREE.LatheGeometry(points.map(([r,y])=>new THREE.Vector2(r+.005,y)),96,-Math.PI/2,Math.PI);
  const positions=detailGeometry.attributes.position;
  const uv=detailGeometry.attributes.uv;
  for(let i=0;i<positions.count;i++) {
    const y=positions.getY(i);
    const v=y>.605 ? .600+(y-.605)/1.735*.283 : y<-.695 ? .373+(y+.695)/1.585*.343 : .373+(y+.695)/1.30*.227;
    uv.setXY(i,.5+positions.getX(i)*.285,v);
  }
  const detailTexture=new THREE.TextureLoader().load('/static/images/revenger-bottle-real.png');
  detailTexture.colorSpace=THREE.SRGBColorSpace;detailTexture.anisotropy=4;
  const detail=new THREE.Mesh(detailGeometry,new THREE.MeshBasicMaterial({map:detailTexture,transparent:true,opacity:.73,alphaTest:.02,depthWrite:false}));
  detail.renderOrder=5;bottle.add(detail);

  // The rounded PET foot and the five molded lobes catch the studio lights.
  for(let i=0;i<5;i++) {
    const foot=new THREE.Mesh(new THREE.SphereGeometry(.25,20,12),plastic);
    const a=i/5*Math.PI*2;
    foot.scale.set(1,.58,1);foot.position.set(Math.sin(a)*.39,-2.24,Math.cos(a)*.39);bottle.add(foot);
  }
  for(const y of [2.09,2.17,2.25,2.32]) {
    const thread=new THREE.Mesh(new THREE.TorusGeometry(.254,.018,8,64),plastic);
    thread.rotation.x=Math.PI/2;thread.position.y=y;bottle.add(thread);
  }
  const collar=new THREE.Mesh(new THREE.TorusGeometry(.28,.025,10,64),plastic);
  collar.rotation.x=Math.PI/2;collar.position.y=2.04;bottle.add(collar);

  const waterMaterial=new THREE.MeshPhysicalMaterial({color:0xffffff,transmission:1,roughness:.025,thickness:1.2,ior:1.333,attenuationColor:0xd7f3eb,attenuationDistance:10,envMap:environment,envMapIntensity:.65,side:THREE.FrontSide});
  const waterPoints=[[.01,-2.16],[.56,-2.16],[.65,-2.08],[.65,1.25],[.53,1.49],[.01,1.49]];
  const liquid=new THREE.Mesh(new THREE.LatheGeometry(waterPoints.map(([r,y])=>new THREE.Vector2(r,y)),64),waterMaterial);
  bottle.add(liquid);

  const labelBack=new THREE.Mesh(new THREE.CylinderGeometry(.719,.719,1.28,96,1,true),emerald);
  labelBack.position.y=-.045;bottle.add(labelBack);
  const labelTexture=new THREE.TextureLoader().load('/static/images/revenger-bottle-real.png');
  labelTexture.colorSpace=THREE.SRGBColorSpace;
  labelTexture.repeat.set(.397,.226);labelTexture.offset.set(.302,.374);
  labelTexture.anisotropy=4;
  const label=new THREE.Mesh(new THREE.CylinderGeometry(.724,.724,1.24,64,1,true,-1.22,2.44),new THREE.MeshStandardMaterial({map:labelTexture,roughness:.34,metalness:.12,envMap:environment,envMapIntensity:.75}));
  label.position.y=-.045;bottle.add(label);
  for(const y of [-.695,.605]) {
    const band=new THREE.Mesh(new THREE.CylinderGeometry(.723,.723,.022,96,1,true),gold);
    band.position.y=y;bottle.add(band);
  }

  const cap=new THREE.Group();
  const capBody=new THREE.Mesh(new THREE.CylinderGeometry(.289,.296,.32,64),emerald);
  cap.add(capBody);
  const capTop=new THREE.Mesh(new THREE.CylinderGeometry(.27,.287,.035,64),emerald);
  capTop.position.y=.169;cap.add(capTop);
  const ribGeometry=new THREE.BoxGeometry(.012,.245,.018);
  for(let i=0;i<52;i++) {
    const angle=i/52*Math.PI*2;
    const rib=new THREE.Mesh(ribGeometry,emerald);
    rib.position.set(Math.sin(angle)*.294,0,Math.cos(angle)*.294);
    rib.rotation.y=angle;cap.add(rib);
  }
  const seal=new THREE.Mesh(new THREE.CylinderGeometry(.3,.3,.045,64),emerald);
  seal.position.y=2.12;bottle.add(seal);
  cap.position.y=2.305;bottle.add(cap);

  const beads=new THREE.InstancedMesh(new THREE.SphereGeometry(1,8,6),plastic,74);
  const dummy=new THREE.Object3D();
  for(let i=0;i<74;i++) {
    const y=(i%2 ? -.9-(i%23)*.05 : .8+(i%19)*.031);
    const a=i*2.39996;
    const r=.725;
    dummy.position.set(Math.sin(a)*r,y,Math.cos(a)*r);
    const size=.012+((i*17)%23)/1300;
    dummy.scale.set(size,size*1.3,size*.7);dummy.updateMatrix();beads.setMatrixAt(i,dummy.matrix);
  }
  bottle.add(beads);
  return {bottle,cap,liquid,labelTexture};
}
