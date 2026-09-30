import pytest

from pageObjects.AddManufacturerPage import AddManufacturer
from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchManufacturerPage import SearchManufacturer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_SearchManufacturerPublish_All_060:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()
    @pytest.mark.regression
    def test_searchmanufacturerpublish_all(self,setup):
        self.logger.info(
            "***** Test_SearchManfacturerPublish_All_060 *****"
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
        # CATALOG -> MANUFACTURERS
        # =====================================================
        self.logger.info(
            "***** Starting Search Manufacturer By Published All Test *****"
        )
        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addmanufacturer = AddManufacturer(self.driver)
        self.addmanufacturer.clickonManufacturersmenuItem()

        # =====================================================
        # SEARCH MANUFACTURER
        # =====================================================

        self.searchmanufacturer = SearchManufacturer(self.driver)
        self.searchmanufacturer.selectPublishedItem("All")

        self.searchmanufacturer.clickSearch()

        # =====================================================
        # VERIFY RESULTS
        # =====================================================
        row_count = self.searchmanufacturer.getManufacturerRowCount()

        assert row_count > 0, (
            "No manufacturer rows were returned "
            "after selecting Published = All"
        )
        self.logger.info(
            f"***** Published = All returned "
            f"{row_count} manufacturer rows *****"
        )
