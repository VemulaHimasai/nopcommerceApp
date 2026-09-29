import pytest

from pageObjects.AddManufacturerPage import AddManufacturer
from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchManufacturerPage import SearchManufacturer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_SearchManufacturerByName_059:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchmanufacturerbyname(self,setup):
        self.logger.info(
            "***** Test_SearchManfacturerByName_059 *****"
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
            "***** Starting Search Manufacturer By Name Test *****"
        )
        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addmanufacturer = AddManufacturer(self.driver)
        self.addmanufacturer.clickonManufacturersmenuItem()

        # =====================================================
        # SEARCH MANUFACTURER
        # =====================================================

        self.searchmanufacturer = SearchManufacturer(self.driver)

        manufacturer_name = self.searchmanufacturer.getFirstManufacturerName()

        assert manufacturer_name, (
            "No existing category was found in the table"
        )
        self.logger.info(
            f"***** Manufacturer selected for search: "
            f"{manufacturer_name} *****"
        )
        self.searchmanufacturer.enterManufacturerName(manufacturer_name)
        self.searchmanufacturer.clickSearch()

        manufacturer_present = (
            self.searchmanufacturer.isManufacturerPresent(manufacturer_name)
        )
        assert manufacturer_present, (
            f"Manufacturer '{manufacturer_name}' "
            f"was not found after searching by name"
        )
        self.logger.info(
            f"***** Manufacturer '{manufacturer_name}' "
            f"found successfully *****"
        )


