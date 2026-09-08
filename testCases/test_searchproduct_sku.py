import os
import pytest
import string
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchProductPage import SearchProduct
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_SearchProductBySKU_030:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchproductbysku(self,setup):
        self.logger.info("*****Test_SearchProductBySKU_030*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("*****Login Successful******")

        self.logger.info("*****Staring Search Product By SKU test*****")

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.searchproduct = SearchProduct(self.driver)
        self.searchproduct.setSKU("SKU64529")
        self.searchproduct.clickGo()

        print("URL after Go:", self.driver.current_url)
        print("Title after Go:", self.driver.title)

        assert self.searchproduct.verifySKU("SKU64529"),\
        "Expected SKU was not found on the product page"


