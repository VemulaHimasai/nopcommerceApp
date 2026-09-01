import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.ActivityTypePage import ActivityTypePage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_VerifyActivityTypeDisplayed_026:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_verifyactivitytypedisplayed(self,setup):
        self.logger.info("******VerifyActivityTypeDisplayed******")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("********Starting Verify Activity Type**********")

        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.activity_type = ActivityTypePage(self.driver)
        self.activity_type.clickActivityTypeMenuItem()

        activity_types = ["Add a new blog post","Add a new category"]

        for activity in activity_types:
            result = self.activity_type.isActivityTypePresent(activity)
            self.logger.info("fActivity Type '{activity_name}' Status: {result}")
            assert result,(f"Activity type '{activity} not displayed")



