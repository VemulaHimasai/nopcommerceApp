import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.EditProductPage import EditProductPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_DeleteProductByRow_032:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_deleteproductbyRow(self,setup):
        self.logger.info("*****Test_DeleteProduct_032*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("*****Login Successful******")

        self.logger.info("*****Staring Delete Product test*****")

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        #delete particular product by row

        self.editproduct = EditProductPage(self.driver)
        self.editproduct.clickEditProductByRow(2)

        self.editproduct.clickDelete()

        self.editproduct.confirmDelete()

        assert self.editproduct.isProductDeletedSuccessfully(), \
            "Product deletion success message was not displayed"

        self.logger.info("***** Product deleted successfully *****")






