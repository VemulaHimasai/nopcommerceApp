import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.AddManufacturerPage import AddManufacturer
from pageObjects.DeleteManufacturerPage import DeleteManufacturer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_DeleteManufacturerSelected_065:


    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_deletemanufacturerselect(self, setup):

        self.logger.info(
            "***** Test_DeleteManufacturer_Selected_065 *****"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # Login
        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***** Login successful *****")

        # Open Catalog > Manufacturers
        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addmanufacturer = AddManufacturer(self.driver)
        self.addmanufacturer.clickonManufacturersmenuItem()

        self.logger.info("***** Manufacturers page opened *****")

        # Create manufacturer to delete
        manufacturer_name = "Test Manufacturer 065"

        self.addmanufacturer.clickAddNew()
        self.addmanufacturer.setManufacturerName(manufacturer_name)
        self.addmanufacturer.clickSave()

        self.logger.info(
            f"***** Manufacturer created: {manufacturer_name} *****"
        )

        # Select and delete the manufacturer
        self.deletemanufacturer = DeleteManufacturer(self.driver)
        self.deletemanufacturer.selectManufacturer(manufacturer_name)
        self.deletemanufacturer.clickDeleteSelected()
        self.deletemanufacturer.confirmDelete(manufacturer_name)

        # Verify deletion
        assert not self.deletemanufacturer.isManufacturerPresent(
            manufacturer_name
        ), f"Manufacturer was not deleted: {manufacturer_name}"

        self.logger.info(
            f"***** Manufacturer deleted successfully: "
            f"{manufacturer_name} *****"
        )

