import time
import pytest
import string
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pageObjects.ActivityPage import ActivityPage
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

    def test_searchcustomerrole_registered(self,setup):
        self.logger.info("*****SearchCustomer_RoleRegistered_022*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("********Starting_SearchRegistered_Role_022******")
        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.onlinecustomer = OnlineCustomersPage(self.driver)
        self.onlinecustomer.clickonOnlineCustomerMenuItem()

        normal_customer_names = self.onlinecustomer.getCustomerNames()
        print("\n Normal Customers Names : ")
        for name in normal_customer_names:
            print(name)
        self.logger.info(
            f"Normal table customer count: "
            f"{len(normal_customer_names)}"
        )
        self.onlinecustomer.selectCustomerRole("Registered")

        self.onlinecustomer.clickSearch()

        search_customer_names = self.onlinecustomer.getSearchResults()

        print("\nRegistered Search Results:")
        for name in search_customer_names:
            print(name)

        self.logger.info(
            f"Registered search result count: "
            f"{len(search_customer_names)}"
        )

        for customer_name in search_customer_names:
            assert customer_name in normal_customer_names,(
                f"Customer '{customer_name}' from "
                f"Registered search results was not found "
                f"in the normal table"
            )


