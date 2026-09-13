import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        self.driver.maximize_window()

        # -------------------------------------------------
        # Get number of rows from Excel
        # -------------------------------------------------

        self.rows = XLUtils.getRowCount(
            self.path,
            "Sheet1"
        )

        print(
            "Number of rows in Excel:",
            self.rows
        )

        lst_status = []

        # -------------------------------------------------
        # Read Excel data
        # -------------------------------------------------

        for r in range(2, self.rows + 1):

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
                f"Row {r}: Username={self.user}, "
                f"Expected={self.exp}"
            )

            # -------------------------------------------------
            # Open login page for every Excel row
            # -------------------------------------------------

            self.driver.get(
                self.baseURL
            )

            wait = WebDriverWait(
                self.driver,
                10
            )

            # -------------------------------------------------
            # Wait until Email field is visible
            # -------------------------------------------------

            wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "Email")
                )
            )

            self.lp = LoginPage(
                self.driver
            )

            # -------------------------------------------------
            # Enter username
            # -------------------------------------------------

            self.lp.setUserName(
                self.user
            )

            # -------------------------------------------------
            # Enter password
            # -------------------------------------------------

            self.lp.setPassword(
                self.password
            )

            # -------------------------------------------------
            # Click Login
            # -------------------------------------------------

            self.lp.clickLogin()

            # -------------------------------------------------
            # Give nopCommerce time to process login
            # -------------------------------------------------

            time.sleep(2)

            # -------------------------------------------------
            # Get actual title
            # -------------------------------------------------

            act_title = self.driver.title

            exp_title = (
                "Dashboard / nopCommerce administration"
            )

            print(
                f"Row {r}: Actual Title={act_title}, "
                f"Expected Result={self.exp}"
            )

            # =================================================
            # VALIDATION
            # =================================================

            if act_title == exp_title:

                # -------------------------------------------------
                # Login successful
                # -------------------------------------------------

                if self.exp == "Pass":

                    self.logger.info(
                        f"Row {r}: *****Test Passed*****"
                    )

                    lst_status.append(
                        "Pass"
                    )

                elif self.exp == "Fail":

                    self.logger.error(
                        f"Row {r}: *****Test Failed*****"
                    )

                    lst_status.append(
                        "Fail"
                    )

                # =================================================
                # LOGOUT
                # =================================================

                try:

                    # -------------------------------------------------
                    # Wait for modal backdrop if present
                    # -------------------------------------------------

                    try:

                        wait.until(
                            EC.invisibility_of_element_located(
                                (
                                    By.CSS_SELECTOR,
                                    ".modal-backdrop"
                                )
                            )
                        )

                    except Exception:
                        pass

                    # -------------------------------------------------
                    # Wait for Logout link
                    # -------------------------------------------------

                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//a[@href='/logout']"
                            )
                        )
                    )

                    # -------------------------------------------------
                    # Find Logout link
                    # -------------------------------------------------

                    logout_link = self.driver.find_element(
                        By.XPATH,
                        "//a[@href='/logout']"
                    )

                    # -------------------------------------------------
                    # Scroll Logout link into view
                    # -------------------------------------------------

                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        logout_link
                    )

                    # -------------------------------------------------
                    # Re-fetch Logout link
                    # -------------------------------------------------

                    logout_link = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//a[@href='/logout']"
                            )
                        )
                    )

                    # -------------------------------------------------
                    # JavaScript click
                    # -------------------------------------------------

                    self.driver.execute_script(
                        "arguments[0].click();",
                        logout_link
                    )

                    print(
                        "Logout clicked"
                    )

                    # =================================================
                    # VERIFY LOGOUT
                    # =================================================
                    #
                    # nopCommerce redirects to the storefront
                    # home page after logout.
                    #
                    # URL:
                    # https://localhost:59579/
                    #
                    # Title:
                    # Your store. Home page title
                    # =================================================

                    def logout_completed(driver):

                        try:

                            current_url = (
                                driver.current_url.lower()
                            )

                            current_title = (
                                driver.title.strip().lower()
                            )

                            # Home page after logout
                            if (
                                current_url.rstrip("/")
                                == self.baseURL.rstrip("/").lower()
                            ):
                                return True

                            if (
                                current_title
                                == "your store. home page title"
                            ):
                                return True

                            return False

                        except Exception:

                            return False

                    wait.until(
                        logout_completed
                    )

                    print(
                        "Logout completed successfully"
                    )

                    print(
                        "Current URL after logout:",
                        self.driver.current_url
                    )

                    print(
                        "Current Title after logout:",
                        self.driver.title
                    )

                except Exception as e:

                    self.logger.error(
                        f"Row {r}: Logout failed: {e}"
                    )

                    print(
                        f"Row {r}: Logout failed: {e}"
                    )

                    print(
                        "Current URL after logout attempt:",
                        self.driver.current_url
                    )

                    print(
                        "Current Title after logout attempt:",
                        self.driver.title
                    )

                    lst_status.append(
                        "Fail"
                    )

            else:

                # -------------------------------------------------
                # Login unsuccessful
                # -------------------------------------------------

                if self.exp == "Fail":

                    self.logger.info(
                        f"Row {r}: *****Test Passed*****"
                    )

                    lst_status.append(
                        "Pass"
                    )

                elif self.exp == "Pass":

                    self.logger.error(
                        f"Row {r}: *****Test Failed*****"
                    )

                    lst_status.append(
                        "Fail"
                    )

        # =========================================================
        # FINAL TEST RESULT
        # =========================================================

        if "Fail" not in lst_status:

            self.logger.info(
                "****Login DDT Test Passed****"
            )

            self.driver.close()

            assert True

        else:

            self.logger.error(
                "****Login DDT Test Failed****"
            )

            self.driver.close()

            assert False

        self.logger.info(
            "****End of Login DDT Test****"
        )

        self.logger.info(
            "*****Completed TC_LoginDDT_002******"
        )