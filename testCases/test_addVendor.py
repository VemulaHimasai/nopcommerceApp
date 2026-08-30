import time
import pytest
import string
import random
from selenium.webdriver.support.ui import WebDriverWait

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.AddVendorPage import AddVendor
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_012_AddVendor:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_addVendor(self, setup):

        self.logger.info(
            "******* Test_012_AddVendor *******"
        )

        self.driver = setup

        self.driver.get(self.baseURL)

        self.driver.maximize_window()

        self.driver.implicitly_wait(10)

        # Login
        self.lp = LoginPage(self.driver)

        self.lp.setUserName(
            self.username
        )

        self.lp.setPassword(
            self.password
        )

        self.lp.clickLogin()

        self.logger.info(
            "***** Login Successfully *****"
        )

        # Navigate to Vendors
        self.logger.info(
            "****** Starting Add Vendor Test ******"
        )

        self.addcust = AddCustomer(
            self.driver
        )

        self.addcust.clickOnCustomersMenu()

        self.addvendor = AddVendor(
            self.driver
        )

        self.addvendor.clickonVendorMenuItem()

        self.addvendor.clickonAddNew()

        self.logger.info(
            "****** Providing Vendor Info ******"
        )

        # Generate unique Vendor Name
        vendor_name = (
            "Vendor_"
            + str(int(time.time()))
        )

        self.addvendor.setVendorName(
            vendor_name
        )

        print(
            "Generated Vendor Name:",
            vendor_name
        )

        # Generate unique Vendor Email
        vendor_email = (
            random_generator()
            + "@gmail.com"
        )

        self.addvendor.setVendorEmail(
            vendor_email
        )

        print(
            "Generated Vendor Email:",
            vendor_email
        )

        # Vendor Description
        self.addvendor.setVendorDesc(
            "This is used for testing purpose"
        )

        # Save Vendor
        self.addvendor.clickSave()

        WebDriverWait(self.driver,15).until(
            lambda driver:"/Admin/Vendor/List" in driver.current_url)
        print("After Save URL: ",self.driver.current_url)
        print("After Save Title : ",self.driver.title)

        self.logger.info(f"After Save URL: {self.driver.current_url}")

        #Verify vendor was successfully created

        assert "/Admin/Vendor/List" in self.driver.current_url,\
        "Vendor was not redirected to Vendor List Page"

        self.logger.info("******Vendor added successfully******")

        print("Vendor added successfully")

def random_generator(
        size=8,
        chars=string.ascii_lowercase
        + string.digits
):

    return "".join(
        random.choice(chars)
        for _ in range(size)
    )