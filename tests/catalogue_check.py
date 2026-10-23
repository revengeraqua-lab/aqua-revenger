"""Product enquiry and footer checks; optional live URL argument."""
import sys,threading
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import create_app
from content import PAGES
from playwright.sync_api import sync_playwright,expect
from werkzeug.serving import make_server

def verify(base):
 Path('test-results').mkdir(exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,args=['--enable-unsafe-swiftshader'])
  page=browser.new_page(viewport={'width':1440,'height':1000});errors=[];bad=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
  for key,info in PAGES.items():
   page.goto(base+info['path'],wait_until='networkidle')
   expect(page.locator('.topline')).to_have_count(0)
   credit=page.get_by_role('link',name='dipanshudev.com',exact=False)
   expect(credit).to_have_attribute('href','https://dipanshudev.com')
   for width in [320,390,768,1440]:
    page.set_viewport_size({'width':width,'height':1000})
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(key,width)
   if key=='products':
    expect(page.locator('.water-grid .catalogue-card')).to_have_count(4)
    expect(page.locator('.beverage-grid .catalogue-card')).to_have_count(3)
    for photo in page.locator('.drink-photo img').all():
     photo.scroll_into_view_if_needed();photo.evaluate('(e)=>e.decode()')
    assert '₹' not in page.locator('main').inner_text()
    assert 'Price on request' not in page.locator('main').inner_text()
    page.screenshot(path='test-results/products-new-desktop.png',full_page=True)
   page.locator('footer').scroll_into_view_if_needed()
   if key=='company':page.locator('footer').screenshot(path='test-results/footer-new-desktop.png')
  page.goto(base+'/products',wait_until='networkidle')
  card=page.locator('.format-500ml');quantity=card.locator('input[name="quantity"]')
  card.get_by_role('button',name='Decrease 500 ml quantity').click();expect(quantity).to_have_value('1')
  for _ in range(2):card.get_by_role('button',name='Increase 500 ml quantity').click()
  expect(quantity).to_have_value('3')
  quantity.fill('10000');card.get_by_role('button',name='Increase 500 ml quantity').click();expect(quantity).to_have_value('10000')
  quantity.fill('3');card.get_by_role('button',name='Enquire now').click()
  expect(page.locator('#enquiry-size')).to_have_value('500 ml')
  expect(page.locator('#enquiry-quantity')).to_have_value('3')
  expect(page.locator('#enquiry-product')).to_have_value('water')
  page.goto(base+'/products',wait_until='networkidle')
  page.set_viewport_size({'width':390,'height':844})
  card=page.locator('#jeera-soda');card.locator('input[name="quantity"]').fill('12')
  card.get_by_role('button',name='Enquire about jeera soda').click()
  expect(page.locator('#enquiry-product')).to_have_value('jeera-soda')
  expect(page.locator('#enquiry-quantity')).to_have_value('12')
  page.goto(base+'/products',wait_until='networkidle');page.emulate_media(reduced_motion='reduce')
  page.screenshot(path='test-results/products-new-mobile.png',full_page=True)
  page.locator('footer').scroll_into_view_if_needed();page.locator('footer').screenshot(path='test-results/footer-new-mobile.png')
  for selector in ['.catalogue-card','.office','.value']:
   for node in page.locator(selector).all():assert node.evaluate('(e)=>getComputedStyle(e).opacity')=='1'
  assert not errors,errors
  assert not bad,bad
  browser.close()
  print('PASS: 6 pages, footer credit, no top strip/prices, 7 product images, quantity bounds, enquiry prefills, mobile layout and reduced motion.')
if __name__=='__main__':
 if len(sys.argv)>1:verify(sys.argv[1].rstrip('/'))
 else:
  server=make_server('127.0.0.1',5001,create_app());threading.Thread(target=server.serve_forever,daemon=True).start()
  try:verify('http://127.0.0.1:5001')
  finally:server.shutdown()
