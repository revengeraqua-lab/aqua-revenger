# Revenger animation reference

## Selected reference

- Live experience: https://tabasco.hilostudiolab.com/
- Author's case study: https://hilostudiolab.com/en/projects/tabasco

The case study describes three visual chapters: peppers, aging barrels and the finished product range. It explains its use of scroll-driven 3D storytelling and coordinated typography. Revenger applies the general idea of distinct visual chapters to its own brand: parent company, brand introduction, opening ritual, a refreshing moment, and bottle formats.

## REA inspection

REA `capture_browser_scenario` opened the live reference in an isolated, headless Chrome session at 1440 × 1000 with reduced motion disabled. It captured the loading screen and the live pepper scene, accessibility output, and page-error events.

Evidence ID: `ev_7cad0c80efdd544842e8bc9eee344ae3a27b8f56762c66b34afab77ca772e11a`.

The capture completed without page errors. Keyboard PageDown did not establish the entire reference site's scroll choreography, so later chapter details above are attributed to the author's case study rather than inferred from those screenshots. No reference code, textures, models, branding or copy were downloaded into Revenger.

## Revenger implementation

- One paused GSAP timeline defines all five chapters.
- Native scroll seeks the same timeline forwards and backwards.
- Forest atmosphere dissolves into a light product studio, followed by a closer opening scene and a glass-pouring scene.
- World-space 3D coordinates connect bottle mouth, stream and glass; the final chapter reveals four bottle formats.
- Copy explicitly names GangaShree Roots Private Limited and introduces Revenger as packaged drinking water. The forest is atmospheric artwork, not a claim about the source of the water.

Local photographs/concept artwork remain documented in `ASSETS.md`. Three.js and GSAP are self-hosted under `static/vendor`, with their upstream notices retained.
