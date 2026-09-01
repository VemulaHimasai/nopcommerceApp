
import os
import pytest
import string
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_003_AddCustomer:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.sanity
    def test_addCustomer(self, setup):

        self.logger.info(
            "********** Test_003_AddCustomer **********"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        wait = WebDriverWait(self.driver, 15)

        # -------------------------------------------------
        # Login
        # -------------------------------------------------

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "********* Login Successful **********"
        )

        # -------------------------------------------------
        # Navigate to Customers
        # -------------------------------------------------

        self.logger.info(
            "********* Starting Add Customer Test *********"
        )

        self.addcust = AddCustomer(self.driver)

        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        # -------------------------------------------------
        # Click Add New
        # -------------------------------------------------

        self.addcust.clickonAddNew()

        self.logger.info(
            "******** Providing customer information ********"
        )

        # -------------------------------------------------
        # Generate Unique Email
        # -------------------------------------------------

        self.email = random_generator() + "@gmail.com"

        print(
            "Generated email:",
            self.email
        )

        # -------------------------------------------------
        # Enter Email
        # -------------------------------------------------

        self.addcust.setEmail(self.email)

        email_field = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.addcust.txtEmail_xpath
                )
            )
        )

        actual_email = email_field.get_attribute("value")

        print(
            "Expected email:",
            repr(self.email)
        )

        print(
            "Actual email:",
            repr(actual_email)
        )

        assert actual_email == self.email, (
            f"Email mismatch. "
            f"Expected: {self.email}, "
            f"Actual: {actual_email}"
        )

        # -------------------------------------------------
        # Enter Password
        # -------------------------------------------------

        self.addcust.setPassword("test123")

        # -------------------------------------------------
        # Select Customer Role
        # -------------------------------------------------

        self.addcust.setCustomerRoles("Registered")

        # -------------------------------------------------
        # Verify Customer Role
        # -------------------------------------------------

        registered_role = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//li[contains(@class,'select2-selection__choice') "
                    "and @title='Registered']"
                )
            )
        )

        assert registered_role.is_displayed(), (
            "Registered customer role was not selected"
        )

        print(
            "Customer Role successfully selected: Registered"
        )

        # -------------------------------------------------
        # Other Customer Information
        # -------------------------------------------------

        self.addcust.setManagerofVendor("Vendor1")
        self.addcust.setGender("Female")
        self.addcust.setFirstName("Himasai")
        self.addcust.setLastName("V")
        self.addcust.setCompanyName("xxxxx")
        self.addcust.setAdminComment(
            "This is for testing purpose"
        )

        self.logger.info(
            "******** Customer information provided ********"
        )

        # -------------------------------------------------
        # Save Customer
        # -------------------------------------------------

        self.addcust.clickSave()

        self.logger.info(
            "******** Saving customer information ********"
        )

        # -------------------------------------------------
        # Verify Success / Error Message
        # -------------------------------------------------

        try:

            wait.until(
                lambda driver:
                driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.alert.alert-success"
                )
                or
                driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.alert.alert-danger"
                )
            )

            success_messages = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.alert.alert-success"
            )

            if success_messages:

                success_msg = success_messages[0].text.strip()

                print(
                    "Success message:",
                    success_msg
                )

                self.logger.info(
                    f"Success message: {success_msg}"
                )

                assert (
                    "customer has been added successfully"
                    in success_msg.lower()
                ), (
                    f"Unexpected success message: {success_msg}"
                )

                self.logger.info(
                    "******** Customer added successfully ********"
                )

            else:

                error_messages = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.alert.alert-danger"
                )

                error_msg = (
                    error_messages[0].text.strip()
                    if error_messages
                    else "Unknown error"
                )

                print(
                    "ERROR MESSAGE:",
                    error_msg
                )

                self.logger.error(
                    f"Customer creation failed: {error_msg}"
                )

                os.makedirs(
                    ".\\Screenshots",
                    exist_ok=True
                )

                self.driver.save_screenshot(
                    ".\\Screenshots\\test_addCustomer_scr.png"
                )

                pytest.fail(
                    f"Customer was not added successfully. "
                    f"Error: {error_msg}"
                )

        except Exception as e:

            os.makedirs(
                ".\\Screenshots",
                exist_ok=True
            )

            self.driver.save_screenshot(
                ".\\Screenshots\\test_addCustomer_scr.png"
            )

            self.logger.error(
                f"******** Add customer test failed ******** {e}"
            )

            raise

        # -------------------------------------------------
        # Navigate Back to Customers
        # -------------------------------------------------

        self.logger.info(
            "******** Verifying customer in Customers grid ********"
        )

        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        self.logger.info(
            "******** Customers page opened ********"
        )

        # -------------------------------------------------
        # Search Customer
        # -------------------------------------------------

        searchcust = SearchCustomer(self.driver)

        searchcust.setEmail(self.email)
        searchcust.clickSearch()

        self.logger.info(
            f"******** Searching for {self.email} ********"
        )

        # -------------------------------------------------
        # Verify Customer Exists in Grid
        # -------------------------------------------------

        try:

            customer_email_xpath = (
                f"//table[@id='customers-grid']"
                f"//tbody//td"
                f"[normalize-space()='{self.email}']"
            )

            # -------------------------------------------------
            # Wait for DataTable refresh and email to appear
            # -------------------------------------------------

            wait.until(
                EC.text_to_be_present_in_element(
                    (
                        By.XPATH,
                        customer_email_xpath
                    ),
                    self.email
                )
            )

            # -------------------------------------------------
            # IMPORTANT:
            # Locate the element again after DataTable refresh.
            # This prevents stale element reference errors.
            # -------------------------------------------------

            actual_grid_email = self.driver.find_element(
                By.XPATH,
                customer_email_xpath
            ).text.strip()

            print(
                "Expected grid email:",
                self.email
            )

            print(
                "Actual grid email:",
                actual_grid_email
            )

            # -------------------------------------------------
            # Validate Email
            # -------------------------------------------------

            assert actual_grid_email == self.email, (
                f"Customer email mismatch in grid. "
                f"Expected: {self.email}, "
                f"Actual: {actual_grid_email}"
            )

            print(
                "Customer found in grid:",
                self.email
            )

            self.logger.info(
                "******** Customer found in Customers grid ********"
            )

        except Exception as e:

            # -------------------------------------------------
            # Take Screenshot
            # -------------------------------------------------

            os.makedirs(
                ".\\Screenshots",
                exist_ok=True
            )

            self.driver.save_screenshot(
                ".\\Screenshots\\test_addCustomer_grid_scr.png"
            )

            # -------------------------------------------------
            # Debug Information
            # -------------------------------------------------

            print(
                "Customer was NOT found in Customers grid."
            )

            print(
                "Search email:",
                self.email
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Page title:",
                self.driver.title
            )

            # -------------------------------------------------
            # Print Grid Rows for Debugging
            # -------------------------------------------------

            try:

                rows = self.driver.find_elements(
                    By.XPATH,
                    "//table[@id='customers-grid']//tbody//tr"
                )

                print(
                    "Number of rows:",
                    len(rows)
                )

                for row in rows:

                    try:

                        print(
                            "ROW:",
                            row.text
                        )

                    except Exception as row_error:

                        print(
                            "Could not read row:",
                            row_error
                        )

            except Exception as grid_error:

                print(
                    "Could not read grid:",
                    grid_error
                )

            self.logger.error(
                f"Customer grid verification failed: {e}"
            )

            raise

        # -------------------------------------------------
        # Test Passed
        # -------------------------------------------------

        self.logger.info(
            "******** Add customer test passed ********"
        )


# ---------------------------------------------------------
# Random Email Generator
# ---------------------------------------------------------

def random_generator(
        size=8,
        chars=string.ascii_lowercase + string.digits
):
    return ''.join(
        random.choice(chars)
        for _ in range(size)
    )

