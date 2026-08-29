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
            "**********Test_003_AddCustomer**********"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        # -------------------------------------------------
        # Login
        # -------------------------------------------------

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "*********Login Successful**********"
        )

        # -------------------------------------------------
        # Navigate to Customers
        # -------------------------------------------------

        self.logger.info(
            "*****Starting Add Customer Test*******"
        )

        self.addcust = AddCustomer(self.driver)

        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        # -------------------------------------------------
        # Click Add New
        # -------------------------------------------------

        self.addcust.clickonAddNew()

        self.logger.info(
            "********Providing customer info**********"
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

        # Verify email
        email_value = self.driver.find_element(
            By.XPATH,
            self.addcust.txtEmail_xpath
        ).get_attribute("value")

        print(
            "Expected email:",
            repr(self.email)
        )

        print(
            "Actual email:",
            repr(email_value)
        )

        print(
            "Email field value:",
            email_value
        )

        assert email_value == self.email

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

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//li[contains(@class,'select2-selection__choice') "
                    "and @title='Registered']"
                )
            )
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
            "********Customer information provided**********"
        )

        # -------------------------------------------------
        # Save Customer
        # -------------------------------------------------

        self.addcust.clickSave()

        self.logger.info(
            "********Saving customer info**********"
        )

        # -------------------------------------------------
        # Verify Success / Error Message
        # -------------------------------------------------

        try:

            WebDriverWait(
                self.driver,
                15
            ).until(
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

            # ---------------------------------------------
            # Check Success Message
            # ---------------------------------------------

            success_messages = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.alert.alert-success"
            )

            if success_messages:

                msg = success_messages[0].text

                print(
                    "Success message:",
                    msg
                )

                self.logger.info(
                    f"Success message: {msg}"
                )

                assert (
                    "customer has been added successfully"
                    in msg.lower()
                )

                self.logger.info(
                    "********Customer added successfully**********"
                )

            # ---------------------------------------------
            # Check Error Message
            # ---------------------------------------------

            else:

                error_messages = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.alert.alert-danger"
                )

                if error_messages:

                    error_msg = error_messages[0].text

                    print(
                        "ERROR MESSAGE:",
                        error_msg
                    )

                    self.logger.error(
                        f"Customer creation failed: {error_msg}"
                    )

                else:

                    print(
                        "No success or error message found."
                    )

                    print(
                        "Current URL:",
                        self.driver.current_url
                    )

                    print(
                        "Page title:",
                        self.driver.title
                    )

                    print(
                        "Page text:",
                        self.driver.find_element(
                            By.TAG_NAME,
                            "body"
                        ).text
                    )

                self.driver.save_screenshot(
                    ".\\Screenshots\\test_addCustomer_scr.png"
                )

                assert False, (
                    "Customer was not added successfully"
                )

        except Exception as e:

            self.driver.save_screenshot(
                ".\\Screenshots\\test_addCustomer_scr.png"
            )

            self.logger.error(
                f"********Add customer test failed********** {e}"
            )

            raise

        # -------------------------------------------------
        # Navigate Back to Customers
        # -------------------------------------------------

        self.logger.info(
            "********Verifying customer in Customers grid**********"
        )

        self.addcust.clickOnCustomersMenu()

        self.addcust.clickonCustomersMenuItem()

        self.logger.info(
            "********Customers page opened**********"
        )

        # -------------------------------------------------
        # Search Customer
        # -------------------------------------------------

        searchcust = SearchCustomer(self.driver)

        searchcust.setEmail(self.email)

        searchcust.clickSearch()

        self.logger.info(
            f"********Searching for {self.email}**********"
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

            WebDriverWait(
                self.driver,
                15
            ).until(
                lambda driver: any(
                    cell.text.strip() == self.email
                    for cell in driver.find_elements(
                        By.XPATH,
                        customer_email_xpath
                    )
                )
            )

            print(
                "Customer found in grid:",
                self.email
            )

            self.logger.info(
                "********Customer found in Customers grid**********"
            )

        except Exception as e:

            self.driver.save_screenshot(
                ".\\Screenshots\\test_addCustomer_grid_scr.png"
            )

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

            # ---------------------------------------------
            # Print Grid Rows for Debugging
            # ---------------------------------------------

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

                    print(
                        "ROW:",
                        row.text
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
            "********Add customer test passed**********"
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