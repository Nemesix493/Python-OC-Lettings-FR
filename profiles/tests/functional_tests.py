from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from django.urls import reverse_lazy

from base_test.functional_tests import BaseFunctionalTest
from .utils import get_profile


class ProfileTest(BaseFunctionalTest):

    def test_index(self):
        for browser in self.browsers:
            browser.get(urljoin(self.live_server_url, str(reverse_lazy('profiles:index'))))
            h1_title = browser.find_element(By.TAG_NAME, 'h1')
            self.assertEqual(
                h1_title.text,
                'Profiles'
            )

    def test_letting(self):
        (user, profile) = get_profile()
        for browser in self.browsers:
            browser.get(
                urljoin(
                    self.live_server_url,
                    str(reverse_lazy('profiles:profile', kwargs={'username': user.username}))
                )
            )
            h1_title = browser.find_element(By.TAG_NAME, 'h1')
            self.assertEqual(
                h1_title.text,
                user.username
            )
