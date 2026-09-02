import string
import random
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.ActivityPage import ActivityPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_ClearActivityLogs_021:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_clearactivitylogs(self,setup):
        self.logger.info("*****Clear_ActivityLogs_020*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("**********Starting Clear_ActivityLogs_020**********")

        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.activity = ActivityPage(self.driver)
        self.activity.clickActivityPageMenuItem()

        self.activity.clearall_logs()
        self.logger.info("**********Clear_ActivityLogs_020 completed**********")