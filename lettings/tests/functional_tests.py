from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from django.urls import reverse_lazy

from base_test.functional_tests import BaseFunctionalTest
from .utils import get_letting


class LettingTest(BaseFunctionalTest):

    def test_index(self):
        for browser in self.browsers:
            browser.get(urljoin(self.live_server_url, str(reverse_lazy('lettings:index'))))
            h1_title = browser.find_element(By.TAG_NAME, 'h1')
            self.assertEqual(
                h1_title.text,
                'Lettings'
            )

    def test_letting(self):
        (letting, address) = get_letting()
        for browser in self.browsers:
            browser.get(
                urljoin(
                    self.live_server_url,
                    str(reverse_lazy('lettings:letting', kwargs={'letting_id': letting.id}))
                )
            )
            h1_title = browser.find_element(By.TAG_NAME, 'h1')
            self.assertEqual(
                h1_title.text,
                letting.title
            )
