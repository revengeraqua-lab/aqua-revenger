import json,re,unittest
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
                self.assertEqual(m.canonical,'https://revenger-397n.vercel.app'+page['path'])
                schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S).group(1))
                self.assertEqual(schema['@graph'][0]['telephone'],'+918169456633')
                self.assertEqual(len(schema['@graph'][0]['areaServed']),10)
                titles.append(page['title']);descriptions.append(page['description'])
        self.assertEqual(len(set(titles)),6);self.assertEqual(len(set(descriptions)),6)
    def test_crawl_files(self):
        r=self.client.get('/sitemap.xml');self.assertEqual(r.status_code,200)
        root=ElementTree.fromstring(r.data);self.assertEqual(len(root),6)
        self.assertIn(b'/sitemap.xml',self.client.get('/robots.txt').data)
        self.assertEqual(self.client.get('/unknown').status_code,404)
    def test_verified_content(self):
        company=self.client.get('/company').data
        for text in ('Subir Banerjee','Rakesh Salve','Managing Director','Chief Executive Officer'):self.assertIn(text.encode(),company)
        areas=self.client.get('/service-areas').data
        for cities in REGIONS.values():
            for city in cities:self.assertIn(city.encode(),areas)
        contact=self.client.get('/contact').data
        for text in ('GangaShreeroots@gmail.com','401202','212107','tel:+918169456633'):self.assertIn(text.encode(),contact)
if __name__=='__main__':unittest.main()
