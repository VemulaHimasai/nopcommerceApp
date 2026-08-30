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

class Test_SearchActivityDate_016:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()
    @pytest.mark.regression
    def test_searchActivityDate(self, setup):
        self.logger.info("*****SearchActivityDate_016*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("**********Starting SearchActivityDate_016**********")
        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.activity = ActivityPage(self.driver)
        self.activity.clickActivityPageMenuItem()

        self.activity.setCreatedFrom("24-08-2026")
        self.activity.setCreatedTo("26-08-2026")

        self.activity.clickSearch()

        self.activity.scrollToTable()

        rows = self.activity.getNoOfRows()

        assert rows > 0

