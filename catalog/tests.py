"""Test the app catalog"""
from unittest.mock import patch
from django.urls import NoReverseMatch, reverse
from django.test import TestCase
from nutella_stop.wsgi import get_wsgi_application, application, os_environ, os
from .database import regex, results
from .models import Product, Category

# Create your tests here.
class PageTestCase(TestCase):
    """Test pages"""
    def test_catalog_page(self):
        """test the index page"""
        response = self.client.get(reverse('catalog:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        """test the index page"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        """test the search page"""
        response = self.client.get(reverse('catalog:search'), {
            'query': 'Oeufs',
            })
        self.assertEqual(response.status_code, 200)

    def test_notices_page(self):
        """test the notices page"""
        response = self.client.get(reverse('catalog:notices'))
        self.assertEqual(response.status_code, 200)

    def test_admin_page(self):
        """test the admin page"""
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

class DetailPageTestCase(TestCase):
    """Test detail pages"""
    # ran before each test.
    def setUp(self):
        """setUp"""
        self.product = Product()
        self.category = Category.objects.create(name='Saumons, Poissons')
        Product.objects.create(
            name='SOMETHING_WITH_NUTRI_SCORE_A',
            category=self.category,
            description='nothing',
            nutriscore='A',
            stores='LECLERC',
            image='img/...',
            brand='Django',
            calories='49',
            lipids='78',
            sugars='8',
            proteins='7',
            salts='8',
            url_off='https://...',
            id='74'
            )

    def test_substitute_page(self):
        """test substitute page"""
        response = self.client.get(reverse('catalog:search-a-substitute'),
                                   {'query': 'SOMETHING_WITH_NUTRI_SCORE_A',})
        self.assertEqual(response.status_code, 200)

    def test_not_existing_substitute_page(self):
        """test no substitute page"""
        try:
            response = self.client.get(reverse('catalog:search-a-substitute'), {
                'query': 'NOTHING',
            })
            self.assertEqual(response.status_code, 404)
        except:
            pass

    def test_simple_product(self):
        """test simple product """
        test = Product.objects.filter(name='SOMETHING_WITH_NUTRI_SCORE_A')
        t = None
        for t in test:
            pass
        self.assertEqual(78, t.lipids)
        self.assertEqual(74, t.id)
        self.assertEqual('nothing', t.description)
        self.assertNotEqual(2318, t.proteins)
        self.assertFalse(t.stores is None)

    def test_detail_page_returns_200(self):
        """test that detail page returns a 200 if the item exists"""
        product_id = self.product.id
        response = self.client.get(reverse('catalog:index', args=(product_id)))
        self.assertEqual(response.status_code, 200)

    def test_search_returns_200(self):
        example = str('SOMETHING_WITH_NUTRI_SCORE_A')
        response = self.client.get(reverse('catalog:search'), {'query': example,})
        self.assertEqual(response.status_code, 200)

    def test_regex_id(self):
        cat = Category.objects.filter(name='Saumons, Poissons')
        for c in cat:
            pass
        global categories
        categories = ['A CATEGORY', 'B CATEGORY', 'Noisettes']
        for category in categories:
            regex(category, c.name)
        self.assertEqual(categories.index(category), 2)

    @patch('catalog.database.results')
    def test_results_message(self, mock_api):
        test = Product.objects.filter(name='SOMETHING_WITH_NUTRI_SCORE_A')
        for t in test:
            product_id = t.id
        m = results(product_id)
        message = m
        fake_results = {'lipids_percentage': '130.0%', 'calories_percentage': '8.75%',
                        'salts_percentage': '347.82608695652175%', 'result_nutri_score_cal': \
                        'Peu calorique', 'result_nutri_score_pro': 'Un peu protéiné',
                        'result_nutri_score_salts': 'Trop salé', 'result_nutri_score_sugars': \
                        'Peu sucré', 'result_nutri_score_lpds': 'Trop lipidique',
                        'proteins_percentage': '43.75%', 'sugars_percentage': '17.77777777777778%'}
        del message['this_product']
        mock_api.message = message
        self.assertEquals(fake_results, mock_api.message)

    @patch('catalog.database.results')
    def test_results_score(self, mock_api):
        test = Product.objects.filter(name='SOMETHING_WITH_NUTRI_SCORE_A')
        for t in test:
            product_id = t.id
        m = results(product_id)
        message = m
        mock_api.message = message
        self.assertEqual("Trop lipidique", mock_api.message['result_nutri_score_lpds'])
        self.assertNotEqual("Un peu trop lipidique", mock_api.message['result_nutri_score_lpds'])
        self.assertEqual("Un peu protéiné", mock_api.message['result_nutri_score_pro'])
        self.assertNotEqual("Bonne source de protéines", mock_api.message['result_nutri_score_pro'])

class NoReverse(TestCase):
    def test_fake_page(self):
        try:
            response = self.client.get(reverse('fake'))
            self.assertRaisesMessage(NoReverseMatch, response)
        except NoReverseMatch:
            pass

    def test_detail_not_existing(self):
        try:
            response = self.client.get(reverse('catalog:index', args=('9')))
            self.assertRaisesMessage(NoReverseMatch, response)
        except NoReverseMatch:
            pass

class OsTest(TestCase):
    def test_wsgi(self):
        self.assertEqual(type(application), type(get_wsgi_application()))

    def test_os_environ(self):
        a = 'DJANGO_SETTINGS_MODULE'
        b = 'nutella_stop.settings'
        self.assertEqual(os.environ.setdefault(a, b), os_environ)
