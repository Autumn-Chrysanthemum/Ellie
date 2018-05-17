import unittest
from selenium import webdriver
from faker import Faker
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

fake = Faker()


class AddEmployee(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://hrm-online.portnov.com/")
        self.driver.maximize_window()
        self.wait=WebDriverWait(self.driver, 25)


    def test_valid_login(self):
        driver = self.driver

        expected_first_name = fake.first_name()
        expected_last_name = fake.last_name()
        employeeId = fake.random_number(9)
        expected_job_title = "QA Lead"
        expected_employment_status = "Full Time"
        user_name=expected_first_name+expected_last_name
        password= "Happy123"


        driver.find_element_by_id("txtUsername").send_keys("admin")
        driver.find_element_by_id("txtPassword").send_keys("password")
        driver.find_element_by_id("btnLogin").click()
        welcome_text = driver.find_element_by_id("welcome").text

        #  expected value vs. Actual value
        self.assertEqual("Welcome Admin", welcome_text)

        driver.find_element_by_id("btnAdd").click()

        form_title_1 = driver.find_element_by_class_name("head").text
        self.assertEqual("Add Employee", form_title_1)

        # create employee
        driver.find_element_by_id("firstName").send_keys(expected_first_name)
        driver.find_element_by_id("lastName").send_keys(expected_last_name)
        driver.find_element_by_id("employeeId").clear()
        driver.find_element_by_id("employeeId").send_keys(employeeId)
        driver.find_element_by_id("chkLogin").click()

        locator_user_name = (By.ID, "user_name")
        self.wait.until(EC.visibility_of_element_located(locator_user_name)).send_keys(user_name)
        # TODO: why do we need to wait for second fild to be visiable??? ask Ellie
        locator_password = (By.ID, "user_password")
        self.wait.until(EC.visibility_of_element_located(locator_password)).send_keys(password)
        driver.find_element_by_id("re_password").send_keys(password)
        driver.find_element_by_id("btnSave").click()

        # TODO: don't need to check success message - NO message here

        form_title_2 = driver.find_element_by_class_name("head").text
        #  expected value vs. Actual value
        self.assertEqual("Personal Details", form_title_2)

        driver.find_element_by_xpath("//ul[@id='sidenav']/li[6]").click()
        driver.find_element_by_id("btnSave").click()

        job_title_element = driver.find_element_by_id("job_job_title")
        Select(job_title_element).select_by_visible_text(expected_job_title)
        employment_status_element = driver.find_element_by_id("job_emp_status")
        Select(employment_status_element).select_by_visible_text(expected_employment_status)
        driver.find_element_by_id("btnSave").click()

        driver.find_element_by_id("menu_pim_viewEmployeeList").click()
        driver.find_element_by_id("empsearch_id").send_keys(employeeId)
        driver.find_element_by_id("searchBtn").click()

        list_employees=driver.find_elements_by_xpath("//td[3]/a")
        self.assertTrue(len(list_employees) == 1)

        # better to use variables here, because you probably need to use them
        first_name = driver.find_element_by_xpath("//td[3]/a").text
        last_name = driver.find_element_by_xpath("//td[4]/a").text
        job_title = driver.find_element_by_xpath("//td[5]").text
        employment_status = driver.find_element_by_xpath("//td[6]").text

        #   you can put indexes(list) and words(dictionary)
        # for index start with 0 all the time!!!, because the list must start with 0
        message = "expected the table to contain first name '{0}', but instead the value was '[1]'"
        #   expected value vs. Actual value
        self.assertEqual(expected_first_name, first_name, message.format(expected_first_name, first_name))
        self.assertEqual(expected_last_name, last_name)
        self.assertEqual(expected_job_title, job_title)
        self.assertEqual(expected_employment_status, employment_status)

        # logout
        driver.find_element_by_id("welcome").click()
        locator_logout = (By.XPATH, "//a[contains(text(),'Logout')]")
        self.wait.until(EC.visibility_of_element_located(locator_logout)).click()

        # login again
        driver.find_element_by_id("txtUsername").send_keys(user_name)
        driver.find_element_by_id("txtPassword").send_keys(password)
        driver.find_element_by_id("btnLogin").click()

        # assertion
        welcome_text = driver.find_element_by_id("welcome").text
        expected_welcome_message = "Welcome " + expected_first_name
        #  expected value vs. Actual value
        self.assertEqual(expected_welcome_message, welcome_text)


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
