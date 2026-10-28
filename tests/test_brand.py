import json,re,unittest
from unittest.mock import patch
from html.parser import HTMLParser
from xml.etree import ElementTree
from app import create_app
from content import PAGES,REGIONS
class Metadata(HTMLParser):
    def __init__(self):super().__init__();self.meta={};self.canonical=None;self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta':self.meta[a.get('name') or a.get('property')]=a.get('content')
        if tag=='link' and a.get('rel')=='canonical':self.canonical=a['href']
        if tag=='h1':self.h1+=1
class BrandTests(unittest.TestCase):
    def setUp(self):self.client=create_app().test_client()
    def test_pages_metadata_and_schema(self):
        titles=[];descriptions=[]
        for key,page in PAGES.items():
            with self.subTest(page=key):
                r=self.client.get(page['path']);self.assertEqual(r.status_code,200)
                html=r.data.decode('utf-8-sig');m=Metadata();m.feed(html)
                self.assertEqual(m.h1,1);self.assertEqual(m.meta['description'],page['description'])
                self.assertEqual(m.meta['google-site-verification'],'JXDHFEyrgIf-oBW4D--vTRlSq3RV4mFEZV3dvApucmc')
                self.assertEqual(m.canonical,'https://revenger.co.in'+page['path'])
                self.assertEqual(m.meta['og:url'],m.canonical)
                schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S).group(1))
                self.assertEqual(schema['@graph'][0]['telephone'],'+918169456633')
                self.assertEqual(len(schema['@graph'][0]['areaServed']),10)
                titles.append(page['title']);descriptions.append(page['description'])
        self.assertEqual(len(set(titles)),6);self.assertEqual(len(set(descriptions)),6)
    def test_crawl_files(self):
        r=self.client.get('/sitemap.xml');self.assertEqual(r.status_code,200)
        root=ElementTree.fromstring(r.data);self.assertEqual(len(root),6)
        urls=[node.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for node in root]
        self.assertEqual(urls,['https://revenger.co.in'+p['path'] for p in PAGES.values()])
        self.assertIn(b'Sitemap: https://revenger.co.in/sitemap.xml',self.client.get('/robots.txt').data)
        self.assertEqual(self.client.get('/unknown').status_code,404)
    def test_origin_override_is_consistent_and_not_taken_from_host_header(self):
        with patch.dict('os.environ',{'SITE_URL':'https://preview.example.com/'}):
            client=create_app().test_client()
        html=client.get('/company',headers={'Host':'untrusted.example'}).data.decode('utf-8-sig')
        meta=Metadata();meta.feed(html)
        self.assertEqual(meta.canonical,'https://preview.example.com/company')
        self.assertIn(b'https://preview.example.com/company',client.get('/sitemap.xml').data)
        self.assertIn(b'Sitemap: https://preview.example.com/sitemap.xml',client.get('/robots.txt').data)
    def test_verified_content(self):
        company=self.client.get('/company').data
        for text in ('Subir Banerjee','Rakesh Salve','Managing Director','Chief Executive Officer'):self.assertIn(text.encode(),company)
        areas=self.client.get('/service-areas').data
        for cities in REGIONS.values():
            for city in cities:self.assertIn(city.encode(),areas)
        contact=self.client.get('/contact').data
        for text in ('GangaShreeroots@gmail.com','401202','212107','tel:+918169456633'):self.assertIn(text.encode(),contact)
        products=self.client.get('/products').data.decode('utf-8-sig')
        self.assertEqual(products.count('class="catalogue-card reveal format-'),2)
        for text in ('500 ml','1 litre','revenger-water-500ml.png','revenger-water-1l.png','revenger-soda-500ml.png','revenger-jeera-soda-500ml.png','revenger-nimbu-soda-500ml.png'):self.assertIn(text,products)
        for text in ('format-250ml','format-2l','250 ml','2 litres','revenger-drinks-collection.png'):self.assertNotIn(text,products)
        home=self.client.get('/').data.decode('utf-8-sig')
        self.assertIn('/static/images/revenger-water-1l.png',home)
        self.assertNotIn('/static/images/revenger-bottle-real.png',home)
if __name__=='__main__':unittest.main()
