
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchCustomerByName_005:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchCustomerByName(self, setup):

        self.logger.info(
            "******* SearchCustomerByName_005 *********"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

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
        # Navigate to Customers
        # -------------------------------------------------

        self.logger.info(
            "********** Starting SearchCustomerByName_005 **********"
        )

        self.addcust = AddCustomer(self.driver)

        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        self.logger.info(
            "******** Customers page opened ********"
        )

        # -------------------------------------------------
        # Search Customer By Name
        # -------------------------------------------------

        searchcust = SearchCustomer(self.driver)

        self.logger.info(
            "******** Searching customer by Name ***********"
        )

        searchcust.setFirstName("Johnny")
        searchcust.setLastName("James")

        searchcust.clickSearch()

        # -------------------------------------------------
        # Wait/scroll to search results
        # -------------------------------------------------

        searchcust.scrollToTable()

        # -------------------------------------------------
        # Verify search result
        # -------------------------------------------------

        status = searchcust.searchCustomerByName(
            "Johnny James"
        )

        print(
            "Search Customer By Name Status:",
            status
        )

        assert status is True, (
            "Customer 'Johnny James' was not found "
            "in search results."
        )

        self.logger.info(
            "******** TC_SearchCustomerByName_005 Finished **********"
        )

        self.driver.close()

