import sqlite3
import tempfile
import unittest
import os
from unittest.mock import patch
from contextlib import closing
from pathlib import Path
from app import create_app


class EnquiryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / 'test.sqlite3'
        self.client = create_app(self.database).test_client()
        self.details = dict(name='Test Customer', phone='+91 9876543210', city='Lucknow', email='test@example.com', kind='order', items=[dict(id='500ml', quantity=2)])

    def tearDown(self):
        self.temp.cleanup()

    def test_enquiry_is_persisted(self):
        result = self.client.post('/api/enquiries', json=self.details)
        self.assertEqual(result.status_code, 201)
        with closing(sqlite3.connect(self.database)) as db:
            row = db.execute('SELECT reference, name, items FROM enquiries').fetchone()
        self.assertEqual(row[0], result.json['reference'])
        self.assertEqual(row[1], self.details['name'])
        self.assertIn('500ml', row[2])

    def test_rejects_invalid_quantities_and_missing_order(self):
        for items in ([], [{'id':'500ml','quantity':True}], [{'id':'unknown','quantity':1}], [{'id':'500ml','quantity':101}]):
            with self.subTest(items=items):
                self.assertEqual(self.client.post('/api/enquiries', json={**self.details, 'items':items}).status_code, 400)

    def test_rejects_bad_contact_details(self):
        for field, value in [('phone','123'), ('email','invalid'), ('name',''), ('kind','bad')]:
            self.assertEqual(self.client.post('/api/enquiries', json={**self.details,field:value}).status_code, 400)

    def test_partner_does_not_need_a_bag(self):
        self.assertEqual(self.client.post('/api/enquiries', json={**self.details,'kind':'distributor','items':[]}).status_code, 201)

    def test_invalid_json_and_home(self):
        self.assertEqual(self.client.post('/api/enquiries', data='bad',content_type='application/json').status_code,400)
        self.assertEqual(self.client.get('/').status_code,200)
        self.assertEqual(len(self.client.get('/api/products').json['products']),4)

    def test_serverless_home_never_writes_to_filesystem(self):
        with patch.dict(os.environ, {'VERCEL':'1', 'DATABASE_URL':'', 'POSTGRES_URL':''}), \
             patch('pathlib.Path.mkdir', side_effect=PermissionError('Read-only filesystem')), \
             patch('sqlite3.connect', side_effect=AssertionError('Must not open SQLite')):
            client = create_app().test_client()
            home = client.get('/')
            self.assertEqual(home.status_code, 200)
            self.assertIn(b'/static/scroll-story.js', home.data)
            self.assertIn(b'data-available="false"', home.data)
            self.assertEqual(client.get('/api/health').json, {'status':'ok', 'enquiries':'unconfigured'})
            self.assertEqual(client.post('/api/enquiries', json=self.details).status_code, 503)

    def test_database_failure_does_not_report_enquiry_saved(self):
        with patch('storage.sqlite3.connect', side_effect=sqlite3.OperationalError('readonly')):
            result = self.client.post('/api/enquiries', json=self.details)
        self.assertEqual(result.status_code, 503)
        self.assertNotIn('reference', result.json)
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_remote_database_does_not_connect_during_startup(self):
        with patch.dict(os.environ, {'VERCEL':'1', 'DATABASE_URL':'postgresql://example.invalid/test'}), \
             patch('psycopg.connect', side_effect=AssertionError('Must stay lazy')):
            self.assertEqual(create_app().test_client().get('/').status_code, 200)

    def test_static_cdn_build_preserves_asset_paths(self):
        from build import build_assets
        target = build_assets(Path(self.temp.name) / 'public' / 'static')
        for name in ('app.js','scroll-story.js','vendor/three/three.module.js','images/revenger-bottle-real.png','fonts/fonts.css'):
            self.assertTrue((target / name).is_file(), name)


if __name__ == '__main__':
    unittest.main()
