
import pytest

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

        self.logger.info("***** SearchActivityDate_016 *****")

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # Login
        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("*********** Login Successful **********")

        # Navigate to Activity Log
        self.logger.info("********** Starting SearchActivityDate_016 **********")

        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.activity = ActivityPage(self.driver)
        self.activity.clickActivityPageMenuItem()

        # Set date range
        self.activity.setCreatedFrom("29-08-2026")
        self.activity.setCreatedTo("31-08-2026")

        # Search
        self.activity.clickSearch()

        # Scroll to results
        self.activity.scrollToTable()

        # Validate results
        rows = self.activity.getNoOfRows()

        self.logger.info(f"Activity log rows found: {rows}")

        assert rows > 0, (
            "No activity log records found for date range "
            "29-08-2026 to 31-08-2026"
        )

