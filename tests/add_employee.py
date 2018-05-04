import unittest
from selenium import webdriver
from faker import Faker
import time

fake = Faker()



class AddEmployee(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://hrm-online.portnov.com/")


    def test_valid_login(self):
        driver = self.driver

        first_name = fake.first_name()
        last_name = fake.last_name()
        employeeId = fake.random_number(9)

        driver.find_element_by_id("txtUsername").send_keys("admin")
        driver.find_element_by_id("txtPassword").send_keys("password")
        driver.find_element_by_id("btnLogin").click()
        welcome_text = driver.find_element_by_id("welcome").text

        #  expected value vs. Actual value
        self.assertEqual("Welcome Admin", welcome_text)

        driver.find_element_by_id("btnAdd").click()

        form_title_1 = driver.find_element_by_class_name("head").text
        self.assertEqual("Add Employee", form_title_1)

        driver.find_element_by_id("firstName").send_keys(first_name)
        driver.find_element_by_id("lastName").send_keys(last_name)
        driver.find_element_by_id("employeeId").clear()
        driver.find_element_by_id("employeeId").send_keys(employeeId)
        driver.find_element_by_id("btnSave").click()

        form_title_2 = driver.find_element_by_class_name("head").text
        #  expected value vs. Actual value
        self.assertEqual("Personal Details", form_title_2)

        driver.find_element_by_id("menu_pim_viewEmployeeList").click()

        driver.find_element_by_id("empsearch_id").send_keys(employeeId)
        driver.find_element_by_id("searchBtn").click()

        list_employees=driver.find_elements_by_xpath("//td[3]/a")
        self.assertTrue(len(list_employees) == 1)

        self.assertEqual(first_name, driver.find_element_by_xpath("//td[3]/a").text)
        self.assertEqual(last_name, driver.find_element_by_xpath("//td[4]/a").text)


    def tearDown(self):
        self.driver.quit()



if __name__ == '__main__':
    unittest.main()
