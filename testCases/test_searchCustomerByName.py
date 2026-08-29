import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    def test_searchCustomerByName(self,setup):
        self.logger.info("*******SearchCustomerByName_005*********")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("**********Starting SearchCustomerByName_005**********")

        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        self.logger.info("******** searching customer by Name***********")
        searchcust = SearchCustomer(self.driver)
        searchcust.setFirstName("Tony")
        searchcust.setLastName("James")
        searchcust.clickSearch()

        time.sleep(3)

        searchcust.scrollToTable()

        status = searchcust.searchCustomerByName("Tony James")
        assert True == status
        self.logger.info("********TC_SearchCustomerByName_005 Finished**********")
        self.driver.close()