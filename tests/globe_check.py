"""Real-browser checks for service-globe selection, input, lifecycle and fallback."""
import math
import sys
import threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from content import REGIONS
from playwright.sync_api import sync_playwright, expect
from werkzeug.serving import make_server


def verify(base):
    Path('test-results').mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', headless=True, args=['--enable-unsafe-swiftshader'])
        context = browser.new_context(viewport={'width': 1440, 'height': 1000})
        page = context.new_page(); errors = []; bad = []; requests = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('response', lambda r: bad.append((r.status, r.url)) if r.status >= 400 else None)
        page.on('request', lambda r: requests.append(r.url))
        page.goto(base+'/', wait_until='networkidle')
        assert not any('globe-land.json' in url for url in requests), 'Globe must load lazily'
        section = page.locator('.connections-section'); globe = section.locator('.service-globe')
        section.scroll_into_view_if_needed()
        expect(globe).to_have_attribute('data-renderer', 'webgl', timeout=30000)
        expect(globe).to_have_attribute('data-points', '10')
        expect(section.locator('.service-city')).to_have_count(10)
        expect(globe.locator('canvas')).to_be_visible()
        expect(globe.locator('.globe-pin:visible')).to_have_count(10)
        boxes=[node.bounding_box() for node in globe.locator('.globe-pin').all()]
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:assert not (a['x']<b['x']+b['width'] and a['x']+a['width']>b['x'] and a['y']<b['y']+b['height'] and a['y']+a['height']>b['y']),'Pin labels overlap'
        # The globe genuinely moves without user input.
        before = globe.get_attribute('data-rotation'); page.wait_for_timeout(700)
        assert before != globe.get_attribute('data-rotation')
        globe.get_by_role('button', name='Pause globe motion', exact=True).click()
        expect(globe).to_have_attribute('data-motion', 'paused')
        for state, cities in REGIONS.items():
            for city in cities:
                button = section.get_by_role('button', name=city, exact=True)
                button.click(); expect(button).to_have_attribute('aria-pressed', 'true')
                expect(globe.locator('.globe-selected-city')).to_have_text(city)
                expect(globe.locator('.globe-selected-state')).to_have_text(state)
                expect(globe.locator('.globe-enquire')).to_have_attribute('href', '/contact?city='+city)
        section.get_by_role('button', name='Prayagraj', exact=True).click()
        page.wait_for_timeout(1000)
        page.screenshot(path='test-results/globe-desktop.png')
        expect(globe.get_by_role('button',name='Show Prayagraj on globe')).to_have_attribute('aria-pressed','true')
        frozen = globe.get_attribute('data-rotation'); page.wait_for_timeout(500)
        assert frozen == globe.get_attribute('data-rotation'), 'Pause must freeze the globe'
        canvas = globe.locator('canvas'); box = canvas.bounding_box()
        original=canvas.screenshot()
        for _ in range(2):globe.get_by_role('button',name='Zoom in globe',exact=True).click()
        page.wait_for_function('Number(document.querySelector(".service-globe").dataset.zoom)>1.79')
        assert original!=canvas.screenshot(),'Zoom must change the rendered globe'
        canvas.focus();page.mouse.move(box['x']+box['width']*.5,box['y']+box['height']*.5);page.mouse.wheel(0,-160)
        page.wait_for_function('Number(document.querySelector(".service-globe").dataset.zoom)>2.2')
        canvas.press('-');page.wait_for_function('Number(document.querySelector(".service-globe").dataset.zoom)<2.2')
        for _ in range(10):
            if globe.get_by_role('button',name='Zoom in globe',exact=True).is_enabled():globe.get_by_role('button',name='Zoom in globe',exact=True).click()
        expect(globe.get_by_role('button',name='Zoom in globe',exact=True)).to_be_disabled()
        globe.get_by_role('button',name='Show all service locations',exact=True).click()
        page.wait_for_function('Number(document.querySelector(".service-globe").dataset.zoom)===1')
        expect(globe.locator('.globe-pin:visible')).to_have_count(10)
        globe.get_by_role('button',name='Show Palghar on globe').click()
        expect(globe).to_have_attribute('data-selected','Palghar')
        globe.get_by_role('button',name='Show all service locations',exact=True).click();page.wait_for_timeout(1000)
        box=canvas.bounding_box();frozen=globe.get_attribute('data-rotation')
        page.mouse.move(box['x']+box['width']*.45, box['y']+box['height']*.82)
        page.mouse.down(); page.mouse.move(box['x']+box['width']*.85, box['y']+box['height']*.82, steps=18); page.mouse.up()
        page.wait_for_timeout(1000)
        assert abs(float(globe.get_attribute('data-rotation'))-float(frozen)) > 40, 'Real mouse drag must rotate'
        canvas.focus(); canvas.press('ArrowLeft'); page.wait_for_timeout(500)
        expect(canvas).to_be_focused()
        canvas.press('Home'); page.wait_for_timeout(1200)
        assert abs(float(globe.get_attribute('data-rotation'))+79) < .1
        # Click the actual projected Mumbai point, rather than a mocked click handler.
        city = section.locator('[data-city="Mumbai"]')
        lat, lon = [float(city.get_attribute('data-'+k))*math.pi/180 for k in ['lat', 'lon']]
        yaw, pitch = [float(globe.get_attribute('data-'+k))*math.pi/180 for k in ['rotation', 'pitch']]
        x = 1.065*math.cos(lat)*math.sin(lon+yaw)
        y = 1.065*(math.sin(lat)*math.cos(pitch)-math.cos(lat)*math.cos(lon+yaw)*math.sin(pitch))
        canvas.click(position={'x': box['width']*(.5+x/2.48), 'y': box['height']*(.5-y/2.48)})
        expect(globe).to_have_attribute('data-selected', 'Mumbai')
        globe.locator('.globe-enquire').click()
        expect(page.locator('#enquiry-city')).to_have_value('Mumbai')
        # Responsive layout, real touch rotation and native vertical scrolling.
        mobile = browser.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
        m = mobile.new_page(); m.on('pageerror', lambda e: errors.append(str(e)))
        m.goto(base+'/', wait_until='networkidle'); m.locator('.connections-section').scroll_into_view_if_needed()
        mg = m.locator('.service-globe'); expect(mg).to_have_attribute('data-renderer', 'webgl', timeout=30000)
        m.locator('.service-city[data-city="Thane"]').click()
        expect(mg.locator('.globe-selected-city')).to_have_text('Thane')
        m.locator('.connection-visual').scroll_into_view_if_needed()
        for width in [320,390,768,1024,1440]:
            page.set_viewport_size({'width':width,'height':1000}); page.goto(base+'/',wait_until='networkidle')
            page.locator('.connections-section').scroll_into_view_if_needed()
            expect(page.locator('.service-globe')).to_have_attribute('data-renderer','webgl', timeout=30000)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), width
        session = mobile.new_cdp_session(m)
        b = mg.locator('canvas').bounding_box(); start = (b['x']+b['width']*.25, b['y']+b['height']*.5)
        # Real two-finger pinch, delivered as native touch events.
        cy=b['y']+b['height']*.5;cx=b['x']+b['width']*.5
        def fingers(distance):return [{'id':1,'x':cx-distance,'y':cy},{'id':2,'x':cx+distance,'y':cy}]
        session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':fingers(36)})
        for distance in range(40,76,4):session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':fingers(distance)})
        session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        m.wait_for_function('Number(document.querySelector(".service-globe").dataset.zoom)>1.5')
        mg.get_by_role('button',name='Show all service locations',exact=True).click()
        m.wait_for_function('Number(document.querySelector(".service-globe").dataset.zoom)===1')
        expect(mg.locator('.globe-pin:visible')).to_have_count(10)
        m.locator('.connection-visual').screenshot(path='test-results/globe-all-pins-mobile.png')
        b=mg.locator('canvas').bounding_box()
        start=(b['x']+b['width']*.45,b['y']+b['height']*.78)
        def swipe(dx,dy):
            session.send('Input.dispatchTouchEvent', {'type':'touchStart','touchPoints':[{'x':start[0],'y':start[1]}]})
            for n in range(1,13):
                session.send('Input.dispatchTouchEvent', {'type':'touchMove','touchPoints':[{'x':start[0]+dx*n/12,'y':start[1]+dy*n/12}]})
            session.send('Input.dispatchTouchEvent', {'type':'touchEnd','touchPoints':[]})
        angle = float(mg.get_attribute('data-rotation')); swipe(170,0); m.wait_for_timeout(900)
        assert abs(float(mg.get_attribute('data-rotation'))-angle)>30
        y_before = m.evaluate('scrollY'); swipe(0,-100); m.wait_for_timeout(500)
        assert m.evaluate('scrollY')>y_before+30, 'Vertical swipe must scroll the page'
        m.locator('.connection-visual').screenshot(path='test-results/globe-mobile.png')
        # Reduced-motion visitors get a still globe; offscreen work stops.
        page.emulate_media(reduced_motion='reduce'); page.locator('.connections-section').scroll_into_view_if_needed()
        g = page.locator('.service-globe'); expect(g).to_have_attribute('data-motion','reduced')
        fixed = g.get_attribute('data-rotation'); page.wait_for_timeout(600)
        assert fixed == g.get_attribute('data-rotation')
        page.locator('[data-city="Varanasi"]').click(); expect(g).to_have_attribute('data-selected','Varanasi')
        page.mouse.wheel(0,-30000)
        expect(g).to_have_attribute('data-motion','offscreen')
        fixed=g.get_attribute('data-rotation');page.wait_for_timeout(500)
        assert fixed==g.get_attribute('data-rotation'), 'Offscreen rendering must stop'
        # Independent context with WebGL disabled: static globe and city enquiries survive.
        fallback = browser.new_context(viewport={'width':1280,'height':900})
        fallback.add_init_script("const get=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return type.includes('webgl')?null:get.call(this,type,...args)}")
        f = fallback.new_page(); f.goto(base+'/',wait_until='networkidle'); f.locator('.connections-section').scroll_into_view_if_needed()
        f.wait_for_function('document.querySelector(".service-globe").dataset.mounted==="true"')
        f.locator('[data-city="Ayodhya"]').click()
        expect(f.locator('.service-globe')).to_have_attribute('data-renderer','fallback')
        expect(f.locator('.globe-selected-city')).to_have_text('Ayodhya')
        expect(f.locator('.globe-fallback')).to_be_visible()
        assert not errors, errors
        assert not bad, bad
        browser.close()
        print('PASS: 10 simultaneous readable pins, point/label/city selection, button/wheel/keyboard/pinch zoom, all-locations reset, city enquiry, mouse/touch rotation, native scrolling, 5 widths, pause/reduced motion, offscreen suspension and WebGL fallback.')


if __name__ == '__main__':
    if len(sys.argv)>1: verify(sys.argv[1].rstrip('/'))
    else:
        server=make_server('127.0.0.1',5002,create_app()); threading.Thread(target=server.serve_forever,daemon=True).start()
        try: verify('http://127.0.0.1:5002')
        finally: server.shutdown()
