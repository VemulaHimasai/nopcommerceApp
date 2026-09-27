import os

import pytest
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import XLUtils


class Test_002_DDT_Login:
    baseURL = ReadConfig.getApplicationURL()
    path = ".\\TestData\\LoginData.xlsx"
    logger = LogGen.loggen()

    def open_login_page(self):
        last_exception = None

        for attempt in range(1, 3):
            try:
                print(f"\nOpening login page - Attempt {attempt}")

                self.driver.get(self.baseURL)

                WebDriverWait(self.driver, 20).until(
                    lambda driver: driver.execute_script(
                        "return document.readyState"
                    ) == "complete"
                )

                print(f"Current URL: {self.driver.current_url}")
                print(f"Current Title: {self.driver.title}")

                # Check if already logged in
                if (
                    "dashboard / nopcommerce administration"
                    in self.driver.title.lower()
                ):
                    print("Already logged in. Logging out first.")

                    try:
                        logout_link = WebDriverWait(
                            self.driver,
                            10
                        ).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//a[@href='/logout']")
                            )
                        )

                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});",
                            logout_link
                        )

                        logout_link = self.driver.find_element(
                            By.XPATH,
                            "//a[@href='/logout']"
                        )

                        self.driver.execute_script(
                            "arguments[0].click();",
                            logout_link
                        )

                        WebDriverWait(
                            self.driver,
                            15
                        ).until(
                            EC.presence_of_element_located(
                                (By.ID, "Email")
                            )
                        )

                        print("Successfully logged out.")

                    except Exception as logout_error:
                        print(
                            f"Logout failed: {logout_error}"
                        )

                        admin_url = self.baseURL.rstrip("/")

                        if admin_url.lower().endswith("/admin"):
                            login_url = (
                                admin_url[:-len("/admin")]
                                + "/login"
                            )
                        else:
                            login_url = admin_url + "/login"

                        print(
                            f"Navigating directly to login URL: "
                            f"{login_url}"
                        )

                        self.driver.get(login_url)

                # If login page is not detected, navigate directly
                if not self.driver.find_elements(By.ID, "Email"):
                    admin_url = self.baseURL.rstrip("/")

                    if admin_url.lower().endswith("/admin"):
                        login_url = (
                            admin_url[:-len("/admin")]
                            + "/login"
                        )
                    else:
                        login_url = admin_url + "/login"

                    print(
                        f"Login page not detected."
                    )
                    print(
                        f"Navigating directly to: {login_url}"
                    )

                    self.driver.get(login_url)

                WebDriverWait(
                    self.driver,
                    20
                ).until(
                    EC.visibility_of_element_located(
                        (By.ID, "Email")
                    )
                )

                print("Login page opened successfully.")
                print(
                    f"Login URL: {self.driver.current_url}"
                )

                return True

            except (
                TimeoutException,
                WebDriverException
            ) as e:

                last_exception = e

                print(
                    f"Login page attempt {attempt} failed: "
                    f"{type(e).__name__}: {e}"
                )

                try:
                    os.makedirs(
                        "Screenshots",
                        exist_ok=True
                    )

                    self.driver.save_screenshot(
                        f"Screenshots/"
                        f"login_page_attempt_{attempt}.png"
                    )

                except Exception:
                    pass

                if attempt < 2:
                    try:
                        self.driver.refresh()
                    except Exception:
                        pass

        if last_exception:
            raise last_exception

        raise Exception(
            "Unable to open login page."
        )

    def logout(self, wait):
        try:
            print("Attempting logout...")

            logout_link = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[@href='/logout']")
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                logout_link
            )

            logout_link = self.driver.find_element(
                By.XPATH,
                "//a[@href='/logout']"
            )

            self.driver.execute_script(
                "arguments[0].click();",
                logout_link
            )

            def logout_completed(driver):
                try:
                    current_url = driver.current_url.lower()
                    current_title = driver.title.strip().lower()

                    if (
                        current_url.rstrip("/").endswith("/admin")
                        and
                        "dashboard / nopcommerce administration"
                        in current_title
                    ):
                        return False

                    if "/login" in current_url:
                        try:
                            return driver.find_element(
                                By.ID,
                                "Email"
                            ).is_displayed()
                        except Exception:
                            return False

                    if "your store" in current_title:
                        return True

                    admin_url = self.baseURL.rstrip("/")

                    if admin_url.lower().endswith("/admin"):
                        storefront_url = (
                            admin_url[:-len("/admin")]
                        )
                    else:
                        storefront_url = admin_url

                    return (
                        current_url.rstrip("/")
                        == storefront_url.lower().rstrip("/")
                    )

                except Exception:
                    return False

            result = WebDriverWait(
                self.driver,
                20
            ).until(logout_completed)

            print(
                f"Logout completed: {result}"
            )

            return True

        except Exception as e:
            self.logger.error(
                f"Logout failed: "
                f"{type(e).__name__}: {e}"
            )

            print(
                f"Logout failed: "
                f"{type(e).__name__}: {e}"
            )

            try:
                os.makedirs(
                    "Screenshots",
                    exist_ok=True
                )

                self.driver.save_screenshot(
                    "Screenshots/logout_failed.png"
                )

            except Exception:
                pass

            return False

    @pytest.mark.regression
    def test_login_ddt(self, setup):
        self.driver = setup

        try:
            self.driver.maximize_window()
        except Exception:
            pass

        wait = WebDriverWait(
            self.driver,
            20
        )

        self.logger.info(
            "****Login DDT Test Started****"
        )

        lst_status = []

        self.rows = XLUtils.getRowCount(
            self.path,
            "Sheet1"
        )

        print(
            f"Total Excel Rows: {self.rows}"
        )

        for r in range(2, self.rows + 1):

            row_status = "Fail"

            username = XLUtils.readData(
                self.path,
                "Sheet1",
                r,
                1
            )

            password = XLUtils.readData(
                self.path,
                "Sheet1",
                r,
                2
            )

            expected_result = XLUtils.readData(
                self.path,
                "Sheet1",
                r,
                3
            )

            username = str(username).strip()
            password = str(password).strip()
            expected_result = str(
                expected_result
            ).strip()

            print("\n" + "=" * 70)
            print(f"Row {r}")
            print(f"Username: {username}")
            print(
                f"Expected Result: "
                f"{expected_result}"
            )

            try:
                self.open_login_page()

            except Exception as e:
                self.logger.error(
                    f"Row {r}: Login page could not "
                    f"be opened: {e}"
                )

                print(
                    f"Row {r}: Login page could not "
                    f"be opened: "
                    f"{type(e).__name__}: {e}"
                )

                lst_status.append(row_status)
                continue

            try:
                lp = LoginPage(self.driver)

                lp.setUserName(username)
                lp.setPassword(password)
                lp.clickLogin()

                print(
                    "Login button clicked."
                )

                def login_state(driver):
                    try:
                        title = driver.title.strip().lower()

                        if (
                            "dashboard / nopcommerce administration"
                            in title
                        ):
                            return "success"

                        email_elements = driver.find_elements(
                            By.ID,
                            "Email"
                        )

                        if email_elements:
                            try:
                                if email_elements[0].is_displayed():
                                    return "failed"
                            except Exception:
                                pass

                        return False

                    except Exception:
                        return False

                login_result = WebDriverWait(
                    self.driver,
                    20
                ).until(login_state)

                login_success = (
                    login_result == "success"
                )

                actual_title = (
                    self.driver.title.strip()
                )

                print(
                    f"Actual Title: "
                    f"{actual_title}"
                )

                print(
                    f"Login Success: "
                    f"{login_success}"
                )

                expected_pass = (
                    expected_result.lower()
                    == "pass"
                )

                if login_success == expected_pass:
                    row_status = "Pass"
                else:
                    row_status = "Fail"

                # Logout is cleanup only.
                # It does not create another DDT result.
                if login_success:
                    logout_result = self.logout(
                        wait
                    )

                    if not logout_result:
                        self.logger.warning(
                            f"Row {r}: Logout failed "
                            f"after login."
                        )

                        print(
                            f"Row {r}: Logout failed "
                            f"after login."
                        )

            except Exception as e:
                row_status = "Fail"

                self.logger.error(
                    f"Row {r}: Login test failed: "
                    f"{type(e).__name__}: {e}"
                )

                print(
                    f"Row {r}: Login test failed: "
                    f"{type(e).__name__}: {e}"
                )

                try:
                    os.makedirs(
                        "Screenshots",
                        exist_ok=True
                    )

                    self.driver.save_screenshot(
                        f"Screenshots/"
                        f"login_ddt_row_{r}.png"
                    )

                except Exception:
                    pass

            lst_status.append(row_status)

            print(
                f"Row {r}: "
                f"{'*' * 5}"
                f"Test {row_status}"
                f"{'*' * 5}"
            )

        expected_rows = self.rows - 1
        processed_rows = len(lst_status)

        print("\n" + "=" * 70)
        print("Login DDT Test Summary")
        print(
            f"Expected Data Rows : "
            f"{expected_rows}"
        )
        print(
            f"Processed Rows     : "
            f"{processed_rows}"
        )
        print(
            f"Status List        : "
            f"{lst_status}"
        )

        if (
            processed_rows == expected_rows
            and lst_status
            and "Fail" not in lst_status
        ):
            self.logger.info(
                "****Login DDT Test Passed****"
            )
            assert True

        else:
            self.logger.error(
                "****Login DDT Test Failed****"
            )
            assert False