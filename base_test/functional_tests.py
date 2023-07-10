from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")


class BaseFunctionalTest(StaticLiveServerTestCase):
    webdrivers = [
        # (selenium_webdriver.Chrome, chrome_options),
        (selenium_webdriver.Firefox, firefox_options),
    ]
    page_load_timeout = 10

    def setUp(self) -> None:
        self.browsers = []
        for webdriver in self.webdrivers:
            browser = webdriver[0](options=webdriver[1])
            WebDriverWait(browser, self.page_load_timeout).until(
                lambda _browser:
                _browser.execute_script("return document.readyState") == "complete"
            )
            self.browsers.append(browser)
        return super().setUp()

    def tearDown(self) -> None:
        for browser in self.browsers:
            browser.quit()
        return super().tearDown()
