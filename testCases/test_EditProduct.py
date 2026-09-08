import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.EditProductPage import EditProductPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_EditProduct_032:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_editproduct(self,setup):
        self.logger.info("*****Test_EditProduct_031*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("*****Login Successful******")

        self.logger.info("*****Staring Edit Product test*****")

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.editproduct = EditProductPage(self.driver)
        self.editproduct.clickEditProduct("Test Product 6289")

        self.logger.info("*****Edit page opened successfully****")

        self.editproduct.setSKU("SKU64529")

        self.editproduct.setPrice("999")

        self.logger.info("*****Product details updated*****")

        self.editproduct.clickSave()

        self.logger.info("*****Save button clicked*****")

        assert self.editproduct.isProductUpdatedSuccessfully(),\
        "Product update success message was not displayed"
