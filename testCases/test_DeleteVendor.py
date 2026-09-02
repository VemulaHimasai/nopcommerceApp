import pytest

from pageObjects.AddVendorPage import AddVendor
from pageObjects.LoginPage import LoginPage
from pageObjects.SearchVendorPage import SearchVendorPage
from pageObjects.AddcustomerPage import AddCustomer
from utilities.readproperties import ReadConfig


@pytest.mark.regression
class Test_DeleteVendor_016:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    def test_delete_vendor(self, setup):

        self.driver = setup

        # =================================================
        # LOGIN PAGE
        # =================================================

        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        print("Login successful")

        # =================================================
        # OPEN CUSTOMERS MENU
        # =================================================

        self.addcust = AddCustomer(self.driver)

        self.addcust.clickOnCustomersMenu()

        print("Customers menu opened")

        # =================================================
        # OPEN VENDOR MENU
        # =================================================

        self.addvendor = AddVendor(self.driver)

        self.addvendor.clickonVendorMenuItem()

        print(
            "Vendor list page opened:",
            self.driver.current_url
        )

        # =================================================
        # VENDOR PAGE
        # =================================================

        self.vendorPage = SearchVendorPage(self.driver)

        self.vendorPage.waitForVendorList()

        # =================================================
        # SELECT PARTICULAR VENDOR
        # =================================================

        # Overall row number across ALL pages
        #
        # Example:
        # 1  = first vendor
        # 10 = tenth vendor
        # 11 = first vendor on page 2
        # 15 = fifth vendor on page 2
        # 21 = first vendor on page 3

        row_number = 12

        print(
            "Selecting vendor overall row:",
            row_number
        )

        # =================================================
        # GET VENDOR NAME
        # =================================================

        vendor_name = (
            self.vendorPage.getVendorNameByOverallRow(
                row_number
            )
        )

        assert vendor_name is not None, (
            f"Vendor overall row {row_number} "
            f"was not found"
        )

        print(
            "Vendor selected:",
            vendor_name
        )

        # =================================================
        # OPEN EDIT PAGE
        # =================================================

        self.vendorPage.clickEditVendorByOverallRow(
            row_number
        )

        print(
            "Edit page opened for:",
            vendor_name
        )

        # =================================================
        # DELETE VENDOR
        # =================================================

        self.vendorPage.clickDeleteButton()

        print("Delete button clicked")

        # =================================================
        # CONFIRM DELETE
        # =================================================

        self.vendorPage.clickConfirmDelete()

        print("Delete confirmed")

        # =================================================
        # VERIFY SUCCESS MESSAGE
        # =================================================

        success_message = (
            self.vendorPage.getSuccessMessage()
        )

        print(
            "Success message:",
            success_message
        )

        assert (
            "The vendor has been deleted successfully."
            in success_message
        ), (
            "Vendor deletion success message "
            "not found"
        )

        print(
            "Vendor deleted successfully:",
            vendor_name
        )