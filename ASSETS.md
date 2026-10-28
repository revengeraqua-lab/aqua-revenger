# Photorealistic asset update

Generated with the built-in `image_gen` tool, then copied into this workspace. Original files remain in the Codex generated-images directory. Alpha transparency is preserved. No image editing or background removal scripts were used. The bottle and cap use independently clipped copies of the same transparent asset; the splash uses separate foreground and background layers.

These are generated brand concept visuals, not photographs of an existing manufactured bottle or a verified water source.

## Final asset paths and prompt set

### `static/images/revenger-bottle-real.png`

Use case: product-mockup. Create a photorealistic premium commercial product photograph asset for Revenger packaged drinking water website, TRANSPARENT BACKGROUND. Portrait canvas about 2:3. One realistic clear 500 ml PET mineral water bottle centered, upright frontal view, uncapped, filled with crystal clear water, convincing optical refraction, clear molded ridged plastic shoulders and lower body, five-lobed PET bottle base, tiny realistic condensation beads and subtle waterline, crisp studio specular highlights, deep emerald green wraparound printed label with fine metallic gold trim and ivory italic serif wordmark EXACT TEXT 'Revenger', smaller 'PACKAGED DRINKING WATER', subtle two-leaf gold emblem. White stripbox reflections with dark emerald edges; believable mass-produced premium water bottle photograph, NOT drawing, NOT vector, NOT illustration, NOT opaque frosted glass, NOT cartoon, not exaggerated glowing edges. Bottle body should occupy x approximately 24%-76% of canvas and y 20%-96%; leave 4% bottom margin. The cap is a SEPARATE OBJECT floating DIRECTLY ABOVE the bottle's open threaded neck, aligned on the same vertical centerline: emerald green realistic ribbed screw cap, photographed matching bottle lighting, cap occupies roughly x 41%-59%, y 5%-12%. Clear transparent gap between cap and open neck from y12%-20%. No splash, no scenery, no shadow plane, no extra bottles. Both the separate cap and bottle are fully contained, isolated with genuine transparent alpha. This exact layout allows splitting the photograph into independently animated cap and bottle layers using CSS. Make it look like a real professional beverage advertising photograph.

### `static/images/water-splash-real.png`

Use case: ads-marketing. High speed macro studio PHOTOGRAPH of one dramatic crystal clear water splash isolated on a genuinely transparent background. Wide horizontal composition roughly 3:2. A broad irregular crescent ribbon of clear liquid sweeps from lower left across center bottom and rises on right with twisting thin sheets, lace-like edges, tiny airborne droplets frozen in motion, realistic fluid surface tension, clear optical refraction and bright silver white specular highlights with subtle emerald tint. The splash is open at center top, has empty transparent area above center to place a product bottle. Bottom crescent trough at y65%, side arms reaching y30%, loose droplets reaching y12%. Luxury bottled water advertising photography with dark-field rim lighting. Entire splash and every drop fully inside canvas, lots of transparent space around edges. NO bottle NO glass NO text NO background NO opaque solid base NO cartoon NO illustration NO perfect geometric ring NO concentric circles. Real water with organic irregular shapes, captured at 1/10000 second, spectacular yet physically plausible.

### `static/images/forest-stream.png`

Use case: ads-marketing. A cinematic editorial landscape photograph for premium emerald-green bottled water brand Revenger, portrait 4:5 composition. Low camera almost at the surface of a beautiful crystal clear flowing forest stream, detailed glassy transparent ripples over smooth dark stones in foreground, lush deep green trees and mossy banks, distant soft mountain silhouette in background, gentle early morning sunlight entering from upper right through thin mist, subtle warm golden reflections, photorealistic natural details and restrained premium color grading, rich forest green palette. Quiet elegant feeling, no people, no bottles, no packaging, no text, no buildings. This is atmospheric brand imagery, not a particular real geographic location. Avoid illustration, cartoon, excessive HDR, artificial neon colors. Real professional landscape photography.


## Cinematic water opening — 23 October 2026

- Asset: `public/static/images/hero-water.png` (1931 × 814).
- Generated with the built-in imagegen tool, then copied into the project. Not an image of an actual water source or facility.
- Final prompt: “Create a photorealistic premium water brand website hero BACKGROUND PHOTO ONLY, cinematic widescreen landscape 16:9 or wider. Extreme close-up of a pristine deep emerald and jade water surface, looking at a shallow grazing angle across sculptural soft ripples, elegant fine golden-white sunlight caustics on the right, rich dark forest green shadows on the left and bottom. Abstract real liquid, photographed with a high-end macro lens, tactile transparent moving water, delicate tiny highlights, visually calm but powerful, sophisticated luxury beverage campaign. Water must fill entire frame edge-to-edge. The left 55% is very dark quiet negative space for white typography, luminous water folds and reflections mainly in the right 45%, long rippling lines stretching diagonally. Color palette deep emerald #073d30, jade, pale champagne reflections; atmospheric depth. NO text, NO words, NO logo, NO bottle, NO glass, NO frame, NO landscape, NO mountains, NO forest, NO sky, NO added objects. This is editorial brand mood artwork, not a claim of a real water source.”
- Usage: CSS photographic fallback and a Three.js background plane with subtle UV refraction. The initial screen uses only the navigation wordmark, with no repeated hero wordmark or giant droplet.


## Leaf emblem and rear packaging — 23 October 2026

`public/static/images/leaf-mark.svg` is a code-native vector interpretation of the gold leaf emblem on the existing bottle artwork, used before the Revenger name. The existing bottle photograph is UV-mapped onto complementary front/rear label surfaces and front/rear PET detail meshes for 360-degree inspection. No new product specifications or regulatory panel are implied.


## Client-supplied leadership portraits — 23 October 2026

- `public/static/images/subir-banerjee.jpeg`: Subir Banerjee, Managing Director, 1067 × 1474.
- `public/static/images/rakesh-salve.jpeg`: Rakesh Salve, Chief Executive Officer, 1219 × 1290.

Supplied and identified by the client for publication on the company page. Original JPEG files are used without image alteration. CSS preserves each portrait's original aspect ratio; names, roles and descriptive alt text accompany the photographs.

## Geographic globe assets - 23 October 2026

`public/static/data/globe-land.json` and `public/static/images/service-globe.svg` are deterministic, code-native geographic assets prepared by `tools/build_globe_data.py` from Natural Earth's public-domain land dataset. No image generation was used for these assets. The SVG is the static fallback for the interactive Three.js globe. Approximate service-city centres come from GeoNames (CC BY 4.0); attribution is displayed alongside the globe. Source details are in `REFERENCES.md`.

## Product catalogue artwork - 23 October 2026

- Final file: `public/static/images/revenger-drinks-collection.png` (1536 x 1024 RGBA).
- Generated with the built-in imagegen tool, using `public/static/images/revenger-bottle-real.png` as the packaging-style reference.
- Original: `C:/Users/Dipanshu pandey/.codex/generated_images/01a14edf-f7ed-7892-910a-03c38f08fa29/exec-83dab881-d03c-4498-b1b4-207cc7bc6d32.png`.
- Copied without pixel editing. Four equally spaced bottle panels are displayed individually with CSS. Water-card sizing is illustrative; no prices or capacity claims are printed in the generated artwork. These are brand concepts, not verified manufactured-package photographs. The catalogue states that the company confirms current packaging, formats and availability.

Final prompt:

> Create a photorealistic product artwork sprite sheet for the Revenger beverages brand, using the attached bottle only as brand/packaging style reference. Wide landscape canvas 3:2 or 2:1. Exactly FOUR standalone complete CLOSED bottles arranged in four equally wide columns: column1 center x12.5% clear packaged drinking WATER, deep emerald green cap and emerald gold-trim label; column2 x37.5% crystal-clear carbonated SODA, muted silver gray cap and emerald/silver gold-trim label; column3 x62.5% light warm amber JEERA SODA, brown cap and dark amber/emerald gold-trim label with a small cumin botanical motif; column4 x87.5% very pale lemon yellow LEMON SODA, yellow cap and emerald/citrus gold-trim label with a small lemon illustration. All bottles exactly same tall slender realistic ribbed PET silhouette, SAME height and base alignment, front facing, evenly isolated. Each bottle must fit completely inside its own column with generous empty gutters; caps at y10%, bottoms at y92%, no overlap, no floating caps. Each label contains the same gold two-leaf emblem, exact large ivory italic word 'Revenger', and only the appropriate product name: 'PACKAGED DRINKING WATER', 'SODA', 'JEERA SODA', 'LEMON SODA'. Do not print any size, price, capacity, certification, barcode, nutrition or health claim. Realistic clear plastic optical reflections, fine condensation, elegant studio softbox illumination, commercial beverage product photograph quality, consistent emerald and gold premium brand family. Genuine TRANSPARENT background around every bottle. No scenery, no hands, no glasses, no fruit outside bottles, no large splash, no typography outside labels, no pedestal, no cast floor shadow. Important all 4 bottles must be separate and wholly within their equal quarter of the image so each column can be displayed individually on a website without altering pixels.

## Client-supplied product packaging - 28 October 2026

The client supplied five approved package reference images. The built-in `image_gen` background-extraction workflow removed only the surrounding scenery/background and preserved each bottle as an isolated transparent product-card asset. These files replace the earlier four-column concept sprite in the live catalogue:

- `public/static/images/revenger-water-500ml.png` — 500 ml packaged drinking water.
- `public/static/images/revenger-water-1l.png` — 1 litre packaged drinking water.
- `public/static/images/revenger-soda-500ml.png` — 500 ml soda.
- `public/static/images/revenger-jeera-soda-500ml.png` — 500 ml jeera soda.
- `public/static/images/revenger-nimbu-soda-500ml.png` — 500 ml nimbu soda.

Final background-extraction prompt pattern: “Edit only the specified supplied reference image. Remove the background and ground effects to genuine transparent alpha. Preserve the full bottle, proportions, cap, liquid, molded PET body, label artwork and visible package text exactly. Do not redesign, redraw, reinterpret or relabel.”
