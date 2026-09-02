import pytest
import time

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.SearchVendorPage import SearchVendorPage
from pageObjects.AddVendorPage import AddVendor
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_EditVendor_015:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_edit_vendor(self, setup):

        self.logger.info("******* Test_EditVendor_015 *******")

        self.driver = setup

        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # Login
        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("*********** Login Successful **********")

        # Navigate to Vendors
        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.addvendor = AddVendor(self.driver)
        self.addvendor.clickonVendorMenuItem()

        self.logger.info("******** Starting Edit Vendor Test ********")

        # Search all vendors
        searchvendor = SearchVendorPage(self.driver)

        searchvendor.setName("")
        searchvendor.clickSearch()

        time.sleep(2)

        # Get first available vendor dynamically
        old_vendor_name = searchvendor.getFirstVendorName()

        self.logger.info(
            f"Vendor selected for editing: {old_vendor_name}"
        )

        assert old_vendor_name is not None, (
            "No vendors available in the vendor table"
        )

        # Verify vendor exists
        status = searchvendor.searchVendorByName(
            old_vendor_name
        )

        assert status is True, (
            f"Vendor '{old_vendor_name}' was not found"
        )

        self.logger.info(
            f"Vendor '{old_vendor_name}' found successfully"
        )

        # Continue your existing edit operation below