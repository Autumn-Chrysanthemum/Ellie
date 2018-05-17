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

        driver.find_element_by_xpath("//img[@alt='OrangeHRM']")
        # driver.find_element_by_id("branding").find_element_by_tag_name('img')
        # driver.find_element_by_xpath("//*[@id='branding']/img")
        logo_element = driver.find_element_by_css_selector("#branding > img")
        logo_size = logo_element.size

        # expected, actual
        self.assertEqual(56, logo_size.get("height"))
        self.assertTrue(logo_size.get("width") == 283)
        self.assertDictEqual({'width': 283, 'height': 56}, logo_size)

        window_size= driver.get_window_size()
        logo_location = logo_element.location
        top_right_logo_corner_x_location = logo_size.get("width") + logo_location.get("x")

        # The entire logo (width) fits within the left of the window
        self.assertTrue(top_right_logo_corner_x_location < window_size.get("width")/2)


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
