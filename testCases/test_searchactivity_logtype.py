import time
import pytest
import string
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.ActivityPage import ActivityPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_SearchActivityLogType_018:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()
    @pytest.mark.regression
    def test_searchactivity_logtype(self,setup):
        self.logger.info("*****SearchActivity_LogType_018*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("**********Starting SearchActivity_LogType_018**********")
        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.activity = ActivityPage(self.driver)
        self.activity.clickActivityPageMenuItem()

        self.activity.setActivity_LogType("Customers were exported")
        self.activity.clickSearch()

        self.activity.scrollToTable()

        rows = self.activity.getNoOfRows()

        assert rows > 0
