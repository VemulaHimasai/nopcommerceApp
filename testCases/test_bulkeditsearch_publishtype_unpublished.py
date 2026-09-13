import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.BulkEditProductPage import BulkEditProductPage
from pageObjects.BulkEditProductSearchPage import BulkEditProductSearchPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_BulkEditSearchPublishTypeUnPublished_042:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_bulkeditsearch_publishtype_unpublished(self, setup):

        self.logger.info(
            "***** Test_BulkEditProductSearchPublishTypeUnPublished_042 Started *****"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # ---------------- LOGIN ----------------
        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "***** Login Successful *****"
        )

        # ---------------- NAVIGATE TO BULK EDIT ----------------
        self.logger.info(
            "***** Starting Bulk Edit Product Search Published Type Test *****"
        )

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.bulkedit = BulkEditProductPage(self.driver)
        self.bulkedit.clickBulkEditProducts()

        # ---------------- INITIALIZE BULK EDIT SEARCH PAGE ----------------
        self.bulkeditsearch = BulkEditProductSearchPage(
            self.driver
        )

        # ---------------- SEARCH BY PUBLISHED TYPE ----------------
        self.bulkeditsearch.SelectByPublishedType(
            "Unpublished only"
        )

        self.bulkeditsearch.clickSearch()

        # ---------------- VERIFY NO DATA ----------------
        assert self.bulkeditsearch.isNoDataAvailable(), (
            "Expected 'No data available in table' "
            "for Published Type: Unpublished only"
        )

        self.logger.info(
            "***** Published Type 'Unpublished only' "
            "correctly returned no data *****"
        )

        self.logger.info(
            "***** Published Type 'Unpublished only' "
            "Search Passed *****"
        )