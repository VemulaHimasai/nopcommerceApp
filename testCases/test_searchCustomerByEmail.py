
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchCustomerByEmail_004:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchCustomerByEmail(self, setup):

        self.logger.info(
            "******* SearchCustomerByEmail_004 *********"
        )

        self.driver = setup

        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.driver.implicitly_wait(10)

        # -------------------------------------------------
        # Login
        # -------------------------------------------------

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "*********** Login Successful **********"
        )

        # -------------------------------------------------
        # Open Customers
        # -------------------------------------------------

        self.logger.info(
            "********** Starting SearchCustomerByEmail_004 **********"
        )

        self.addcust = AddCustomer(self.driver)

        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        # -------------------------------------------------
        # Search Customer By Email
        # -------------------------------------------------

        self.logger.info(
            "******** Searching customer by email ID ***********"
        )

        searchcust = SearchCustomer(self.driver)

        email = "stark1@stark1.com"

        searchcust.setEmail(email)
        searchcust.clickSearch()

        # -------------------------------------------------
        # Scroll to search results
        # -------------------------------------------------

        searchcust.scrollToTable()

        # -------------------------------------------------
        # Verify customer exists in search results
        # -------------------------------------------------

        status = searchcust.searchCustomerByEmail(email)

        print(
            "Search Customer By Email Status:",
            status
        )

        assert status is True, (
            f"Customer with email '{email}' "
            f"was not found in search results"
        )

        self.logger.info(
            "******** Customer found successfully ********"
        )

        self.logger.info(
            "******** TC_SearchCustomerByEmail_004 Finished **********"
        )

        self.driver.quit()

