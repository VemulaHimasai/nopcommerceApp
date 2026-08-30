import string
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.ActivityPage import ActivityPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_Delete_SingleActivity_019:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    def test_delete_singleactivity(self,setup):
        self.logger.info("*****Delete_SingleActivity_019*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("**********Starting Delete_SingleActivity_019**********")

        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.activity = ActivityPage(self.driver)
        self.activity.clickActivityPageMenuItem()

        self.activity.setActivity_LogType("Add a new customer")
        self.activity.clickSearch()

        rows = self.activity.getNoOfRows()

        assert rows > 0, "Activity Log record was not found"

        self.logger.info(f"Activity Log records found: {rows}")

        self.activity.deleteSingleActivity("Add a new customer")

        self.logger.info("******Activity Log delete clicked*******")

