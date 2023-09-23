from django.test import TestCase
from django.urls import reverse_lazy

from .utils import get_profile


class ProfilesViewsTest(TestCase):
    def test_index(self):
        response = self.client.get(reverse_lazy('profiles:index'))
        self.assertEqual(
            response.status_code,
            200
        )

    def test_letting(self):
        (user, profile) = get_profile()
        response = self.client.get(
            reverse_lazy('profiles:profile', kwargs={'username': user.username})
        )
        self.assertEqual(
            response.status_code,
            200
        )
