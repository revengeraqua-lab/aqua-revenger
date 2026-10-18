"""Run with: python tests/browser_check.py (requires playwright package and Chrome)."""
import sys
import tempfile
import threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from playwright.sync_api import sync_playwright, expect
from werkzeug.serving import make_server

output = Path('test-results')
output.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as folder:
    server = make_server('127.0.0.1', 5001, create_app(Path(folder) / 'ui.sqlite3'))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', headless=True, args=['--enable-unsafe-swiftshader'])
            page = browser.new_page(viewport={'width':1440,'height':1000})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto('http://127.0.0.1:5001', wait_until='networkidle')
            stage=page.locator('.story-stage')
            expect(stage).to_have_attribute('data-renderer','webgl',timeout=30000)
            expect(stage.locator('canvas')).to_be_visible()
            def seek(progress):
                dimensions=page.locator('.scroll-story').evaluate('(e)=>({top:e.getBoundingClientRect().top+scrollY,distance:e.offsetHeight-document.querySelector(".story-stage").offsetHeight})')
                delta=dimensions['top']+dimensions['distance']*progress-page.evaluate('scrollY')
                page.mouse.wheel(0,delta)
                page.wait_for_function('(p)=>Math.abs(Number(document.querySelector(".story-stage").dataset.progress)-p)<.002',arg=progress,timeout=15000)
            seek(.33)
            expect(stage).to_have_attribute('data-chapter','2')
            expect(stage).to_have_attribute('data-scene','light')
            seek(.55)
            expect(stage).to_have_attribute('data-chapter','3')
            assert float(stage.get_attribute('data-cap'))>.99
            assert abs(stage.bounding_box()['y'])<1, 'Scene must pin to the viewport'
            page.screenshot(path=str(output / '3d-open.png'))
            seek(.76)
            expect(stage).to_have_attribute('data-chapter','4')
            assert float(stage.get_attribute('data-flow'))>.99
            page.screenshot(path=str(output / '3d-pour.png'))
            seek(.33)
            assert float(stage.get_attribute('data-flow'))==0, 'Scrolling backwards must stop the stream'
            seek(.99)
            expect(stage).to_have_attribute('data-chapter','5')
            expect(stage.locator('.story-formats')).to_be_visible()
            seek(0)
            assert float(stage.get_attribute('data-cap'))<.001, 'Cap must close on reverse scroll'
            page.screenshot(path=str(output / 'desktop.png'))
            for width in [320,390,768,1024,1440]:
                page.set_viewport_size({'width':width,'height':900})
                assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), f'Overflow at {width}'
            page.set_viewport_size({'width':390,'height':844})
            seek(.76)
            assert float(stage.get_attribute('data-flow'))>.99
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.screenshot(path=str(output / '3d-mobile-pour.png'))
            seek(0)
            page.mouse.wheel(0,-300)
            page.wait_for_timeout(300)
            page.screenshot(path=str(output / 'mobile.png'))
            page.get_by_role('button',name='Toggle navigation').click()
            expect(page.locator('.header nav')).to_be_visible()
            page.get_by_role('link',name='The collection',exact=True).click()
            page.get_by_role('button',name='Add one case of 500 ml to bag').click()
            page.get_by_role('button',name='Open enquiry bag').click()
            page.get_by_role('button',name='Increase 500 ml cases').click()
            expect(page.locator('#bag-count')).to_have_text('2')
            page.get_by_role('button',name='Enquire about these cases').click()
            page.get_by_label('Your name').fill('Browser Test')
            page.get_by_label('Phone number').fill('+91 9876543210')
            page.get_by_label('City',exact=True).fill('Lucknow')
            page.get_by_role('button',name='Send enquiry').click()
            expect(page.locator('#form-status')).to_contain_text('Reference: RV-')
            expect(page.locator('#bag-count')).to_have_text('0')
            page.get_by_role('button',name='Close enquiry').click()
            page.locator('.roots-copy .partner-button').click()
            expect(page.locator('#enquiry-form button[type=submit]')).to_contain_text('Send enquiry')
            expect(page.locator('#enquiry-form button[type=submit]')).to_be_enabled()
            page.get_by_role('button',name='Close enquiry').click()
            page.get_by_role('button',name='Pause ambient animations').click()
            expect(page.locator('body')).to_have_class('js-ready motion-paused')
            page.emulate_media(reduced_motion='reduce')
            page.reload(wait_until='networkidle')
            expect(page.get_by_role('button',name='Resume ambient animations')).to_be_visible()
            assert page.locator('.scroll-story').evaluate('(e)=>e.offsetHeight<=innerHeight+1'), 'Reduced motion must remove the long pinned scroll'
            assert not errors, errors
            browser.close()
            print('PASS: true WebGL scene, pinned scroll, opening, pouring, reverse scrubbing, 5 responsive widths, mobile navigation, cart, persisted enquiry and reduced motion; no page errors.')
    finally:
        server.shutdown()
