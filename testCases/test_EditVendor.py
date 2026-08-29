import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.AddVendorPage import AddVendor
from pageObjects.SearchVendorPage import SearchVendorPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_EditVendor_014:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_edit_vendor(self,setup):
        self.logger.info("******* Test_EditVendor_014 *******")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***********Login Successful**********")

        self.logger.info("**********Starting EditVendor_014**********")

        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()

        self.addvendor = AddVendor(self.driver)
        self.addvendor.clickonVendorMenuItem()

        self.logger.info("********edit vendor**********")
        searchvendor = SearchVendorPage(self.driver)
        old_vendor_name = "Vendor2"
        searchvendor.setName(old_vendor_name)
        searchvendor.clickSearch()

        status = searchvendor.searchVendorByName(old_vendor_name)

        assert status is True, "Vendor edit failed"

        self.logger.info(f"Vendor found: {old_vendor_name}")
        self.logger.info("*****Clicked Edit Button******")

        searchvendor.clickEditVendorByName(old_vendor_name)

        new_vendor_name = "Vendor2_update"
        self.addvendor.editVendorName(new_vendor_name)

        self.addvendor.clickSave()

        self.logger.info(f"Vendor name updated from {old_vendor_name} to {new_vendor_name}")

        print("Updated Vendor Name: ", new_vendor_name)
