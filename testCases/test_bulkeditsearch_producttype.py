import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.BulkEditProductPage import BulkEditProductPage
from pageObjects.BulkEditProductSearchPage import BulkEditProductSearchPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_BulkEditSearchProductType_039:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_bulkeditsearch_producttype(self,setup):
        self.logger.info("***** Test_BulkEditProductSearchProductType_038*****")

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # Login
        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***** Login Successful *****")

        self.logger.info("***** Starting Bulk Edit Product Search Product Type Test *****")

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.bulkedit = BulkEditProductPage(self.driver)
        self.bulkedit.clickBulkEditProducts()

        self.bulkeditsearch = BulkEditProductSearchPage(self.driver)

        self.bulkeditsearch.SelectByProductType("All")
        self.bulkeditsearch.clickSearch()

        rows = self.bulkeditsearch.getSearchResults()

        assert len(rows) > 0, "No products found for Product Type: All"


