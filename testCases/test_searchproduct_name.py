import pytest

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
    def test_searchproductbyname(self, setup):

        self.logger.info(
            "***** Test_SearchProductByName_029 *****"
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
            "***** Starting Search Product By Name Test *****"
        )

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        # =====================================================
        # CREATE SEARCH PRODUCT OBJECT
        # =====================================================

        self.searchproduct = SearchProduct(
            self.driver
        )

        # =====================================================
        # GET AN EXISTING PRODUCT DYNAMICALLY
        # =====================================================

        product_name = (
            self.searchproduct.getFirstProductName()
        )

        assert product_name, (
            "No existing product was found "
            "in the Products table"
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
        # SEARCH PRODUCT BY NAME
        # =====================================================

        self.searchproduct.setProductName(
            product_name
        )

        self.searchproduct.clickSearch()

        # =====================================================
        # VERIFY PRODUCT
        # =====================================================

        assert self.searchproduct.isProductPresent(
            product_name
        ), (
            f"Expected product '{product_name}' "
            f"was not found in search result"
        )

        self.logger.info(
            f"Product '{product_name}' "
            f"found successfully"
        )

        print(
            f"Product '{product_name}' "
            f"search verification PASSED"
        )