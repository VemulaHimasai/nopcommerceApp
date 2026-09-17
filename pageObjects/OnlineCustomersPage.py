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

        role_values = {
            "Administrators": "1",
            "Forum Moderators": "2",
            "Registered": "3",
            "Guests": "4",
            "Vendors": "5"
        }

        if role not in role_values:
            raise ValueError(
                f"Invalid role selected: {role}"
            )

        expected_value = role_values[role]

        print("\n========== SELECT CUSTOMER ROLE ==========")
        print(f"Requested role: {role}")
        print(f"Expected value: {expected_value}")

        select_xpath = (
            "//select[@id='SelectedCustomerRoleIds']"
        )

        for attempt in range(3):

            try:

                # -------------------------------------------------
                # Locate actual Customer Roles select
                # -------------------------------------------------

                select_element = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            select_xpath
                        )
                    )
                )

                print(
                    "Customer Roles select found:",
                    select_element.get_attribute("id")
                )

                # -------------------------------------------------
                # Select role through Select2 / jQuery
                # -------------------------------------------------

                self.driver.execute_script(
                    """
                    const select = arguments[0];
                    const value = arguments[1];

                    if (!window.jQuery) {
                        throw new Error(
                            "jQuery is not available on the page."
                        );
                    }

                    window.jQuery(select)
                        .val([value])
                        .trigger('change');
                    """,
                    select_element,
                    expected_value
                )

                print(
                    f"Requested Select2 value update: "
                    f"{expected_value}"
                )

                # -------------------------------------------------
                # Verify actual option.selected state
                # -------------------------------------------------

                def role_is_selected(driver):

                    return driver.execute_script(
                        """
                        const select = document.getElementById(
                            'SelectedCustomerRoleIds'
                        );

                        if (!select) {
                            return false;
                        }

                        return Array.from(select.options).some(
                            option =>
                                option.value === arguments[0]
                                && option.selected === true
                        );
                        """,
                        expected_value
                    )

                self.wait.until(role_is_selected)

                # -------------------------------------------------
                # Read selected roles
                # -------------------------------------------------

                selected_roles = self.driver.execute_script(
                    """
                    const select = document.getElementById(
                        'SelectedCustomerRoleIds'
                    );

                    if (!select) {
                        return [];
                    }

                    return Array.from(select.selectedOptions)
                        .map(option => ({
                            text: option.text.trim(),
                            value: option.value
                        }));
                    """
                )

                print(
                    "Selected Customer Roles:",
                    selected_roles
                )

                # -------------------------------------------------
                # Verify requested role
                # -------------------------------------------------

                role_found = any(
                    item["value"] == expected_value
                    for item in selected_roles
                )

                if not role_found:
                    raise AssertionError(
                        f"Customer role '{role}' was not selected. "
                        f"Actual values: {selected_roles}"
                    )

                # -------------------------------------------------
                # Verify actual select value
                # -------------------------------------------------

                actual_value = self.driver.execute_script(
                    """
                    const select = document.getElementById(
                        'SelectedCustomerRoleIds'
                    );

                    return select ? select.value : '';
                    """
                )

                print(
                    "Actual Customer Role value:",
                    actual_value
                )

                if actual_value != expected_value:
                    raise AssertionError(
                        f"Expected Customer Role value "
                        f"'{expected_value}', "
                        f"but actual value is "
                        f"'{actual_value}'."
                    )

                # -------------------------------------------------
                # Verify visible Select2 value
                # -------------------------------------------------

                visible_role = self.driver.execute_script(
                    """
                    const select = document.getElementById(
                        'SelectedCustomerRoleIds'
                    );

                    if (!select) {
                        return '';
                    }

                    const container = select
                        .parentElement
                        .querySelector(
                            '.select2-selection__rendered'
                        );

                    return container
                        ? container.innerText.trim()
                        : '';
                    """
                )

                print(
                    "Visible Select2 role:",
                    repr(visible_role)
                )

                print(
                    f"Customer Role selected successfully: "
                    f"{role}"
                )

                return True

            except StaleElementReferenceException:

                print(
                    f"Customer Roles select became stale. "
                    f"Retrying "
                    f"({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(0.5)

            except TimeoutException:

                print(
                    f"Timeout while selecting role "
                    f"'{role}' "
                    f"(attempt {attempt + 1}/3)."
                )

                if attempt == 2:
                    raise

                time.sleep(0.5)

        raise TimeoutException(
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
