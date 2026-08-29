import time
import pytest
from selenium.webdriver.common.by import By

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer
from pageObjects.EditCustomerPage import EditCustomerPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_EditCustomer_010:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_edit_customer(self, setup):

        self.logger.info(
            "******* Editing Customer *******"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        # Login
        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "******* Login Successful *****"
        )

        # Navigate to Customers
        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        self.logger.info(
            "******* Customers page opened *******"
        )

        # Customers page object
        searchcust = SearchCustomer(self.driver)

        time.sleep(2)

        # Select customer and click Edit
        searchcust.clickEditCustomer(5)

        self.logger.info(
            "******* Edit Customer button clicked *******"
        )

        time.sleep(2)

        # Verify Edit Customer page
        assert "Edit customer" in self.driver.page_source

        self.logger.info(
            "******* Edit Customer page opened successfully *******"
        )

        # Edit Customer page object
        editcust = EditCustomerPage(self.driver)

        # Change First Name
        editcust.setFirstName("Johnny")

        # Save customer
        editcust.clickSave()

        # Verify success message
        msg = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        if "The customer has been updated successfully" in msg:

            self.logger.info(
                "********* Edit Customer test passed **********"
            )

        else:

            self.driver.save_screenshot(
                ".\\Screenshots\\test_editCustomer_scr.png"
            )

            self.logger.error(
                "********* Edit Customer test failed **********"
            )

            assert False

        self.driver.close()

        self.logger.info(
            "****** Ending Edit Customer Test *******"
        )