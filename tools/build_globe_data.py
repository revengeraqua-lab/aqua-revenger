"""Prepare small, local globe geometry from Natural Earth's public-domain land.

python tools/build_globe_data.py .build/globe/land.geojson
No network calls or raster-image edits. Coastlines only, no political borders.
"""
import json
import math
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from content import CITY_CENTRES


def inside(lon, lat, ring):
    hit = False
    a = ring[-1]
    for b in ring:
        if (b[1] > lat) != (a[1] > lat) and lon < (a[0]-b[0])*(lat-b[1])/(a[1]-b[1])+b[0]:
            hit = not hit
        a = b
    return hit


def projected(lon, lat):
    lon, lat = math.radians(lon-79), math.radians(lat)
    pitch = math.radians(23)
    x, y, z = math.cos(lat)*math.sin(lon), math.sin(lat), math.cos(lat)*math.cos(lon)
    return 300+x*250, 300-(y*math.cos(pitch)-z*math.sin(pitch))*250, y*math.sin(pitch)+z*math.cos(pitch)


def build(source):
    features = json.loads(source.read_text(encoding='utf-8'))['features']
    polygons = []
    for feature in features:
        g = feature['geometry']
        polygons.extend([g['coordinates']] if g['type'] == 'Polygon' else g['coordinates'])
    bounded = [(p, (min(v[0] for v in p[0]), min(v[1] for v in p[0]), max(v[0] for v in p[0]), max(v[1] for v in p[0]))) for p in polygons]
    dots = []
    for step in range(1, 128):
        lat = -90+step*1.4
        count = max(1, round(360*math.cos(math.radians(lat))/1.4))
        for n in range(count):
            lon = -180+(n+.5)*360/count
            if any(b[0] <= lon <= b[2] and b[1] <= lat <= b[3] and inside(lon, lat, p[0]) and not any(inside(lon, lat, h) for h in p[1:]) for p, b in bounded):
                dots.extend([round(lon, 3), round(lat, 3)])
    coasts = []
    for polygon in polygons:
        for ring in polygon:
            line = []
            for a, b in zip(ring, ring[1:]):
                delta = (b[0]-a[0]+180) % 360-180
                steps = max(1, math.ceil(max(abs(delta), abs(b[1]-a[1]))/1.5))
                for n in range(steps):
                    line.extend([round(a[0]+delta*n/steps, 3), round(a[1]+(b[1]-a[1])*n/steps, 3)])
            line.extend(ring[-1])
            coasts.append(line)
    data = {'source': 'Natural Earth ne_110m_land, public domain', 'dots': dots, 'coasts': coasts}
    target = BASE/'public/static/data/globe-land.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(data, separators=(',', ':')), encoding='utf-8')
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><defs><radialGradient id="o" cx="35%" cy="28%"><stop stop-color="#246a50"/><stop offset="1" stop-color="#052e26"/></radialGradient></defs><circle cx="300" cy="300" r="250" fill="url(#o)"/>']
    for lon, lat in zip(dots[::2], dots[1::2]):
        x, y, z = projected(lon, lat)
        if z > 0:
            svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.2" fill="#b5ca9f" opacity=".7"/>')
    for lat, lon, _ in CITY_CENTRES.values():
        x, y, z = projected(lon, lat)
        if z > 0:
            svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#edce72"/>')
    svg.append('</svg>')
    (BASE/'public/static/images/service-globe.svg').write_text(''.join(svg), encoding='utf-8')
    print(f'Wrote {len(dots)//2} land dots, {len(coasts)} coastlines ({target.stat().st_size} bytes) and SVG fallback.')


if __name__ == '__main__':
    build(Path(sys.argv[1]))
