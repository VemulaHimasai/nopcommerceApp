import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer
from pageObjects.SearchVendorPage import SearchVendorPage
from pageObjects.AddVendorPage import AddVendor
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_SearchVendorByName_013:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchVendorByName(self,setup):
        self.logger.info("*****SearchVendorByName_013*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("**********Starting SearchVendorByName_013**********")
        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.addvendor = AddVendor(self.driver)
        self.addvendor.clickonVendorMenuItem()

        self.logger.info("******** searching vendor by Name***********")
        searchvendor = SearchVendorPage(self.driver)
        searchvendor.setName("Vendor2")
        searchvendor.clickSearch()

        time.sleep(3)



        status = searchvendor.searchVendorByName("Vendor2")
        assert True == status
        self.logger.info("********TC_SearchvendorrByName_013 Finished**********")
        self.driver.close()
