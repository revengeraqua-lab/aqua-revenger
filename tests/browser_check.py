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
        page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
        page.goto(base+'/',wait_until='networkidle')
        stage=page.locator('.story-stage')
        expect(stage).to_have_attribute('data-renderer','webgl',timeout=30000)
        expect(stage.locator('canvas')).to_be_visible()
        def seek(progress):
            d=page.locator('.scroll-story').evaluate('(e)=>({top:e.getBoundingClientRect().top+scrollY,distance:e.offsetHeight-document.querySelector(".story-stage").offsetHeight})')
            page.mouse.wheel(0,d['top']+d['distance']*progress-page.evaluate('scrollY'))
            page.wait_for_function('(p)=>Math.abs(Number(document.querySelector(".story-stage").dataset.progress)-p)<.002',arg=progress,timeout=15000)
        for progress,chapter in [(.33,'2'),(.55,'3'),(.76,'4'),(.99,'5'),(0,'1')]:
            seek(progress)
            expect(stage).to_have_attribute('data-chapter',chapter)
            if chapter=='3':assert float(stage.get_attribute('data-cap'))>.99
            if chapter=='4':
                assert float(stage.get_attribute('data-flow'))>.99
                assert abs(stage.bounding_box()['y'])<1
                page.screenshot(path=str(output/'cinematic-pour.png'))
        page.get_by_role('button',name='Pause 3D animation').click()
        expect(page.get_by_role('button',name='Resume 3D animation')).to_have_attribute('aria-pressed','true')
        page.get_by_role('button',name='Resume 3D animation').click()
        for width in [320,390,768,1024]:
            page.set_viewport_size({'width':width,'height':900})
            seek(.76)
            assert float(stage.get_attribute('data-flow'))>.99
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
        assert not errors,errors
        assert not bad,bad
        print('PASS: 3D opening/pouring/reverse scroll, pause/resume, 6 pages, page metadata, mobile menu, 4 viewport sizes, contact links, enquiry prefills, values and reduced motion; no JS/HTTP errors.')
        browser.close()
if __name__=='__main__':
    if len(sys.argv)>1:verify(sys.argv[1].rstrip('/'))
    else:
        with tempfile.TemporaryDirectory() as temp:
            server=make_server('127.0.0.1',5001,create_app(Path(temp)/'test.sqlite3'))
            threading.Thread(target=server.serve_forever,daemon=True).start()
            try:verify('http://127.0.0.1:5001')
            finally:server.shutdown()
