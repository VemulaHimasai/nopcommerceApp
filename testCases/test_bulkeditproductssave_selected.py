import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchProductPage import SearchProduct
from pageObjects.BulkEditProductPage import BulkEditProductPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_BulkEditProductSaveSelected_036:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_bulkeditproductssaveselected(self, setup):

        self.logger.info(
            "*** Test_BulkEditProductSaveSelected_035 ***"
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

        self.logger.info(
            "***** Starting Bulk Edit Product Save Selected Test *****"
        )

        # =====================================================
        # NAVIGATE TO PRODUCTS
        # =====================================================

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        # =====================================================
        # BULK EDIT PRODUCTS
        # =====================================================

        self.bulkedit = BulkEditProductPage(self.driver)

        self.bulkedit.clickBulkEditProducts()

        # =====================================================
        # ADD PRODUCT
        # =====================================================

        self.bulkedit.clickAddNew()

        product_name = self.bulkedit.setProductName()
        sku = self.bulkedit.setSKU()
        new_price = self.bulkedit.setNewPrice()
        old_price = self.bulkedit.setOldPrice()
        stock_quantity = self.bulkedit.setStockQuantity()

        # Debug information
        self.bulkedit.printProductRows()

        self.logger.info(
            f"Product Name: {product_name}"
        )

        self.logger.info(
            f"SKU: {sku}"
        )

        self.logger.info(
            f"New Price: {new_price}"
        )

        self.logger.info(
            f"Old Price: {old_price}"
        )

        self.logger.info(
            f"Stock Quantity: {stock_quantity}"
        )

        # =====================================================
        # SELECT PRODUCT
        # =====================================================

        self.bulkedit.selectProductByName(
            product_name
        )

        self.logger.info(
            f"Product '{product_name}' selected for Save Selected"
        )

        # =====================================================
        # SAVE SELECTED
        # =====================================================

        self.bulkedit.clickSaveSelected()

        self.bulkedit.clickConfirmSelected()

        self.logger.info(
            "Bulk Edit Save Selected completed"
        )

        # =====================================================
        # RETURN TO PRODUCTS LIST
        # =====================================================

        self.bulkedit.clickBacktoProductsList()

        # =====================================================
        # SEARCH PRODUCT
        # =====================================================

        self.searchproduct = SearchProduct(
            self.driver
        )

        self.searchproduct.setProductName(
            product_name
        )

        self.searchproduct.clickSearch()

        # =====================================================
        # VERIFY PRODUCT
        # =====================================================

        assert self.searchproduct.isProductPresent(
            product_name
        ), (
            f"Product '{product_name}' "
            "was not found in search results"
        )

        self.logger.info(
            f"Product '{product_name}' "
            "successfully found in Products table"
        )