Three.js 0.186.1, copied from the official npm `three` package.

- Upstream: https://github.com/mrdoob/three.js
- License: MIT, included as `LICENSE`
- Vendored files: `build/three.module.js`, `build/three.core.js`, `examples/jsm/environments/RoomEnvironment.js`
- Documentation: https://threejs.org/docs/pages/MeshPhysicalMaterial.html and https://threejs.org/docs/pages/LatheGeometry.html

The two build files retain their original contents. RoomEnvironment imports the local `three` import-map entry. Runtime rendering and user interactions are implemented in the adjacent project modules, not in vendored code.
