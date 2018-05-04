import unittest
import time

from selenium import webdriver


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://hrm-online.portnov.com/")

    def test_valid_login(self):
        driver = self.driver
        driver.find_element_by_id("txtUsername").send_keys("admin")
        driver.find_element_by_id("txtPassword").send_keys("password")
        driver.find_element_by_id("btnLogin").click()
        # duplicate line is command+D

        welcome_text = driver.find_element_by_id("welcome").text

        #  expected value vs. Actual value
        self.assertEqual("Welcome Admin", welcome_text)

    def test_invalid_login(self):
        driver = self.driver
        driver.find_element_by_id("txtUsername").send_keys("admin")
        driver.find_element_by_id("txtPassword").send_keys("password123")
        driver.find_element_by_id("btnLogin").click()
        time.sleep(5)

        panel_text = driver.find_element_by_id("logInPanelHeading").text
        self.assertEqual("LOGIN Panel", panel_text)

        error_text = driver.find_element_by_id("spanMessage").text
        self.assertEqual("Invalid credentials", error_text)

        time.sleep(5)

    def test_pws_required_login(self):
        driver = self.driver
        driver.find_element_by_id("txtUsername").send_keys("admin")
        driver.find_element_by_id("btnLogin").click()
        time.sleep(5)

        panel_text = driver.find_element_by_id("logInPanelHeading").text
        self.assertEqual("LOGIN Panel", panel_text)

        error_text = driver.find_element_by_id("spanMessage").text
        self.assertEqual("Password cannot be empty", error_text)

        time.sleep(5)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
