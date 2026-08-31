import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.OnlineCustomersPage import OnlineCustomersPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchCustomerRoleRegistered_022:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchcustomerrole_registered(self, setup):

        self.logger.info(
            "*****SearchCustomer_RoleRegistered_022*****"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        # Login
        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "***********Login Successful**********"
        )

        # Navigate to Online Customers
        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.onlinecustomer = OnlineCustomersPage(self.driver)
        self.onlinecustomer.clickonOnlineCustomerMenuItem()

        # Get normal online customers
        normal_customer_names = (
            self.onlinecustomer.getCustomerNames()
        )

        print("\nNormal Customers Names:")

        for name in normal_customer_names:
            print(name)

        self.logger.info(
            f"Normal table customer count: "
            f"{len(normal_customer_names)}"
        )

        # Select Registered role
        self.onlinecustomer.selectCustomerRole(
            "Registered"
        )

        # Search
        self.onlinecustomer.clickSearch()

        # Get search results
        search_customer_names = (
            self.onlinecustomer.getSearchResults()
        )

        print("\nRegistered Search Results:")

        for name in search_customer_names:
            print(name)

        self.logger.info(
            f"Registered search result count: "
            f"{len(search_customer_names)}"
        )

        # Validate search returned results
        assert len(search_customer_names) > 0, (
            "No customers found for Registered role"
        )