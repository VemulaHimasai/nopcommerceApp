import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.EditProductPage import EditProductPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_DeleteProduct_Select_034:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()


    @pytest.mark.regression
    def test_deleteproductselect(self, setup):
        self.logger.info("*****Test_DeleteProduct_Select_033*****")

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("*****Login Successful******")

        self.logger.info("*****Starting Delete Selected Product test*****")

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.editproduct = EditProductPage(self.driver)

        # Get product name from row 2 before deleting
        product_name = self.editproduct.getProductNameByRow(2)

        # Select product from row 2
        self.editproduct.selectProductCheckbox(2)

        # Click Delete Selected
        self.editproduct.clickDeleteSelected()

        # Confirm deletion
        self.editproduct.confirmselectedDelete()

        # Verify product is removed from table
        assert self.editproduct.isProductDeletedFromTable(product_name), \
            f"Product '{product_name}' was not deleted from the table"

        self.logger.info(
            f"***** Product '{product_name}' was deleted successfully *****"
        )




