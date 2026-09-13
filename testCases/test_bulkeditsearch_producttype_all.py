import os
import time
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.BulkEditProductPage import BulkEditProductPage
from pageObjects.BulkEditProductSearchPage import BulkEditProductSearchPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_BulkEditSearchProductTypeAll_039:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_bulkeditsearch_producttype_all(self, setup):

        self.logger.info(
            "***** Test_BulkEditSearchProductTypeAll_039 *****"
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

        self.bulkeditsearch.SelectByProductType("All")

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
            "bulk_edit_before_search.png"
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
        # ALLOW AJAX TABLE TO STABILIZE
        # =====================================================

        time.sleep(2)

        # =====================================================
        # SCREENSHOT AFTER SEARCH
        # =====================================================

        after_search = os.path.join(
            screenshot_dir,
            "bulk_edit_after_search.png"
        )

        self.driver.save_screenshot(
            after_search
        )

        print(
            f"Screenshot saved: {after_search}"
        )

        # =====================================================
        # GET SEARCH RESULTS
        # =====================================================

        rows = (
            self.bulkeditsearch.getSearchResults()
        )

        # =====================================================
        # VERIFY RESULTS
        # =====================================================

        assert len(rows) > 0, (
            "No products found for "
            "Product Type: All"
        )

        self.logger.info(
            f"***** Product Type 'All' search "
            f"returned {len(rows)} products *****"
        )

        print(
            f"Product Type 'All' search successful. "
            f"Rows found: {len(rows)}"
        )