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

## Product catalogue reference - 23 October 2026

- Bisleri product range: https://www.bisleri.com/products
- Product detail inspected: https://www.bisleri.com/bisleri-water-bottles/BISW-1LTR12-240.html

REA `capture_browser_scenario` opened the detail page in isolated headless Chrome at 1440 x 1000. Its accessibility capture showed bottle, label, case and rear-label image views, the product format, quantity decrement/increment controls and grouped footer links.

Evidence ID: `ev_148a267c3eef96218ddec499f6b26fa9b6ee2d852d014fed54a3adb9704e32a4`.

This was a read-only layout study; checkout and quantity interactions on Bisleri were not tested. The reference capture reported third-party script errors involving `$`, `initMap` and `initialised`. No reference code, product photography, logos or commercial terms were copied.

Revenger uses the general idea of clear product imagery, size information and quantity controls in its own emerald/gold design. The client requested no prices, so no pricing or cart flow is displayed. Water-format and beverage enquiry controls carry the chosen product, preferred size where applicable, and bottle quantity to the contact composer. New product concept artwork is documented in `ASSETS.md`.

## Service globe geography - 23 October 2026

- Land/coastlines: Natural Earth, `ne_110m_land.geojson` from the publisher-maintained repository: https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_land.geojson
- Natural Earth public-domain terms: https://www.naturalearthdata.com/about/terms-of-use/
- Approximate city centres: GeoNames `cities1000` daily extract, https://download.geonames.org/export/dump/cities1000.zip ; Creative Commons Attribution 4.0: https://creativecommons.org/licenses/by/4.0/ ; source licence notice: https://download.geonames.org/export/dump/readme.txt
- Three.js camera documentation: https://threejs.org/docs/#OrthographicCamera

The map uses geographic land shapes without political boundaries. `tools/build_globe_data.py` prepares 6,083 land dots, 128 coastline paths and a code-native SVG fallback; it does not generate or alter raster images. `public/static/data/globe-land.json` is served locally. GeoNames attribution is visible beside the globe, with Natural Earth credited as well.

Only the client's ten service cities are plotted. `CITY_CENTRES` in `content.py` records latitude, longitude and the GeoNames feature ID for each. Chitrakoot uses the Uttar Pradesh city centre named Chitrakoot Dham in the source; the other cities are matched within Maharashtra or Uttar Pradesh to avoid namesakes. These are approximate city centres, not new office or factory locations. The connecting arc illustrates the two service states and does not imply worldwide coverage.
