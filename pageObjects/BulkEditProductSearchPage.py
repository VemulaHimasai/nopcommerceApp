
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BulkEditProductSearchPage:

    # =========================================================
    # PRODUCT NAME SEARCH
    # =========================================================

    txtsearchproduct_name = "//input[@id='SearchProductName']"

    # =========================================================
    # VENDOR DROPDOWN
    # =========================================================

    drpVendor = (
        "//label[normalize-space()='Vendor']"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//span[contains(@class,'select2-selection') "
        "and @role='combobox']"
    )

    # =========================================================
    # PRODUCT TYPE DROPDOWN
    # =========================================================

    drpProducttype = (
        "//span[@role='combobox' "
        "and @aria-labelledby="
        "'select2-SearchProductTypeId-container']"
    )

    # =========================================================
    # PUBLISHED TYPE DROPDOWN
    # =========================================================

    drpPublishedtype = (
        "//span[@role='combobox' "
        "and @aria-labelledby="
        "'select2-SearchPublishedId-container']"
    )

    # =========================================================
    # SEARCH BUTTON
    # =========================================================

    btnSearch = "//button[normalize-space()='Search']"

    # =========================================================
    # BULK EDIT PRODUCTS TABLE
    # =========================================================

    products_table_xpath = (
        "//table[@class='table table-hover "
        "table-bordered table-striped']"
    )

    # =========================================================
    # INITIALIZE
    # =========================================================

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # =========================================================
    # SET PRODUCT NAME
    # =========================================================

    def setProductName(self, product_name):

        product_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtsearchproduct_name)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            product_name_field
        )

        product_name_field.clear()
        product_name_field.send_keys(product_name)

        print(
            f"Product name entered for search: "
            f"{product_name}"
        )

    # =========================================================
    # SELECT BY VENDOR
    # =========================================================

    def SelectByVendor(self, vendor):

        # ---------------------------------------------------------
        # Wait for Vendor dropdown
        # ---------------------------------------------------------

        vendor_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drpVendor)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_dropdown
        )

        vendor_dropdown.click()

        print("Vendor dropdown clicked")

        # ---------------------------------------------------------
        # Wait for Select2 results container
        # ---------------------------------------------------------

        results_container_xpath = (
            "//ul[contains(@class,'select2-results__options')]"
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, results_container_xpath)
            )
        )

        print("Vendor dropdown options container loaded")

        # ---------------------------------------------------------
        # Find Vendor1
        # ---------------------------------------------------------

        vendor_option_xpath = (
            "//li[contains(@class,'select2-results__option') "
            "and normalize-space(.)="
            f"'{vendor}']"
        )

        vendor_option = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, vendor_option_xpath)
            )
        )

        print(
            "Vendor option found:",
            vendor_option.text
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_option
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, vendor_option_xpath)
            )
        )

        vendor_option.click()

        # ---------------------------------------------------------
        # Verify selected vendor
        # ---------------------------------------------------------

        selected_vendor = self.wait.until(
            EC.presence_of_element_located(
                (By.ID, "SearchVendorId")
            )
        )

        selected_vendor_value = (
            selected_vendor.get_attribute("value")
        )

        print(
            "SearchVendorId value:",
            selected_vendor_value
        )

        print(
            f"Vendor '{vendor}' selected"
        )

    # =========================================================
    # SELECT BY PRODUCT TYPE
    # =========================================================

    def SelectByProductType(self, product_type):

        product_type_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drpProducttype)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            product_type_dropdown
        )

        product_type_dropdown.click()

        product_type_option_xpath = (
            f"//li[contains(@class,'select2-results__option') "
            f"and normalize-space(.)='{product_type}']"
        )

        product_type_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, product_type_option_xpath)
            )
        )

        product_type_option.click()

        print(
            f"Product Type '{product_type}' selected"
        )

    # =========================================================
    # SELECT BY PUBLISHED TYPE
    # =========================================================

    def SelectByPublishedType(self, published_type):

        published_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drpPublishedtype)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            published_dropdown
        )

        print(
            "Published Type dropdown found"
        )

        published_dropdown.click()

        published_option_xpath = (
            f"//li[contains(@class,'select2-results__option') "
            f"and normalize-space(.)='{published_type}']"
        )

        published_option = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, published_option_xpath)
            )
        )

        print(
            "Published option found:",
            published_option.text
        )

        published_option.click()

        print(
            f"Published type '{published_type}' selected"
        )

    # =========================================================
    # CLICK SEARCH
    # =========================================================

    def clickSearch(self):

        search_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnSearch)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_btn
        )

        search_btn.click()

        print("Search button clicked")

    # =========================================================
    # GET SEARCH RESULTS
    # =========================================================

    def getSearchResults(self):

        rows_xpath = (
            "//table[@class='table table-hover "
            "table-bordered table-striped']"
            "//tbody//tr"
            "[not(td[@colspan='7' and "
            "contains(normalize-space(.), "
            "'No data available in table')])]"
        )

        try:

            # Wait for the table to be present
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.products_table_xpath)
                )
            )

            # Give DataTable time to update after Search
            self.wait.until(
                lambda driver: (
                    len(
                        driver.find_elements(
                            By.XPATH,
                            rows_xpath
                        )
                    ) >= 0
                )
            )

            rows = self.driver.find_elements(
                By.XPATH,
                rows_xpath
            )

            actual_rows = []

            for row in rows:

                try:

                    if row.is_displayed():

                        row_text = row.text.strip()

                        # Ignore empty rows
                        if row_text:

                            actual_rows.append(row)

                except StaleElementReferenceException:

                    continue

            print(
                "Actual product rows:",
                len(actual_rows)
            )

            return actual_rows

        except TimeoutException:

            print(
                "Search result table did not load"
            )

            return []

    # =========================================================
    # VERIFY PRODUCT DISPLAYED
    # =========================================================

    def isProductDisplayed(self, product_name):

        product_xpath = (
            "//table[@class='table table-hover "
            "table-bordered table-striped']"
            "//tbody//tr"
            "[.//input[contains(@id,'name-') "
            f"and @value='{product_name}']]"
        )

        try:

            product = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, product_xpath)
                )
            )

            print(
                f"Product '{product_name}' "
                "is displayed in search results"
            )

            return product.is_displayed()

        except TimeoutException:

            print(
                f"Product '{product_name}' "
                "is not displayed in search results"
            )

            return False

