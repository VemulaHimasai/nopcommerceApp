import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.OnlineCustomersPage import OnlineCustomersPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchCustomerRoleForumModerator_023:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchcustomerrole_forummoderator(self, setup):

        self.logger.info(
            "*****SearchCustomer_RoleForumModerator_023*****"
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

        # Open Customers menu
        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        # Open Online Customers
        self.onlinecustomer = OnlineCustomersPage(self.driver)
        self.onlinecustomer.clickonOnlineCustomerMenuItem()

        # Select Forum Moderators role
        self.onlinecustomer.selectCustomerRole(
            "Forum Moderators"
        )

        # Click Search
        self.onlinecustomer.clickSearch()

        # Get search results
        search_customer_names = (
            self.onlinecustomer.getSearchResults()
        )

        print("\nForum Moderator Search Results:")

        for name in search_customer_names:
            print(name)

        self.logger.info(
            f"Forum Moderator search result count: "
            f"{len(search_customer_names)}"
        )

        # Verify search returned results
        assert len(search_customer_names) > 0, (
            "No customers found for Forum Moderators role"
        )

        # Verify expected Forum Moderator
        assert "admin@yourStore.com" in search_customer_names, (
            "admin@yourStore.com was not found "
            "in Forum Moderators search results"
        )