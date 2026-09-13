import os
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.BulkEditProductPage import BulkEditProductPage
from pageObjects.BulkEditProductSearchPage import BulkEditProductSearchPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_BulkEditSearchProductTypeGrouped_044:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_bulkeditsearch_producttype_grouped(self, setup):

        self.logger.info(
            "***** Test_BulkEditSearchProductTypeGrouped_044 Started *****"
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
        # OPEN PRODUCTS
        # =====================================================

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        # =====================================================
        # OPEN BULK EDIT PRODUCTS
        # =====================================================

        self.bulkedit = BulkEditProductPage(self.driver)

        self.bulkedit.clickBulkEditProducts()

        # =====================================================
        # BULK EDIT SEARCH PAGE
        # =====================================================

        self.bulkeditsearch = BulkEditProductSearchPage(
            self.driver
        )

        # =====================================================
        # SELECT PRODUCT TYPE
        # =====================================================

        self.bulkeditsearch.SelectByProductType(
            "Grouped (product with variants)"
        )

        # =====================================================
        # SCREENSHOT BEFORE SEARCH
        # =====================================================

        screenshot_dir = os.path.join(
            os.getcwd(),
            "Screenshots"
        )

        os.makedirs(
            screenshot_dir,
            exist_ok=True
        )

        before_search = os.path.join(
            screenshot_dir,
            "bulk_edit_producttype_grouped_before_search.png"
        )

        self.driver.save_screenshot(
            before_search
        )

        print(
            f"Screenshot saved: {before_search}"
        )

        # =====================================================
        # CLICK SEARCH
        # =====================================================

        self.bulkeditsearch.clickSearch()

        # =====================================================
        # SCREENSHOT AFTER SEARCH
        # =====================================================

        after_search = os.path.join(
            screenshot_dir,
            "bulk_edit_producttype_grouped_after_search.png"
        )

        self.driver.save_screenshot(
            after_search
        )

        print(
            f"Screenshot saved: {after_search}"
        )

        # =====================================================
        # VERIFY NO DATA
        # =====================================================

        assert self.bulkeditsearch.isNoDataAvailable(), (
            "Expected 'No data available in table' "
            "for Product Type: Grouped "
            "(product with variants)"
        )

        self.logger.info(
            "***** Product Type "
            "'Grouped (product with variants)' "
            "returned no products as expected *****"
        )

        print(
            "Product Type "
            "'Grouped (product with variants)' "
            "search successful. "
            "No data available as expected."
        )

        self.logger.info(
            "***** Test_BulkEditSearchProductTypeGrouped_044 "
            "Passed *****"
        )