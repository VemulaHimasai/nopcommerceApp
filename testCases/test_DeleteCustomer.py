import os
import pytest
import string
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from pageObjects.AddCustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer
from pageObjects.EditCustomerPage import EditCustomerPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_DeleteCustomer_011:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_delete_customer(self, setup):

        self.logger.info(
            "******* Deleting Customer *******"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        wait = WebDriverWait(
            self.driver,
            15
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

        # =================================================
        # Click Add New
        # =================================================

        self.addcust.clickonAddNew()

        self.logger.info(
            "******* Add Customer page opened *******"
        )

        # =================================================
        # Generate Unique Customer Email
        # =================================================

        customer_email = (
            random_generator()
            + "@gmail.com"
        )

        print(
            "\nGenerated customer email:",
            customer_email
        )

        self.logger.info(
            f"Generated customer email: {customer_email}"
        )

        # =================================================
        # Enter Email
        # =================================================

        self.addcust.setEmail(
            customer_email
        )

        # =================================================
        # Enter Password
        # =================================================

        self.addcust.setPassword(
            "test123"
        )

        # =================================================
        # Select Customer Role
        # =================================================

        self.addcust.setCustomerRoles(
            "Registered"
        )

        # =================================================
        # Customer Information
        # =================================================

        self.addcust.setManagerofVendor(
            "Vendor1"
        )

        self.addcust.setGender(
            "Female"
        )

        self.addcust.setFirstName(
            "DeleteTest"
        )

        self.addcust.setLastName(
            "Customer"
        )

        self.addcust.setCompanyName(
            "xxxxx"
        )

        self.addcust.setAdminComment(
            "Customer created for delete test"
        )

        self.logger.info(
            "******* Customer information entered *******"
        )

        # =================================================
        # Save Customer
        # =================================================

        self.addcust.clickSave()

        self.logger.info(
            "******* Customer save initiated *******"
        )

        # =================================================
        # Verify Customer Added Successfully
        # =================================================

        success_message_xpath = (
            "//div[contains(@class,'alert-success') "
            "and contains("
            "translate(normalize-space(.),"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),"
            "'customer has been added successfully'"
            ")]"
        )

        try:

            success_message = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        success_message_xpath
                    )
                )
            )

            message = success_message.text.strip()

            print(
                "Add customer success message:",
                repr(message)
            )

            assert (
                "customer has been added successfully"
                in message.lower()
            ), (
                "Customer was not added successfully. "
                f"Message: {message}"
            )

            self.logger.info(
                "******* Customer added successfully *******"
            )

        except Exception as e:

            print(
                "Customer creation failed:",
                e
            )

            os.makedirs(
                ".\\Screenshots",
                exist_ok=True
            )

            self.driver.save_screenshot(
                ".\\Screenshots\\test_deleteCustomer_add_scr.png"
            )

            raise

        # =================================================
        # Navigate Back to Customer List
        # =================================================

        self.addcust.clickOnCustomersMenu()

        self.addcust.clickonCustomersMenuItem()

        self.logger.info(
            "******* Customers list opened *******"
        )

        # =================================================
        # Search Newly Created Customer
        # =================================================

        searchcust = SearchCustomer(
            self.driver
        )

        searchcust.setEmail(
            customer_email
        )

        searchcust.clickSearch()

        self.logger.info(
            f"******* Searching for {customer_email} *******"
        )

        # =================================================
        # Verify Customer Exists in Grid
        # =================================================

        customer_email_xpath = (
            "//table[@id='customers-grid']"
            "//tbody//td"
            f"[normalize-space()='{customer_email}']"
        )

        try:

            def customer_email_found(driver):

                try:

                    elements = driver.find_elements(
                        By.XPATH,
                        customer_email_xpath
                    )

                    for element in elements:

                        try:

                            if (
                                element.is_displayed()
                                and
                                element.text.strip()
                                == customer_email
                            ):
                                return True

                        except Exception:
                            continue

                    return False

                except Exception:
                    return False

            wait.until(
                customer_email_found
            )

            print(
                "Customer found in grid:",
                customer_email
            )

            self.logger.info(
                "******* Customer found in grid *******"
            )

        except Exception as e:

            print(
                "Newly created customer was not found:",
                customer_email
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Page title:",
                self.driver.title
            )

            os.makedirs(
                ".\\Screenshots",
                exist_ok=True
            )

            self.driver.save_screenshot(
                ".\\Screenshots\\test_deleteCustomer_search_scr.png"
            )

            raise

        # =================================================
        # Find Customer and Click Edit
        # =================================================

        searchcust.clickEditCustomerByEmail(
            customer_email
        )

        self.logger.info(
            "******* Edit Customer button clicked *******"
        )

        # =================================================
        # Wait for Edit Customer Page
        # =================================================

        wait.until(
            EC.url_contains(
                "/Admin/Customer/Edit"
            )
        )

        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(normalize-space(.),"
                    "'Edit customer')]"
                )
            )
        )

        print(
            "Edit Customer page opened:"
        )

        print(
            self.driver.current_url
        )

        self.logger.info(
            "******* Edit Customer page opened successfully *******"
        )

        # =================================================
        # Create Edit Customer Page Object
        # =================================================

        editcust = EditCustomerPage(
            self.driver
        )

        # =================================================
        # Click Delete
        # =================================================

        editcust.clickDelete()

        self.logger.info(
            "******* Delete Customer button clicked *******"
        )

        # =================================================
        # Confirm Delete
        # =================================================

        editcust.confirmDelete()

        self.logger.info(
            "******* Customer List page opened after Delete *******"
        )

        # =================================================
        # Wait for Customer Grid
        # =================================================

        searchcust.waitForTable()

        # =================================================
        # Verify Customer Deleted
        # =================================================

        deleted = searchcust.isCustomerDeleted(
            customer_email
        )

        print(
            "\nCustomer deletion result:",
            deleted
        )

        assert deleted is True, (
            f"Customer '{customer_email}' "
            "was not deleted from the customer grid."
        )

        self.logger.info(
            "******* Customer deletion verified in grid *******"
        )

        # =================================================
        # Verify Delete Success Message
        # =================================================

        success_delete_message_xpath = (
            "//div[contains(@class,'alert-success') "
            "and contains("
            "translate(normalize-space(.),"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),"
            "'customer has been deleted successfully'"
            ")]"
        )

        try:

            success_message = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        success_delete_message_xpath
                    )
                )
            )

            message = success_message.text.strip()

            print(
                "Delete success message:",
                repr(message)
            )

            assert (
                "customer has been deleted successfully"
                in message.lower()
            ), (
                "Unexpected delete success message: "
                f"{message}"
            )

            self.logger.info(
                "******* Delete success message verified *******"
            )

        except Exception as e:

            self.logger.error(
                f"Delete success message verification failed: {e}"
            )

            os.makedirs(
                ".\\Screenshots",
                exist_ok=True
            )

            self.driver.save_screenshot(
                ".\\Screenshots\\test_deleteCustomer_scr.png"
            )

            raise

        # =================================================
        # Test Passed
        # =================================================

        self.logger.info(
            "********* Delete Customer test passed **********"
        )

        print(
            "\n========================================"
        )

        print(
            "DELETE CUSTOMER TEST PASSED"
        )

        print(
            "Deleted customer:",
            customer_email
        )

        print(
            "========================================"
        )


# =========================================================
# Random Email Generator
# =========================================================

def random_generator(
        size=8,
        chars=string.ascii_lowercase + string.digits
):

    return ''.join(
        random.choice(chars)
        for _ in range(size)
    )