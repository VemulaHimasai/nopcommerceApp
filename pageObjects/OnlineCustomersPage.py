import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)


class OnlineCustomersPage:

    # -------------------------------------------------
    # Online Customers menu
    # -------------------------------------------------

    lnkonlinecustomers_menuitem_xpath = (
        "//a[@href='/Admin/OnlineCustomer/List']"
    )

    # -------------------------------------------------
    # Customer Roles
    # -------------------------------------------------

    txt_Customer_Roles_xpath = "//input[@role='searchbox']"

    lst_Administrators_xpath = (
        "//li[contains(text(),'Administrators')]"
    )

    lst_ForumModerators_xpath = (
        "//li[contains(text(),'Forum Moderators')]"
    )

    lst_Registered_xpath = (
        "//li[contains(text(),'Registered')]"
    )

    lst_Guests_xpath = (
        "//li[contains(text(),'Guests')]"
    )

    lst_Vendors_xpath = (
        "//li[contains(text(),'Vendors')]"
    )

    # -------------------------------------------------
    # Search button
    # -------------------------------------------------

    btnSearchRoles_xpath = (
        "//button[@id='search-customers']"
    )

    # -------------------------------------------------
    # Online Customers table
    # -------------------------------------------------

    table_xpath = (
        "//table[@id='onlinecustomers-grid']"
    )

    table_rows_xpath = (
        "//table[@id='onlinecustomers-grid']//tbody/tr"
    )

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # -------------------------------------------------
    # Open Online Customers
    # -------------------------------------------------

    def clickonOnlineCustomerMenuItem(self):

        online_customers_menu_item = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.lnkonlinecustomers_menuitem_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            online_customers_menu_item
        )

        self.driver.execute_script(
            "arguments[0].click();",
            online_customers_menu_item
        )

        # Wait for Online Customers table
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.table_xpath
                )
            )
        )

    # -------------------------------------------------
    # Get complete table data
    # -------------------------------------------------

    def getTableRows(self):

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.table_xpath
                )
            )
        )

        for attempt in range(3):

            try:

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.table_rows_xpath
                )

                table_data = []

                for row in rows:

                    columns = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    row_data = [
                        column.text.strip()
                        for column in columns
                    ]

                    table_data.append(row_data)

                return table_data

            except StaleElementReferenceException:

                print(
                    f"Table refreshed while reading rows. "
                    f"Retry {attempt + 1}/3"
                )

                time.sleep(0.5)

        raise Exception(
            "Unable to read Online Customers table."
        )

    # -------------------------------------------------
    # Get Customer Names
    # -------------------------------------------------

    def getCustomerNames(self, expected_customer=None):

        for attempt in range(3):

            try:

                # -----------------------------------------
                # Wait for table
                # -----------------------------------------

                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.table_xpath)
                    )
                )

                # -----------------------------------------
                # Wait for real customer data
                # -----------------------------------------

                def table_has_real_data(driver):

                    rows = driver.find_elements(
                        By.XPATH,
                        self.table_rows_xpath
                    )

                    if not rows:
                        return False

                    customer_names = []

                    for row in rows:

                        try:

                            columns = row.find_elements(
                                By.TAG_NAME,
                                "td"
                            )

                            if not columns:
                                continue

                            customer_name = columns[0].text.strip()

                            if not customer_name:
                                continue

                            if customer_name == "Loading...":
                                return False

                            if "No data available" in customer_name:
                                return True

                            customer_names.append(customer_name)

                        except StaleElementReferenceException:
                            return False

                    # -----------------------------------------
                    # If expected customer was supplied,
                    # wait until that customer appears
                    # -----------------------------------------

                    if expected_customer:
                        return expected_customer.strip() in customer_names

                    return len(customer_names) > 0

                self.wait.until(table_has_real_data)

                # -----------------------------------------
                # Read table again
                # -----------------------------------------

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.table_rows_xpath
                )

                customer_names = []

                for row in rows:

                    try:

                        columns = row.find_elements(
                            By.TAG_NAME,
                            "td"
                        )

                        if not columns:
                            continue

                        customer_name = columns[0].text.strip()

                        if not customer_name:
                            continue

                        if customer_name == "Loading...":
                            continue

                        if "No data available" in customer_name:
                            continue

                        customer_names.append(customer_name)

                    except StaleElementReferenceException:
                        raise

                print(
                    "Customer names:",
                    customer_names
                )

                return customer_names

            except StaleElementReferenceException:

                print(
                    f"Online Customers table refreshed. "
                    f"Retry {attempt + 1}/3"
                )

                time.sleep(1)

        raise Exception(
            "Unable to read customer names because "
            "the Online Customers table kept refreshing."
        )
    # -------------------------------------------------
    # Select Customer Role
    # -------------------------------------------------

    def selectCustomerRole(self, role):

        role_xpaths = {

            "Administrators":
                self.lst_Administrators_xpath,

            "Forum Moderators":
                self.lst_ForumModerators_xpath,

            "Registered":
                self.lst_Registered_xpath,

            "Guests":
                self.lst_Guests_xpath,

            "Vendors":
                self.lst_Vendors_xpath
        }

        if role not in role_xpaths:
            raise ValueError(
                f"Invalid role selected: {role}"
            )

        for attempt in range(3):

            try:

                # -------------------------------------------------
                # Locate Role Search Input
                # -------------------------------------------------

                role_input = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.txt_Customer_Roles_xpath
                        )
                    )
                )

                role_input.click()
                role_input.clear()
                role_input.send_keys(role)

                # -------------------------------------------------
                # IMPORTANT:
                # After typing, Select2 may refresh the DOM.
                # Therefore locate the option again.
                # -------------------------------------------------

                role_option = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            role_xpaths[role]
                        )
                    )
                )

                role_option.click()

                print(
                    "Selected Customer Role:",
                    role
                )

                return

            except StaleElementReferenceException:

                print(
                    f"StaleElementReferenceException while selecting "
                    f"'{role}'. Retrying "
                    f"({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        raise AssertionError(
            f"Unable to select customer role: {role}"
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def clickSearch(self):

        search_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnSearchRoles_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_button
        )

        search_button.click()

        # Wait for table
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.table_xpath
                )
            )
        )

    # -------------------------------------------------
    # Get Search Results
    # -------------------------------------------------

    def getSearchResults(self):

        for attempt in range(3):

            try:

                results = self.getCustomerNames()

                print(
                    "Search result customer names:",
                    results
                )

                return results

            except StaleElementReferenceException:

                print(
                    f"Search result table refreshed. "
                    f"Retrying... Attempt {attempt + 1}/3"
                )

                time.sleep(1)

        raise Exception(
            "Search results table remained stale "
            "after 3 attempts."
        )
