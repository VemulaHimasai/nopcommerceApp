import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.BulkEditProductPage import BulkEditProductPage
from pageObjects.BulkEditProductSearchPage import BulkEditProductSearchPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_BulkEditSearchPublishTypeAll_040:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_bulkeditsearch_publishtype_all(self, setup):

        self.logger.info(
            "***** Test_BulkEditProductSearchPublishType_040 Started *****"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # ---------------- LOGIN ----------------
        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***** Login Successful *****")

        # ---------------- NAVIGATE TO BULK EDIT ----------------
        self.logger.info(
            "***** Starting Bulk Edit Product Search Published Type Test *****"
        )

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.bulkedit = BulkEditProductPage(self.driver)
        self.bulkedit.clickBulkEditProducts()

        # ---------------- SEARCH BY PUBLISHED TYPE ----------------
        self.bulkeditsearch = BulkEditProductSearchPage(self.driver)

        self.bulkeditsearch.SelectByPublishedType("All")

        self.bulkeditsearch.clickSearch()

        # ---------------- VERIFY RESULTS ----------------
        rows = self.bulkeditsearch.getSearchResults()

        self.logger.info(f"***** Products Found: {len(rows)} *****")

        assert len(rows) > 0, (
            "No products found for Published Type: All"
        )

        self.logger.info(
            "***** Published Type 'All' Search Passed *****"
        )