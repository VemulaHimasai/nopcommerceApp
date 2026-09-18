
import os

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from pageObjects.AddCustomerPage import AddCustomer
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

        self.driver.get(
            self.baseURL
        )

        self.driver.maximize_window()

        wait = WebDriverWait(
            self.driver,
            20
        )

        # =================================================
        # Login
        # =================================================

        self.lp = LoginPage(
            self.driver
        )

        self.lp.setUserName(
            self.username
        )

        self.lp.setPassword(
            self.password
        )

        self.lp.clickLogin()

        self.logger.info(
            "******* Login Successful *****"
        )

        # =================================================
        # Navigate to Customers
        # =================================================

        self.addcust = AddCustomer(
            self.driver
        )

        self.addcust.clickOnCustomersMenu()

        self.addcust.clickonCustomersMenuItem()

        self.logger.info(
            "******* Customers page opened *******"
        )

        searchcust = SearchCustomer(
            self.driver
        )

        # =================================================
        # Find customer by email and click Edit
        # =================================================

        customer_email = (
            "stark1@stark1.com"
        )

        searchcust.clickEditCustomerByEmail(
            customer_email
        )

        self.logger.info(
            "******* Edit Customer button clicked *******"
        )

        # =================================================
        # Wait for Edit Customer page
        # =================================================

        wait.until(
            EC.url_contains(
                "/Admin/Customer/Edit"
            )
        )

        wait.until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    editcust.txtFirstName_id
                )
            )
        ) if False else None

        assert "Edit customer" in (
            self.driver.page_source
        )

        self.logger.info(
            "******* Edit Customer page opened successfully *******"
        )

        # =================================================
        # Create Edit Customer page object
        # =================================================

        editcust = EditCustomerPage(
            self.driver
        )

        # =================================================
        # Edit Customer
        # =================================================

        editcust.setFirstName(
            "Johnny"
        )

        # =================================================
        # Save Customer
        # =================================================

        editcust.clickSave()

        self.logger.info(
            "******* Customer Save button clicked *******"
        )

        # =================================================
        # IMPORTANT:
        # nopCommerce redirects to Customer List
        # after successful save.
        # =================================================

        try:

            wait.until(
                EC.url_contains(
                    "/Admin/Customer/List"
                )
            )

            print(
                "Customer List redirect detected."
            )

            print(
                "Current URL after Save:",
                self.driver.current_url
            )

            print(
                "Current Title after Save:",
                self.driver.title
            )

        except Exception as e:

            self.logger.error(
                f"Customer List redirect failed: {e}"
            )

            print(
                "Customer List redirect failed:",
                e
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Current Title:",
                self.driver.title
            )

            try:

                os.makedirs(
                    "Screenshots",
                    exist_ok=True
                )

                self.driver.save_screenshot(
                    ".\\Screenshots\\edit_customer_redirect_failure.png"
                )

                print(
                    "Redirect failure screenshot saved."
                )

            except Exception as screenshot_error:

                print(
                    "Unable to save screenshot:",
                    screenshot_error
                )

            assert False, (
                "Customer List page was not opened "
                "after saving customer."
            )

        # =================================================
        # Verify update success message
        # =================================================

        status = (
            editcust.isCustomerUpdatedSuccessfully()
        )

        assert status is True, (
            "Customer update success message "
            "was not found."
        )

        self.logger.info(
            "******* Customer update success message verified *******"
        )

        # =================================================
        # Wait for Customer Grid
        # =================================================

        searchcust.waitForTable()

        self.logger.info(
            "******* Customer List grid loaded *******"
        )

        # =================================================
        # Verify updated customer in grid
        # =================================================

        updated = (
            searchcust.isCustomerNameUpdated(
                customer_email,
                "Johnny James"
            )
        )

        assert updated is True, (
            f"Customer '{customer_email}' was not updated "
            f"to 'Johnny James' in the customer grid."
        )

        self.logger.info(
            "******* Updated customer verified in grid *******"
        )

        self.logger.info(
            "********* Edit Customer test passed **********"
        )

