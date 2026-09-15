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
            "***** Test_BulkEditSearchPublishTypeUnPublished_042 Started *****"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # Login
        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        # Open Product List
        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        # Open Bulk Edit Products
        self.bulkedit = BulkEditProductPage(self.driver)
        self.bulkedit.clickBulkEditProducts()

        self.bulkeditsearch = BulkEditProductSearchPage(self.driver)

        # Select Unpublished Only
        self.bulkeditsearch.SelectByPublishedType(
            "Unpublished only"
        )

        self.logger.info(
            "***** Published Type 'Unpublished only' selected *****"
        )



        # Search
        self.bulkeditsearch.clickSearch()

        self.logger.info(
            "***** Search completed for Published Type "
            "'Unpublished only' *****"
        )

        # Get search results
        rows = self.bulkeditsearch.getSearchResults()

        if len(rows) == 0:

            self.logger.info(
                "***** No unpublished products found. "
                "'No data available in table' is expected. *****"
            )

            assert self.bulkeditsearch.isNoDataAvailable(), (
                "Search returned 0 rows, but "
                "'No data available in table' message "
                "was not displayed."
            )

        else:

            self.logger.info(
                f"***** Found {len(rows)} "
                "unpublished product(s) *****"
            )

            assert self.bulkeditsearch.areAllProductsUnpublished(), (
                "Unpublished Only filter returned one "
                "or more published products"
            )