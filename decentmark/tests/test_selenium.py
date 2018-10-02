from django.contrib.auth import get_user_model
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class UnitLiveTests(LiveServerTestCase):
    def setUp(self):
        User = get_user_model()
        self.user_admin = User.objects.create_superuser(username='admin',
                                 email='admin@decent.mark',
                                 password='password')
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def perform_login(self):
        self.browser.get(self.live_server_url + '/accounts/login/')

        username = self.browser.find_element_by_name("username")
        username.send_keys("admin")

        password = self.browser.find_element_by_name("password")
        password.send_keys("password")

        self.browser.find_element_by_css_selector(".btn-primary").click()

    def test_login_redirects_to_unit_list(self):
        self.perform_login()
        self.assertEqual(self.live_server_url + "/", self.browser.current_url, "At the Unit List page")