
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        searchcust = SearchCustomer(self.driver)

        # -------------------------------------------------
        # Find customer by email and click Edit
        # -------------------------------------------------

        customer_email = "stark1@stark1.com"

        searchcust.clickEditCustomerByEmail(
            customer_email
        )

        self.logger.info(
            "******* Edit Customer button clicked *******"
        )

        # -------------------------------------------------
        # Wait for Edit Customer page
        # -------------------------------------------------

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.url_contains("/Admin/Customer/Edit")
        )

        assert "Edit customer" in self.driver.page_source

        self.logger.info(
            "******* Edit Customer page opened successfully *******"
        )

        # -------------------------------------------------
        # Edit Customer
        # -------------------------------------------------

        editcust = EditCustomerPage(self.driver)

        editcust.setFirstName("Johnny")

        self.logger.info(
            "******* First Name changed to Johnny *******"
        )

        # -------------------------------------------------
        # Save Customer
        # -------------------------------------------------

        editcust.clickSave()

        self.logger.info(
            "******* Save button clicked *******"
        )

        # -------------------------------------------------
        # Verify Success Message
        # -------------------------------------------------

        status = editcust.isUpdateSuccessMessageDisplayed()

        assert status, (
            "Customer update success message was not displayed"
        )

        self.logger.info(
            "********* Edit Customer test passed **********"
        )

        self.driver.close()

        self.logger.info(
            "****** Ending Edit Customer Test *******"
        )

