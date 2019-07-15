from django.test import TestCase, client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.views import Favorite, Product, Category
from catalog.tests import DetailPageTestCase
# Create your tests here.


class PageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_account_page(self):
        response = self.client.get(reverse('account:index'))
        self.assertEqual(response.status_code, 200)

    def test_favorites_page(self):
        response = self.client.get(reverse('account:favorites'))
        self.assertEqual(response.status_code, 200)
    
    def test_profile_page(self):
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 200)

class StatusTestCase(TestCase):
    def test_login(self):
    	response = self.client.post(reverse('account:index'),{'username': 'testuser','password': 'password'}, follow=True)
    	self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('account:logout'))
        self.client.login(username='test', password='password')
        self.client.logout()
        self.assertRaises(KeyError, lambda: self.client.session['_auth_user_id'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
    
    def test_invalid_user(self):
        response = self.client.login(username= "fake", password= "fake")
        self.assertFalse(response)

class Favorites(TestCase):
    def setUp(self):
        DetailPageTestCase.setUp(self)
        self.my_user = User.objects.create(id=5, username='Testuser')

    def test_favorites_in(self):
        test = Product.objects.filter(name='SOMETHING_WITH_NUTRI_SCORE_A')
        for t in test:
            pass
        list_of_favorites = ['Huile de foie de morue', 'Saumon d‘Alaska', 'SOMETHING_WITH_NUTRI_SCORE_A']
        self.favorite = Favorite.objects.create(product_id=t.id, user_id=5)
        self.assertIn(t.name, list_of_favorites) 