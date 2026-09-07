import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchProductPage import SearchProduct
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchProductByVendor_031:

    # ---------------------------------------------------------
    # Application details
    # ---------------------------------------------------------
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    # ---------------------------------------------------------
    # Test Search Product By Vendor
    # ---------------------------------------------------------
    @pytest.mark.regression
    def test_searchproduct_vendor(self, setup):

        self.logger.info(
            "********** Test_SearchProductByVendor_031 Started **********"
        )

        # -----------------------------------------------------
        # Browser setup
        # -----------------------------------------------------
        self.driver = setup

        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.logger.info(
            "Application URL opened: " + self.baseURL
        )

        # -----------------------------------------------------
        # Login
        # -----------------------------------------------------
        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "********** Login Successful **********"
        )

        # -----------------------------------------------------
        # Navigate to Catalog -> Products
        # -----------------------------------------------------
        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.logger.info(
            "********** Products page opened successfully **********"
        )

        # -----------------------------------------------------
        # Search Product
        # -----------------------------------------------------
        self.searchproduct = SearchProduct(self.driver)

        # -----------------------------------------------------
        # Select Vendor = Vendor1
        # -----------------------------------------------------
        self.searchproduct.selectVendor("Vendor1")

        # -----------------------------------------------------
        # Product Name = Empty
        # -----------------------------------------------------
        self.searchproduct.clearProductName()

        # -----------------------------------------------------
        # Product Type = All
        # -----------------------------------------------------
        self.searchproduct.selectProductType("All")

        # -----------------------------------------------------
        # Published = All
        # -----------------------------------------------------
        self.searchproduct.selectPublishedItem("All")

        # -----------------------------------------------------
        # Click Search
        # -----------------------------------------------------
        self.searchproduct.clickSearch()

        self.logger.info(
            "********** Product search performed for Vendor1 **********"
        )

        # -----------------------------------------------------
        # Validate "No data available in table"
        # -----------------------------------------------------
        assert self.searchproduct.isNoDataAvailable(), \
            "Expected 'No data available in table' was not displayed"

        self.logger.info(
            "********** 'No data available in table' validated **********"
        )

        # -----------------------------------------------------
        # Validate "No records"
        # -----------------------------------------------------
        assert self.searchproduct.isNoRecordsDisplayed(), \
            "Expected 'No records' was not displayed"

        self.logger.info(
            "********** 'No records' validated **********"
        )

        self.logger.info(
            "********** Test_SearchProductByVendor_031 Passed **********"
        )