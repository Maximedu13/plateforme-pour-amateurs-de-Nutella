"""tests app account"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.views import Favorite, Product
from catalog.tests import DetailPageTestCase
# Create your tests here.

class PageTestCase(TestCase):
    """class PageTestCase"""
    def test_index_page(self):
        """test_index_page"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_account_page(self):
        """test_index_page"""
        response = self.client.get(reverse('account:index'))
        self.assertEqual(response.status_code, 200)

    def test_favorites_page(self):
        """test_favorites_page"""
        response = self.client.get(reverse('account:favorites'))
        self.assertEqual(response.status_code, 302)

    def test_profile_page(self):
        """test_profile_page"""
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 302)

class StatusTestCase(TestCase):
    """class StatusTestCase"""
    def test_login(self):
        """test login"""
        response = self.client.post(reverse('account:index'),
                                    {'username': 'testuser', 'password': 'password'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """test logout"""
        response = self.client.get(reverse('account:logout'))
        self.client.login(username='test', password='password')
        self.client.logout()
        self.assertRaises(KeyError, lambda: self.client.session['_auth_user_id'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_invalid_user(self):
        """test fake user"""
        response = self.client.login(username="fake", password="fake")
        self.assertFalse(response)

class Favorites(TestCase):
    """Class favorites"""
    def setUp(self):
        DetailPageTestCase.setUp(self)
        self.my_user = User.objects.create(id=5, username='Testuser')
        self.favorite = None

    def test_favorites_in(self):
        """test favorites in"""
        test = Product.objects.filter(name='SOMETHING_WITH_NUTRI_SCORE_A')
        t_t = None
        for t_t in test:
            pass
        list_of_favorites = ['Huile de foie de morue', 'Saumon d‘Alaska',
                             'SOMETHING_WITH_NUTRI_SCORE_A']
        self.favorite = Favorite.objects.create(product_id=t_t.id, user_id=5)
        self.assertIn(t_t.name, list_of_favorites)
