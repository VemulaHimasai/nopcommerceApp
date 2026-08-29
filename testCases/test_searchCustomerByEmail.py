import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    def test_searchCustomerByEmail(self,setup):
        self.logger.info("*******SearchCustomerByEmail_004*********")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("**********Starting SearchCustomerByEmail_004**********")

        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        self.logger.info("******** searching customer by emailID***********")
        searchcust = SearchCustomer(self.driver)
        searchcust.setEmail("stark1@stark1.com")
        searchcust.clickSearch()

        searchcust.scrollToTable()

        time.sleep(3)

        status = searchcust.searchCustomerByEmail("stark1@stark1.com")
        assert True == status
        self.logger.info("********TC_SearchCustomerByEmail_004 Finished**********")
        self.driver.close()