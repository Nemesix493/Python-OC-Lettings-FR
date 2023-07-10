from django.test import TestCase
from django.urls import reverse_lazy

from .utils import get_letting


class LettingsViewsTest(TestCase):
    def test_index(self):
        response = self.client.get(reverse_lazy('lettings:index'))
        self.assertEqual(
            response.status_code,
            200
        )

    def test_letting(self):
        (letting, address) = get_letting()
        response = self.client.get(
            reverse_lazy('lettings:letting', kwargs={'letting_id': letting.id})
        )
        self.assertEqual(
            response.status_code,
            200
        )
