import time
import pytest
import string
import random

from selenium.webdriver.common.by import By
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

        # Wait for Success or Error Message
        WebDriverWait(
            self.driver,
            10
        ).until(
            lambda driver:
            driver.find_elements(
                By.CSS_SELECTOR,
                "div.alert.alert-success"
            )
            or driver.find_elements(
                By.CSS_SELECTOR,
                "div.alert.alert-danger"
            )
        )

        success_msgs = (
            self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.alert.alert-success"
            )
        )

        error_msgs = (
            self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.alert.alert-danger"
            )
        )

        if success_msgs:

            msg = success_msgs[0].text

            print(
                "Success Message:",
                msg
            )

            self.logger.info(
                f"Success Message: {msg}"
            )

            assert (
                "vendor" in msg.lower()
            )

            self.logger.info(
                "***** Vendor Added Successfully *****"
            )

        elif error_msgs:

            msg = error_msgs[0].text

            print(
                "Error Message:",
                msg
            )

            self.logger.error(
                f"Vendor was not added: {msg}"
            )

            pytest.fail(
                f"Vendor creation failed: {msg}"
            )


def random_generator(
        size=8,
        chars=string.ascii_lowercase
        + string.digits
):

    return "".join(
        random.choice(chars)
        for _ in range(size)
    )