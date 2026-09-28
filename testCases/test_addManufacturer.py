import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.AddManufacturerPage import AddManufacturer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_AddManufacturer_058:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_addmanufacturer(self, setup):
        self.logger.info(
            "*****Test_AddManufacturer_058*****"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        wait = WebDriverWait(
            self.driver,
            15
        )

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "*****Login Successful******"
        )

        self.logger.info(
            "*****Starting Add Manufacturer test*****"
        )

        self.addproduct = AddProduct(
            self.driver
        )

        self.addproduct.clickonCatalogMenu()

        self.addmanufacturer = AddManufacturer(
            self.driver
        )

        self.addmanufacturer.clickonManufacturersmenuItem()

        # -------------------------------------------------
        # Click Add New
        # -------------------------------------------------

        self.addmanufacturer.clickAddNew()

        self.logger.info(
            "*****Providing manufacturer details*******"
        )

        # -------------------------------------------------
        # Generate Manufacturer Name
        # -------------------------------------------------

        manufacturer_name = (
            self.addmanufacturer.generateManufacturerName()
        )

        print(
            "Manufacturer Name:",
            manufacturer_name
        )

        # -------------------------------------------------
        # Enter Manufacturer Name
        # -------------------------------------------------

        assert self.addmanufacturer.setManufacturerName(
            manufacturer_name
        ), "Unable to enter manufacturer name."

        # -------------------------------------------------
        # Enter Manufacturer Description
        # -------------------------------------------------

        manufacturer_description = (
            "This is test manufacturer used for testing"
        )

        self.addmanufacturer.setManufacturerDescription(
            manufacturer_description
        )

        # -------------------------------------------------
        # Save Manufacturer
        # -------------------------------------------------

        assert self.addmanufacturer.clickSave(), (
            "Manufacturer save operation failed."
        )

        # -------------------------------------------------
        # Verify Manufacturer Creation
        # -------------------------------------------------

        assert self.addmanufacturer.isManufacturerCreatedSuccessfully(), (
            "Manufacturer was not created successfully"
        )

        self.logger.info(
            "*****Manufacturer created successfully*******"
        )

        print(
            "\nCreated Manufacturer:",
            manufacturer_name
        )