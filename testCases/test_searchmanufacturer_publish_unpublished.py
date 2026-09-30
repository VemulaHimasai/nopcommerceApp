import pytest

from pageObjects.AddManufacturerPage import AddManufacturer
from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchManufacturerPage import SearchManufacturer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_SearchManufacturerPublish_Unpublished_062:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()
    @pytest.mark.regression
    def test_searchmanufacturerpublish_unpublished(self,setup):
        self.logger.info(
            "***** Test_SearchManufacturerPublish_Unpublished_062 *****"
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
            "***** Starting Search Manufacturer By Published - Unpublished Test *****"
        )
        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addmanufacturer = AddManufacturer(self.driver)
        self.addmanufacturer.clickonManufacturersmenuItem()

        # =====================================================
        # SEARCH MANUFACTURER
        # =====================================================

        self.searchmanufacturer = SearchManufacturer(self.driver)
        self.searchmanufacturer.selectPublishedItem("Unpublished only")

        self.searchmanufacturer.clickSearch()

        # =====================================================
        # VERIFY RESULTS
        # =====================================================

        if self.searchmanufacturer.isNoDataAvailable():
            self.logger.info(
                "***** No unpublished manufacturers exist. "
                "No data available in table displayed. *****"
            )
        else:
            row_count = self.searchmanufacturer.getManufacturerRowCount()

            assert row_count > 0, (
                "Search returned neither unpublished "
                "manufacturers nor the expected "
                "'No data available in table' message"
            )

            self.logger.info(
                f"***** Published = Unpublished Only "
                f"returned {row_count} manufacturer rows *****"
            )
