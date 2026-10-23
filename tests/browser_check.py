"""Verify the six-page portfolio in isolated Chrome; optional URL for live verification."""
import sys,tempfile,threading
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import create_app
from content import PAGES
from playwright.sync_api import sync_playwright,expect
from werkzeug.serving import make_server

def verify(base):
    output=Path('test-results');output.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,args=['--enable-unsafe-swiftshader'])
        page=browser.new_page(viewport={'width':1440,'height':1000})
        errors=[];bad=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
        page.goto(base+'/',wait_until='networkidle')
        stage=page.locator('.story-stage')
        expect(stage).to_have_attribute('data-renderer','webgl',timeout=30000)
        expect(stage.locator('canvas')).to_be_visible()
        assert abs(stage.bounding_box()['y']) < 1, 'Water must begin at the top of the screen'
        assert page.locator('.story-brand').count() == 0, 'No duplicate hero wordmark'
        assert page.locator('.topline').count() == 0, 'No strip above the immersive opening'
        assert page.locator('header').evaluate('e=>getComputedStyle(e).position') == 'fixed'
        assert page.locator('header').evaluate('e=>getComputedStyle(e).backgroundColor') == 'rgba(0, 0, 0, 0)'
        page.screenshot(path=str(output/'immersive-opening-desktop.png'))
        def seek(progress):
            d=page.locator('.scroll-story').evaluate('(e)=>({top:e.getBoundingClientRect().top+scrollY,distance:e.offsetHeight-document.querySelector(".story-stage").offsetHeight})')
            page.mouse.wheel(0,d['top']+d['distance']*progress-page.evaluate('scrollY'))
            page.wait_for_function('(p)=>Math.abs(Number(document.querySelector(".story-stage").dataset.progress)-p)<.002',arg=progress,timeout=15000)
        def assert_cap_visible():
            bounds=stage.evaluate('(e)=>({...e.dataset})')
            nav=page.locator('header').bounding_box()
            assert float(bounds['capTop']) >= nav['y']+nav['height']+8, bounds
            assert float(bounds['capLeft'])>=0 and float(bounds['capRight'])<=page.viewport_size['width'], bounds
            assert float(bounds['capBottom'])<page.viewport_size['height'], bounds
        for progress,chapter in [(.33,'2'),(.55,'3'),(.76,'4'),(.99,'5'),(0,'1')]:
            seek(progress)
            expect(stage).to_have_attribute('data-chapter',chapter)
            if chapter!='1':
                expect(page.locator('body')).to_have_class(__import__('re').compile('header-scrolled'))
            if chapter=='1':
                assert not page.locator('body').evaluate("e=>e.classList.contains('header-scrolled')")
            if chapter=='3':
                assert float(stage.get_attribute('data-cap'))>.99
                assert_cap_visible()
            if chapter=='4':
                assert float(stage.get_attribute('data-flow'))>.99
                assert abs(stage.bounding_box()['y'])<1
                assert_cap_visible()
                page.screenshot(path=str(output/'cinematic-pour.png'))
        # Verify a full turn with actual right-mouse drags, not a mocked angle.
        seek(.33)
        canvas=stage.locator('canvas')
        expect(stage.locator('.rotation-hint')).to_be_visible()
        page.get_by_role('button',name='Pause 3D animation').click()
        before=canvas.screenshot()
        for _ in range(2):
            page.mouse.move(820,520)
            page.mouse.down(button='right')
            page.mouse.move(1340,520,steps=20)
            page.mouse.up(button='right')
        page.wait_for_function('Math.abs(Number(document.querySelector(".story-stage").dataset.rotation))>360')
        assert before!=canvas.screenshot(), 'The rendered model must visibly rotate'
        expect(page.get_by_role('button',name='Reset view')).to_be_visible()
        assert_cap_visible()
        page.screenshot(path=str(output/'bottle-rotated.png'))
        page.get_by_role('button',name='Reset view').click()
        page.wait_for_function('Number(document.querySelector(".story-stage").dataset.rotation)===0')
        canvas.press('ArrowRight')
        page.wait_for_function('Number(document.querySelector(".story-stage").dataset.rotation)>0')
        canvas.press('Home')
        page.wait_for_function('Number(document.querySelector(".story-stage").dataset.rotation)===0')
        page.get_by_role('button',name='Resume 3D animation').click()
        # Short desktop screens reproduce the original cap/nav collision.
        for width,height in [(1440,720),(1024,650),(1920,1080)]:
            page.set_viewport_size({'width':width,'height':height})
            for progress in [.33,.55,.76]:
                seek(progress)
                assert_cap_visible()
        page.set_viewport_size({'width':1440,'height':1000})
        seek(0)
        page.get_by_role('button',name='Pause 3D animation').click()
        expect(page.get_by_role('button',name='Resume 3D animation')).to_have_attribute('aria-pressed','true')
        page.get_by_role('button',name='Resume 3D animation').click()
        for width in [320,390,768,1024]:
            page.set_viewport_size({'width':width,'height':900})
            seek(0)
            expect(stage.locator('h1')).to_be_visible()
            header_bottom=page.locator('header').bounding_box()['height']
            assert stage.locator('h1').bounding_box()['y'] > header_bottom
            if width==390:page.screenshot(path=str(output/'immersive-opening-mobile.png'))
            seek(.76)
            assert float(stage.get_attribute('data-flow'))>.99
            assert_cap_visible()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        page.set_viewport_size({'width':390,'height':844})
        seek(.76)
        page.screenshot(path=str(output/'cinematic-mobile-pour.png'))
        page.set_viewport_size({'width':1440,'height':1000})
        for key,info in PAGES.items():
            page.goto(base+info['path'],wait_until='networkidle')
            expect(page).to_have_title(info['title'])
            expect(page.locator('h1')).to_have_count(1)
            expect(page.locator('nav a[aria-current="page"]')).to_have_attribute('href',info['path'])
            page.screenshot(path=str(output/('brand-'+key+'.png')),full_page=True)
            # All internal navigational and static URLs resolve.
            for width in [320,390,768,1440]:
                page.set_viewport_size({'width':width,'height':900})
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(key,width)
        page.set_viewport_size({'width':390,'height':844})
        page.goto(base+'/',wait_until='networkidle')
        page.get_by_role('button',name='Menu').click()
        expect(page.locator('#navigation')).to_be_visible()
        page.get_by_role('link',name='Our company',exact=True).first.click()
        expect(page).to_have_url(base+'/company')
        expect(page.get_by_role('heading',name='Subir Banerjee',exact=True)).to_be_visible()
        page.screenshot(path=str(output/'brand-mobile-company.png'),full_page=True)
        page.goto(base+'/contact?city=Prayagraj&product=jeera-soda',wait_until='networkidle')
        expect(page.locator('#enquiry-city')).to_have_value('Prayagraj')
        expect(page.locator('#enquiry-product')).to_have_value('jeera-soda')
        expect(page.locator('a[href="tel:+918169456633"]').first).to_be_visible()
        expect(page.locator('a[href="mailto:GangaShreeroots@gmail.com"]').first).to_be_visible()
        page.emulate_media(reduced_motion='reduce')
        page.goto(base+'/',wait_until='networkidle')
        assert page.locator('.scroll-story').bounding_box()['height'] < 1500
        page.goto(base+'/values',wait_until='networkidle')
        expect(page.locator('.value')).to_have_count(7)
        # Native touch events: horizontal inspection must coexist with vertical page scroll.
        touch=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        mobile_page=touch.new_page()
        mobile_page.on('pageerror',lambda e:errors.append(str(e)))
        mobile_page.goto(base+'/',wait_until='networkidle')
        expect(mobile_page.locator('.story-stage')).to_have_attribute('data-renderer','webgl',timeout=30000)
        mobile_page.locator('canvas').scroll_into_view_if_needed()
        # Use the wheel to reach the inspection chapter, then real touchscreen input.
        dims=mobile_page.locator('.scroll-story').evaluate('(e)=>e.offsetHeight-document.querySelector(".story-stage").offsetHeight')
        mobile_page.mouse.wheel(0,dims*.33)
        mobile_page.wait_for_function('Number(document.querySelector(".story-stage").dataset.progress)>.32')
        cdp=touch.new_cdp_session(mobile_page)
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':310,'y':540}]})
        for x in range(290,89,-20):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':540}]})
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        mobile_page.wait_for_function('Math.abs(Number(document.querySelector(".story-stage").dataset.rotation))>150')
        start_scroll=mobile_page.evaluate('scrollY')
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':220,'y':640}]})
        for y in range(620,349,-30):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':220,'y':y}]})
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        mobile_page.wait_for_function('(s)=>scrollY>s+100',arg=start_scroll)
        touch.close()
        assert not errors,errors
        assert not bad,bad
        print('PASS: Full-screen water opening, single logo, transparent-to-white fixed header, cap framing at short viewports, right-drag 360°, touch rotation, native vertical scroll, 3D opening/pouring/reverse scroll, pause/resume, 6 pages, page metadata, mobile menu, 4 viewport sizes, contact links, enquiry prefills, values and reduced motion; no JS/HTTP errors.')
        browser.close()
if __name__=='__main__':
    if len(sys.argv)>1:verify(sys.argv[1].rstrip('/'))
    else:
        with tempfile.TemporaryDirectory() as temp:
            server=make_server('127.0.0.1',5001,create_app(Path(temp)/'test.sqlite3'))
            threading.Thread(target=server.serve_forever,daemon=True).start()
            try:verify('http://127.0.0.1:5001')
            finally:server.shutdown()
