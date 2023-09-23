from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from django.urls import reverse_lazy

from base_test.functional_tests import BaseFunctionalTest


class BaseSiteTest(BaseFunctionalTest):

    def test_index(self):
        for browser in self.browsers:
            browser.get(urljoin(self.live_server_url, str(reverse_lazy('base_site:index'))))
            h1_title = browser.find_element(By.TAG_NAME, 'h1')
            self.assertEqual(
                h1_title.text,
                'Welcome to Holiday Homes'
            )
