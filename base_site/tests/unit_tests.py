from django.test import TestCase
from django.urls import reverse_lazy


class BaseSiteViewsTest(TestCase):
    def test_index(self):
        response = self.client.get(reverse_lazy('base_site:index'))
        self.assertEqual(
            response.status_code,
            200
        )
