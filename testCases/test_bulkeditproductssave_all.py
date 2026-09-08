import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchProductPage import SearchProduct
from pageObjects.BulkEditProductPage import BulkEditProductPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_BulkEditProductSaveAll_035:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_bulkeditproductssaveall(self, setup):

        self.logger.info("*** Test_BulkEditProductSaveAll_035 ***")

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # -------------------------------------------------
        # Login
        # -------------------------------------------------

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***** Login Successful *****")
        self.logger.info(
            "***** Starting Bulk Edit Product Save All Test *****"
        )

        # -------------------------------------------------
        # Navigate to Products
        # -------------------------------------------------

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        # -------------------------------------------------
        # Bulk Edit Products
        # -------------------------------------------------

        self.bulkedit = BulkEditProductPage(self.driver)

        self.bulkedit.clickBulkEditProducts()

        # -------------------------------------------------
        # Add New Product
        # -------------------------------------------------

        self.bulkedit.clickAddNew()

        product_name = self.bulkedit.setProductName()
        sku = self.bulkedit.setSKU()
        new_price = self.bulkedit.setNewPrice()
        old_price = self.bulkedit.setOldPrice()
        stock_quantity = self.bulkedit.setStockQuantity()

        self.logger.info(f"Product Name: {product_name}")
        self.logger.info(f"SKU: {sku}")
        self.logger.info(f"New Price: {new_price}")
        self.logger.info(f"Old Price: {old_price}")
        self.logger.info(f"Stock Quantity: {stock_quantity}")

        # -------------------------------------------------
        # Save All
        # -------------------------------------------------

        self.bulkedit.clickSaveAll()
        self.bulkedit.clickConfirmSaveAll()

        self.logger.info("Bulk Edit Save All completed")

        # -------------------------------------------------
        # Return to Products List
        # -------------------------------------------------

        self.bulkedit.clickBacktoProductsList()

        # -------------------------------------------------
        # Search Product
        # -------------------------------------------------

        self.searchproduct = SearchProduct(self.driver)

        self.searchproduct.setProductName(product_name)
        self.searchproduct.clickSearch()

        # -------------------------------------------------
        # Verify Product
        # -------------------------------------------------

        assert self.searchproduct.isProductPresent(product_name), \
            f"Product '{product_name}' was not found in search results"

        self.logger.info(
            f"Product '{product_name}' successfully found in Products table"
        )