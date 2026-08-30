import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.AddVendorPage import AddVendor
from pageObjects.SearchVendorPage import SearchVendorPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_EditVendor_015:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()


    def test_edit_vendor(self, setup):

        self.logger.info("******* Test_EditVendor_014 *******")

        self.driver = setup

        self.driver.get(self.baseURL)

        self.driver.maximize_window()

        self.driver.implicitly_wait(10)


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


        # Search Vendor

        searchvendor = SearchVendorPage(self.driver)

        old_vendor_name = "Vendor2"

        searchvendor.setName(old_vendor_name)

        searchvendor.clickSearch()


        # Verify vendor exists

        status = searchvendor.searchVendorByName(
            old_vendor_name
        )

        assert status is True

        self.logger.info(
            f"Vendor found: {old_vendor_name}"
        )


        # IMPORTANT: Click Edit button

        searchvendor.clickEditVendorByName(
            old_vendor_name
        )

        self.logger.info(
            "***** Clicked Edit Button *****"
        )


        # Edit Vendor Name

        new_vendor_name = "Vendor2_update"

        self.addvendor.editVendorName(
            new_vendor_name
        )

        self.logger.info(
            f"Vendor name changed to: {new_vendor_name}"
        )


        # Save changes

        self.addvendor.clickSave()


        self.logger.info(
            "***** Vendor Updated Successfully *****"
        )