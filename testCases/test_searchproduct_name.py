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

class Test_SearchProductByName_029:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchproductbyname(self,setup):
        self.logger.info("*****Test_SearchProductByName_029*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("*****Login Successful******")

        self.logger.info("*****Staring Search Product By Name test*****")

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.searchproduct = SearchProduct(self.driver)
        self.searchproduct.setProductName("Test Product 6289")
        self.searchproduct.clickSearch()

        assert self.searchproduct.isProductPresent("Test Product 6289"),\
        "Expected product was not found in search result"

