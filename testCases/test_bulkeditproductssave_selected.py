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
            "*** Test_BulkEditProductSaveSelected_036 ***"
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
        # NAVIGATE TO PRODUCTS
        # =====================================================

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        # =====================================================
        # OPEN BULK EDIT
        # =====================================================

        self.bulkedit = BulkEditProductPage(self.driver)

        self.bulkedit.clickBulkEditProducts()

        # =====================================================
        # ADD NEW BULK EDIT ROW
        # =====================================================

        self.bulkedit.clickAddNew()

        product_name = self.bulkedit.setProductName()
        sku = self.bulkedit.setSKU()
        new_price = self.bulkedit.setNewPrice()
        old_price = self.bulkedit.setOldPrice()
        stock_quantity = self.bulkedit.setStockQuantity()

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
        # DEBUG - PRINT BULK EDIT ROWS
        # =====================================================

        self.bulkedit.printProductRows()

        # =====================================================
        # SELECT NEW PRODUCT
        # =====================================================

        self.bulkedit.selectProductByName(
            product_name
        )

        self.logger.info(
            f"Product '{product_name}' selected"
        )

        # =====================================================
        # SAVE SELECTED
        # =====================================================

        self.bulkedit.clickSaveSelected()

        self.bulkedit.clickConfirmSelected()

        self.logger.info(
            "Save Selected completed"
        )

        # =====================================================
        # RETURN TO PRODUCTS LIST
        # =====================================================

        self.bulkedit.clickBacktoProductsList()

        self.logger.info(
            "Returned to Products List"
        )

        # =====================================================
        # CREATE SEARCH PRODUCT PAGE
        # =====================================================

        self.searchproduct = SearchProduct(
            self.driver
        )

        # =====================================================
        # SEARCH PRODUCT
        # =====================================================

        self.searchproduct.setProductName(
            product_name
        )

        self.searchproduct.clickSearch()

        self.logger.info(
            f"Searching for product '{product_name}'"
        )

        self.searchproduct.printSearchResults()

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