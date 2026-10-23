import * as THREE from './vendor/three/three.module.js';

const rad = Math.PI / 180;
const clamp = THREE.MathUtils.clamp;
const spherePoint = (lat, lon, radius = 1) => new THREE.Vector3(
  radius * Math.cos(lat * rad) * Math.sin(lon * rad),
  radius * Math.sin(lat * rad),
  radius * Math.cos(lat * rad) * Math.cos(lon * rad)
);
const geometry = points => new THREE.BufferGeometry().setFromPoints(points);

export async function mountServiceGlobe(section) {
  const root = section.querySelector('.service-globe');
  if (root.dataset.mounted) return;
  root.dataset.mounted = 'true';
  const viewport = root.querySelector('.globe-viewport');
  const label = root.querySelector('.globe-city-label');
  const pause = root.querySelector('.globe-pause');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const cities = [...section.querySelectorAll('.service-city')].map(button => ({
    button, city: button.dataset.city, state: button.dataset.state,
    lat: Number(button.dataset.lat), lon: Number(button.dataset.lon),
    point: spherePoint(Number(button.dataset.lat), Number(button.dataset.lon), 1.065),
    screen: new THREE.Vector3(), visible: false
  }));
  let selected = cities.findIndex(city => city.city === root.dataset.selected), hovered = -1;
  let renderer, scene, camera, globe, pulses;
  let frame = 0, last = 0, visible = false, paused = false, gesture = null;
  let elapsed = 0, yaw = -79 * rad, pitch = 23 * rad, targetYaw = yaw, targetPitch = pitch;
  let auto = true, width = 1, height = 1;
  const world = new THREE.Vector3();
  const forward = new THREE.Vector3(0, 0, 1);

  function requestFrame() { if (renderer && !frame && !document.hidden) frame = requestAnimationFrame(render); }
  function select(index, focus = true) {
    selected = index; hovered = -1;
    const city = cities[index];
    root.dataset.selected = city.city;
    cities.forEach((item, i) => item.button.setAttribute('aria-pressed', String(i === index)));
    root.querySelector('.globe-selected-city').textContent = city.city;
    root.querySelector('.globe-selected-state').textContent = city.state;
    root.querySelector('.globe-enquire').href = '/contact?city=' + encodeURIComponent(city.city);
    label.textContent = city.city;
    if (focus) {
      const desired = -city.lon * rad;
      targetYaw = yaw + Math.atan2(Math.sin(desired - yaw), Math.cos(desired - yaw));
      targetPitch = city.lat * rad;
      auto = true; elapsed = 0;
    }
    requestFrame();
  }
  cities.forEach((city, i) => city.button.addEventListener('click', () => select(i)));
  // Keep city selection/enquiries available even when WebGL or map data fails.
  select(selected, false);

  try {
    const response = await fetch('/static/data/globe-land.json');
    if (!response.ok) throw new Error('Globe geography unavailable');
    const land = await response.json();
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'low-power' });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
    renderer.setClearColor(0x000000, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    const canvas = renderer.domElement;
    canvas.tabIndex = 0;
    canvas.setAttribute('role', 'group');
    canvas.setAttribute('aria-label', 'Service globe. Drag to rotate, use arrow keys to explore, Home to return to India. Choose a city with the city buttons.');
    canvas.setAttribute('aria-keyshortcuts', 'ArrowLeft ArrowRight ArrowUp ArrowDown Home');
    viewport.append(canvas);
    scene = new THREE.Scene();
    camera = new THREE.OrthographicCamera(-1.24, 1.24, 1.24, -1.24, .1, 10);
    camera.position.z = 4;
    globe = new THREE.Group(); scene.add(globe);
    globe.add(new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshPhongMaterial({
      color: 0x0a4536, emissive: 0x031e18, specular: 0x376c4e, shininess: 18
    })));
    scene.add(new THREE.AmbientLight(0xe4f1d5, 1.2));
    const light = new THREE.DirectionalLight(0xe4f6ce, 2.2); light.position.set(-3, 4, 5); scene.add(light);
    const rim = new THREE.DirectionalLight(0x338c7d, 1.5); rim.position.set(3, -1, -2); scene.add(rim);
    const dots = [];
    for (let i = 0; i < land.dots.length; i += 2) dots.push(spherePoint(land.dots[i + 1], land.dots[i], 1.007));
    globe.add(new THREE.Points(geometry(dots), new THREE.PointsMaterial({ color: 0xb8cba2, size: 1.6, sizeAttenuation: false })));
    const coast = [];
    land.coasts.forEach(line => {
      for (let i = 0; i < line.length - 2; i += 2) coast.push(spherePoint(line[i + 1], line[i], 1.008), spherePoint(line[i + 3], line[i + 2], 1.008));
    });
    globe.add(new THREE.LineSegments(geometry(coast), new THREE.LineBasicMaterial({ color: 0x8eb28d, transparent: true, opacity: .35 })));
    const grid = [];
    for (let lat = -75; lat <= 75; lat += 15) for (let lon = -180; lon < 180; lon += 3) grid.push(spherePoint(lat, lon, 1.003), spherePoint(lat, lon + 3, 1.003));
    for (let lon = -180; lon < 180; lon += 20) for (let lat = -90; lat < 90; lat += 3) grid.push(spherePoint(lat, lon, 1.003), spherePoint(lat + 3, lon, 1.003));
    globe.add(new THREE.LineSegments(geometry(grid), new THREE.LineBasicMaterial({ color: 0x86af8e, transparent: true, opacity: .13 })));
    const pinGeometry = new THREE.SphereGeometry(.011, 10, 8);
    const pinMaterial = new THREE.MeshBasicMaterial({ color: 0xf1ce70 });
    cities.forEach(city => {
      city.pin = new THREE.Mesh(pinGeometry, pinMaterial);
      city.pin.position.copy(city.point); globe.add(city.pin);
      globe.add(new THREE.Line(geometry([spherePoint(city.lat, city.lon, 1.012), city.point]), new THREE.LineBasicMaterial({ color: 0xe3c96e, transparent: true, opacity: .8 })));
    });
    // One curved connection joins our two states; it does not imply worldwide supply.
    const a = cities[0].point.clone().normalize(), b = cities[3].point.clone().normalize();
    const arc = [];
    for (let i = 0; i <= 40; i++) arc.push(a.clone().lerp(b, i / 40).normalize().multiplyScalar(1.02 + Math.sin(i / 40 * Math.PI) * .09));
    globe.add(new THREE.Line(geometry(arc), new THREE.LineBasicMaterial({ color: 0xe7c96f, transparent: true, opacity: .55 })));
    pulses = [0, 1].map(() => {
      const ring = new THREE.Mesh(new THREE.RingGeometry(.024, .027, 48), new THREE.MeshBasicMaterial({ color: 0xe8d187, transparent: true, opacity: .7, side: THREE.DoubleSide, depthWrite: false }));
      globe.add(ring); return ring;
    });

    function measure() {
      width = viewport.clientWidth; height = viewport.clientHeight;
      const aspect = width / Math.max(1, height);
      camera.left = -1.24 * Math.max(1, aspect); camera.right = -camera.left;
      camera.top = 1.24 * Math.max(1, 1 / aspect); camera.bottom = -camera.top;
      camera.updateProjectionMatrix(); renderer.setSize(width, height, false); requestFrame();
    }
    new ResizeObserver(measure).observe(viewport);
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      if (visible) { last = 0; requestFrame(); }
      else { cancelAnimationFrame(frame); frame = 0; root.dataset.motion = 'offscreen'; }
    }).observe(viewport);
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) { cancelAnimationFrame(frame); frame = 0; }
      else { last = 0; if (visible) requestFrame(); }
    });
    function syncMotion() {
      pause.disabled = reduce.matches;
      pause.setAttribute('aria-pressed', String(paused || reduce.matches));
      pause.setAttribute('aria-label', reduce.matches ? 'Globe motion reduced' : paused ? 'Resume globe motion' : 'Pause globe motion');
      pause.textContent = reduce.matches ? 'Motion off' : paused ? 'Play \u25b7' : 'Pause \u2161';
      requestFrame();
    }
    pause.addEventListener('click', () => {
      paused = !paused;
      if (paused) { targetYaw = yaw; targetPitch = pitch; }
      elapsed = 0; syncMotion();
    });
    reduce.addEventListener('change', syncMotion);
    function reset() {
      targetYaw = yaw + Math.atan2(Math.sin(-79 * rad - yaw), Math.cos(-79 * rad - yaw));
      targetPitch = 23 * rad; auto = true; elapsed = 0; requestFrame();
    }
    root.querySelector('.globe-reset').addEventListener('click', reset);
    function nearest(event) {
      const box = canvas.getBoundingClientRect();
      let index = -1, distance = 22;
      cities.forEach((city, i) => {
        const delta = Math.hypot(event.clientX - box.left - city.screen.x, event.clientY - box.top - city.screen.y);
        if (city.visible && delta < distance) { distance = delta; index = i; }
      });
      return index;
    }
    canvas.addEventListener('contextmenu', event => event.preventDefault());
    canvas.addEventListener('pointerdown', event => {
      if (gesture || ![0, 2].includes(event.button)) return;
      gesture = { id: event.pointerId, x: event.clientX, y: event.clientY, yaw: targetYaw, pitch: targetPitch, touch: event.pointerType === 'touch', dragging: false, vertical: false };
      if (!gesture.touch) canvas.focus({ preventScroll: true });
    });
    canvas.addEventListener('pointermove', event => {
      if (!gesture) { hovered = nearest(event); canvas.style.cursor = hovered >= 0 ? 'pointer' : ''; requestFrame(); return; }
      if (event.pointerId !== gesture.id || gesture.vertical) return;
      const dx = event.clientX - gesture.x, dy = event.clientY - gesture.y;
      if (!gesture.dragging) {
        if (Math.max(Math.abs(dx), Math.abs(dy)) < 8) return;
        if (gesture.touch && Math.abs(dy) > Math.abs(dx)) { gesture.vertical = true; return; }
        gesture.dragging = true; auto = false; hovered = -1;
        canvas.setPointerCapture(event.pointerId); canvas.classList.add('is-dragging');
      }
      targetYaw = gesture.yaw + dx * .008;
      targetPitch = clamp(gesture.pitch + (gesture.touch ? 0 : dy * .006), -1.15, 1.15);
      requestFrame();
    });
    function release(event) {
      if (!gesture || event.pointerId !== gesture.id) return;
      const click = event.type === 'pointerup' && !gesture.dragging && !gesture.vertical;
      if (canvas.hasPointerCapture(event.pointerId)) canvas.releasePointerCapture(event.pointerId);
      gesture = null; canvas.classList.remove('is-dragging');
      if (click) { const index = nearest(event); if (index >= 0) select(index); }
      requestFrame();
    }
    canvas.addEventListener('pointerup', release); canvas.addEventListener('pointercancel', release);
    canvas.addEventListener('lostpointercapture', () => { gesture = null; canvas.classList.remove('is-dragging'); });
    canvas.addEventListener('pointerleave', () => { hovered = -1; if (gesture && !gesture.dragging) gesture = null; requestFrame(); });
    canvas.addEventListener('keydown', event => {
      if (event.key === 'Home') { event.preventDefault(); reset(); return; }
      if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) return;
      event.preventDefault(); auto = false;
      targetYaw += event.key === 'ArrowLeft' ? -.15 : event.key === 'ArrowRight' ? .15 : 0;
      targetPitch = clamp(targetPitch + (event.key === 'ArrowUp' ? -.12 : event.key === 'ArrowDown' ? .12 : 0), -1.15, 1.15);
      requestFrame();
    });
    canvas.addEventListener('webglcontextlost', event => {
      event.preventDefault(); cancelAnimationFrame(frame); frame = 0;
      root.dataset.renderer = 'fallback'; root.querySelector('.globe-toolbar').hidden = true;
      label.style.opacity = '0'; canvas.hidden = true; renderer = null;
    });
    root.querySelector('.globe-toolbar').hidden = false;
    root.dataset.renderer = 'webgl'; root.dataset.points = String(cities.length);
    measure(); syncMotion();
  } catch (error) {
    renderer?.dispose(); renderer = null; root.dataset.renderer = 'fallback';
  }

  function render(time) {
    frame = 0;
    if (!renderer || document.hidden) return;
    const dt = last ? Math.min((time - last) / 1000, .05) : .016; last = time;
    const moving = !paused && !reduce.matches && !gesture;
    if (moving) elapsed += dt;
    const desiredYaw = targetYaw + (moving && auto ? Math.sin(elapsed * .32) * .14 : 0);
    const blend = reduce.matches ? 1 : 1 - Math.exp(-dt * 7);
    yaw += (desiredYaw - yaw) * blend; pitch += (targetPitch - pitch) * blend;
    globe.rotation.set(pitch, yaw, 0); globe.updateMatrixWorld(true);
    camera.updateMatrixWorld();
    cities.forEach((city, i) => {
      world.copy(city.point).applyMatrix4(globe.matrixWorld);
      city.visible = world.z > .10;
      city.screen.copy(world).project(camera);
      city.screen.x = (city.screen.x + 1) * width / 2;
      city.screen.y = (1 - city.screen.y) * height / 2;
      city.pin.scale.setScalar(i === selected ? 1.6 : 1);
    });
    const active = cities[selected];
    pulses.forEach((ring, i) => {
      ring.position.copy(active.point);
      ring.quaternion.setFromUnitVectors(forward, world.copy(active.point).normalize());
      const phase = reduce.matches || paused ? i * .5 : (elapsed * .5 + i * .5) % 1;
      ring.scale.setScalar(1 + phase * 2); ring.material.opacity = (1 - phase) * .65;
    });
    const labelled = cities[hovered >= 0 ? hovered : selected];
    label.textContent = labelled.city;
    label.style.opacity = labelled.visible ? '1' : '0';
    label.style.transform = `translate(${clamp(labelled.screen.x + 22, 24, width - 120)}px,${clamp(labelled.screen.y - 28, 12, height - 45)}px)`;
    root.dataset.rotation = (yaw / rad).toFixed(2);
    root.dataset.pitch = (pitch / rad).toFixed(2);
    root.dataset.motion = !visible ? 'offscreen' : reduce.matches ? 'reduced' : paused ? 'paused' : 'running';
    renderer.render(scene, camera);
    const settling = Math.abs(desiredYaw - yaw) > .0001 || Math.abs(targetPitch - pitch) > .0001;
    if (visible && (moving || settling)) requestFrame();
  }
}
