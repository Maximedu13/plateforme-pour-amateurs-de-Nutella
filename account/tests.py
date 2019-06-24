from django.test import TestCase
from django.urls import reverse
# Create your tests here.

class PageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_not_existing_page(self):
        response = self.client.get(reverse('irreal'))
        self.assertEqual(response.status_code, 500)