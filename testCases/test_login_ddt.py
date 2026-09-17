
import os

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException
)

from pageObjects.LoginPage import LoginPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import XLUtils


# =========================================================
# TEST CASE - LOGIN DDT
# =========================================================

class Test_002_DDT_Login:

    baseURL = ReadConfig.getApplicationURL()
    path = ".\\TestData\\LoginData.xlsx"

    logger = LogGen.loggen()

    # =====================================================
    # OPEN LOGIN PAGE
    # =====================================================

    def open_login_page(self):

        print("\n========================================")
        print("OPEN LOGIN PAGE")
        print("========================================")

        last_exception = None

        # -------------------------------------------------
        # Try loading login page maximum 2 times
        # -------------------------------------------------

        for attempt in range(1, 3):

            try:

                print(
                    f"Opening login page - attempt "
                    f"{attempt}/2"
                )

                # -------------------------------------------------
                # Navigate to application
                # -------------------------------------------------

                self.driver.get(
                    self.baseURL
                )

                # -------------------------------------------------
                # Wait until browser finishes loading page
                # -------------------------------------------------

                WebDriverWait(
                    self.driver,
                    20
                ).until(
                    lambda driver:
                    driver.execute_script(
                        "return document.readyState"
                    ) == "complete"
                )

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                print(
                    "Current Title:",
                    self.driver.title
                )

                # -------------------------------------------------
                # Wait for Email field
                # -------------------------------------------------

                WebDriverWait(
                    self.driver,
                    20
                ).until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            "Email"
                        )
                    )
                )

                print(
                    "Login Email field found."
                )

                return True

            except (
                TimeoutException,
                WebDriverException
            ) as e:

                last_exception = e

                print(
                    f"Login page attempt {attempt} failed."
                )

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                print(
                    "Current Title:",
                    self.driver.title
                )

                # -------------------------------------------------
                # Save screenshot for debugging
                # -------------------------------------------------

                try:

                    os.makedirs(
                        "Screenshots",
                        exist_ok=True
                    )

                    screenshot_path = (
                        "Screenshots/"
                        f"login_page_attempt_{attempt}.png"
                    )

                    self.driver.save_screenshot(
                        screenshot_path
                    )

                    print(
                        "Screenshot saved:",
                        screenshot_path
                    )

                except Exception as screenshot_error:

                    print(
                        "Screenshot failed:",
                        screenshot_error
                    )

                # -------------------------------------------------
                # Retry
                # -------------------------------------------------

                if attempt < 2:

                    try:

                        self.driver.refresh()

                    except Exception:
                        pass

        # ---------------------------------------------------------
        # Both attempts failed
        # ---------------------------------------------------------

        print(
            "\nLogin page could not be opened."
        )

        print(
            "Final URL:",
            self.driver.current_url
        )

        print(
            "Final Title:",
            self.driver.title
        )

        raise last_exception

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self, wait):

        print(
            "\n========================================"
        )

        print(
            "LOGOUT"
        )

        print(
            "========================================"
        )

        try:

            # -------------------------------------------------
            # Wait for Logout link to become clickable
            # -------------------------------------------------

            logout_link = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//a[@href='/logout']"
                    )
                )
            )

            # -------------------------------------------------
            # Scroll Logout link into view
            # -------------------------------------------------

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                logout_link
            )

            # -------------------------------------------------
            # Re-fetch Logout link
            # -------------------------------------------------

            logout_link = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//a[@href='/logout']"
                    )
                )
            )

            # -------------------------------------------------
            # Click Logout
            # -------------------------------------------------

            self.driver.execute_script(
                "arguments[0].click();",
                logout_link
            )

            print(
                "Logout clicked."
            )

            # =================================================
            # VERIFY LOGOUT
            # =================================================

            def logout_completed(driver):

                try:

                    current_url = (
                        driver.current_url
                        .rstrip("/")
                        .lower()
                    )

                    current_title = (
                        driver.title
                        .strip()
                        .lower()
                    )

                    # -------------------------------------------------
                    # IMPORTANT:
                    # Dashboard means logout has NOT completed.
                    # -------------------------------------------------

                    if (
                        current_url.endswith("/admin")
                        and
                        "dashboard / nopcommerce administration"
                        in current_title
                    ):

                        return False

                    # -------------------------------------------------
                    # Login page
                    # -------------------------------------------------

                    email_fields = driver.find_elements(
                        By.ID,
                        "Email"
                    )

                    if (
                        "/login" in current_url
                        and
                        len(email_fields) > 0
                    ):

                        return True

                    # -------------------------------------------------
                    # Storefront home page by title
                    # -------------------------------------------------

                    if (
                        current_title
                        == "your store. home page title"
                    ):

                        return True

                    # -------------------------------------------------
                    # Storefront URL
                    #
                    # baseURL normally contains /admin.
                    # Remove /admin before comparing.
                    # -------------------------------------------------

                    admin_url = (
                        self.baseURL
                        .rstrip("/")
                        .lower()
                    )

                    if admin_url.endswith("/admin"):

                        storefront_url = admin_url[
                            :-len("/admin")
                        ]

                        if current_url == storefront_url:

                            return True

                    return False

                except Exception:

                    return False

            # -------------------------------------------------
            # Wait for actual logout
            # -------------------------------------------------

            WebDriverWait(
                self.driver,
                20
            ).until(
                logout_completed
            )

            # =================================================
            # LOGOUT SUCCESS
            # =================================================

            print(
                "Logout completed successfully."
            )

            print(
                "Current URL after logout:",
                self.driver.current_url
            )

            print(
                "Current Title after logout:",
                self.driver.title
            )

            return True

        except Exception as e:

            self.logger.error(
                f"Logout failed: {e}"
            )

            print(
                "Logout failed:",
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

            # -------------------------------------------------
            # Save screenshot
            # -------------------------------------------------

            try:

                os.makedirs(
                    "Screenshots",
                    exist_ok=True
                )

                self.driver.save_screenshot(
                    "Screenshots/logout_failed.png"
                )

                print(
                    "Logout failure screenshot saved."
                )

            except Exception:
                pass

            return False

    # =====================================================
    # LOGIN DDT TEST
    # =====================================================

    @pytest.mark.regression
    def test_login_ddt(self, setup):

        self.logger.info(
            "**********Test_002_DDT_Login********"
        )

        self.logger.info(
            "********Verify Login DDT Test********"
        )

        self.driver = setup

        # -------------------------------------------------
        # Maximize browser
        # -------------------------------------------------

        self.driver.maximize_window()

        # -------------------------------------------------
        # Create explicit wait
        # -------------------------------------------------

        wait = WebDriverWait(
            self.driver,
            20
        )

        # =================================================
        # GET NUMBER OF EXCEL ROWS
        # =================================================

        self.rows = XLUtils.getRowCount(
            self.path,
            "Sheet1"
        )

        print(
            "Number of rows in Excel:",
            self.rows
        )

        # -------------------------------------------------
        # Store Pass / Fail result for every row
        # -------------------------------------------------

        lst_status = []

        # =================================================
        # READ EXCEL DATA
        # =================================================

        for r in range(
            2,
            self.rows + 1
        ):

            self.user = XLUtils.readData(
                self.path,
                "Sheet1",
                r,
                1
            )

            self.password = XLUtils.readData(
                self.path,
                "Sheet1",
                r,
                2
            )

            self.exp = XLUtils.readData(
                self.path,
                "Sheet1",
                r,
                3
            )

            print(
                "\n========================================"
            )

            print(
                f"Row {r}: Username={self.user}, "
                f"Expected={self.exp}"
            )

            print(
                "========================================"
            )

            # =================================================
            # OPEN LOGIN PAGE
            # =================================================

            try:

                self.open_login_page()

            except Exception as e:

                self.logger.error(
                    f"Row {r}: Login page could not be opened: {e}"
                )

                print(
                    f"Row {r}: Login page could not be opened."
                )

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                print(
                    "Current Title:",
                    self.driver.title
                )

                lst_status.append(
                    "Fail"
                )

                # -------------------------------------------------
                # Do not continue with unknown page
                # -------------------------------------------------

                break

            # =================================================
            # CREATE LOGIN PAGE OBJECT
            # =================================================

            self.lp = LoginPage(
                self.driver
            )

            # =================================================
            # ENTER USERNAME
            # =================================================

            self.lp.setUserName(
                self.user
            )

            # =================================================
            # ENTER PASSWORD
            # =================================================

            self.lp.setPassword(
                self.password
            )

            # =================================================
            # CLICK LOGIN
            # =================================================

            self.lp.clickLogin()

            # =================================================
            # WAIT FOR LOGIN RESULT
            # =================================================

            try:

                wait.until(
                    lambda driver:
                    driver.execute_script(
                        "return document.readyState"
                    ) == "complete"
                )

            except TimeoutException:

                print(
                    f"Row {r}: "
                    "Page did not reach complete state."
                )

            # -------------------------------------------------
            # Wait until either:
            #
            # 1. Dashboard is displayed
            #
            # OR
            #
            # 2. Login page remains displayed
            # -------------------------------------------------

            try:

                wait.until(
                    lambda driver:
                    (
                        "Dashboard / nopCommerce administration"
                        in driver.title
                    )
                    or
                    (
                        len(
                            driver.find_elements(
                                By.ID,
                                "Email"
                            )
                        ) > 0
                    )
                )

            except TimeoutException:

                print(
                    f"Row {r}: "
                    "Login result could not be determined."
                )

            # =================================================
            # GET ACTUAL TITLE
            # =================================================

            act_title = (
                self.driver.title.strip()
            )

            exp_title = (
                "Dashboard / nopCommerce administration"
            )

            print(
                f"Row {r}: Actual Title={act_title}, "
                f"Expected Result={self.exp}"
            )

            # =================================================
            # LOGIN VALIDATION
            # =================================================

            if act_title == exp_title:

                # =================================================
                # LOGIN SUCCESSFUL
                # =================================================

                if self.exp == "Pass":

                    self.logger.info(
                        f"Row {r}: *****Test Passed*****"
                    )

                    print(
                        f"Row {r}: *****Test Passed*****"
                    )

                    lst_status.append(
                        "Pass"
                    )

                elif self.exp == "Fail":

                    self.logger.error(
                        f"Row {r}: *****Test Failed*****"
                    )

                    print(
                        f"Row {r}: *****Test Failed*****"
                    )

                    lst_status.append(
                        "Fail"
                    )

                # =================================================
                # LOGOUT AFTER SUCCESSFUL LOGIN
                # =================================================

                logout_result = self.logout(
                    wait
                )

                if not logout_result:

                    lst_status.append(
                        "Fail"
                    )

            else:

                # =================================================
                # LOGIN UNSUCCESSFUL
                # =================================================

                if self.exp == "Fail":

                    self.logger.info(
                        f"Row {r}: *****Test Passed*****"
                    )

                    print(
                        f"Row {r}: *****Test Passed*****"
                    )

                    lst_status.append(
                        "Pass"
                    )

                elif self.exp == "Pass":

                    self.logger.error(
                        f"Row {r}: *****Test Failed*****"
                    )

                    print(
                        f"Row {r}: *****Test Failed*****"
                    )

                    lst_status.append(
                        "Fail"
                    )

        # =========================================================
        # FINAL TEST RESULT
        # =========================================================

        print(
            "\n========================================"
        )

        print(
            "FINAL DDT STATUS:",
            lst_status
        )

        print(
            "========================================"
        )

        # ---------------------------------------------------------
        # Make sure at least one Excel row was processed
        # ---------------------------------------------------------

        if (
            lst_status
            and
            "Fail" not in lst_status
        ):

            self.logger.info(
                "****Login DDT Test Passed****"
            )

            self.logger.info(
                "****End of Login DDT Test****"
            )

            self.logger.info(
                "*****Completed TC_LoginDDT_002******"
            )

            assert True

        else:

            self.logger.error(
                "****Login DDT Test Failed****"
            )

            self.logger.error(
                "****End of Login DDT Test****"
            )

            self.logger.error(
                "*****Completed TC_LoginDDT_002******"
            )

            assert False

        # ---------------------------------------------------------
        # Do NOT use driver.close() here.
        #
        # The setup fixture should handle browser cleanup.
        # ---------------------------------------------------------

