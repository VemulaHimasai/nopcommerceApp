import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchProductPage import SearchProduct
from pageObjects.BulkEditProductPage import BulkEditProductPage
from pageObjects.BulkEditProductSearchPage import BulkEditProductSearchPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_BulkEditSearchProductName_037:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_bulkeditsearch_productname(self, setup):

        self.logger.info(
            "***** Test_BulkEditSearchProductName_037 *****"
        )

        self.driver = setup

        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # =====================================================
        # LOGIN
        # =====================================================

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "***** Login Successful *****"
        )

        # =====================================================
        # CATALOG -> PRODUCTS
        # =====================================================

        self.logger.info(
            "***** Starting Bulk Edit Product "
            "Search By Name Test *****"
        )

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        # =====================================================
        # GET EXISTING PRODUCT NAME DYNAMICALLY
        # =====================================================

        self.searchproduct = SearchProduct(
            self.driver
        )

        product_name = (
            self.searchproduct.getFirstProductName()
        )

        assert product_name, (
            "No existing product was found "
            "in Products table"
        )

        print(
            "========================================"
        )

        print(
            "Dynamic Product Name:",
            product_name
        )

        print(
            "========================================"
        )

        self.logger.info(
            f"Dynamic product selected: "
            f"{product_name}"
        )

        # =====================================================
        # OPEN BULK EDIT PRODUCTS
        # =====================================================

        self.bulkedit = BulkEditProductPage(
            self.driver
        )

        self.bulkedit.clickBulkEditProducts()

        # =====================================================
        # CREATE BULK EDIT SEARCH OBJECT
        # =====================================================

        self.bulkeditsearch = (
            BulkEditProductSearchPage(
                self.driver
            )
        )

        # =====================================================
        # SEARCH PRODUCT BY NAME
        # =====================================================

        self.bulkeditsearch.setProductName(
            product_name
        )

        self.bulkeditsearch.clickSearch()

        # =====================================================
        # VERIFY PRODUCT
        # =====================================================

        assert self.bulkeditsearch.isProductDisplayed(
            product_name
        ), (
            f"Product '{product_name}' "
            f"was not displayed in search results"
        )

        self.logger.info(
            f"Product '{product_name}' "
            f"displayed successfully"
        )

        print(
            f"Product '{product_name}' "
            f"bulk edit search verification PASSED"
        )