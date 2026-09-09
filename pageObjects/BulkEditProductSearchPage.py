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
        "//table[contains(@class,'table-hover') "
        "and contains(@class,'table-bordered') "
        "and contains(@class,'table-striped')]"
    )

    # =========================================================
    # PRODUCT ROWS
    # =========================================================

    product_rows_xpath = (
        "//table[contains(@class,'table-hover') "
        "and contains(@class,'table-bordered') "
        "and contains(@class,'table-striped')]"
        "//tbody//tr[contains(@class,'product-row')]"
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
            f"Product name entered for search: {product_name}"
        )

    # =========================================================
    # SELECT BY VENDOR
    # =========================================================

    def SelectByVendor(self, vendor):

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

        results_container_xpath = (
            "//ul[contains(@class,'select2-results__options')]"
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, results_container_xpath)
            )
        )

        print("Vendor dropdown options container loaded")

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

        print("Product Type dropdown clicked")

        # -----------------------------------------------------
        # Select2 options
        # -----------------------------------------------------

        product_type_option_xpath = (
            "//li[contains(@class,'select2-results__option') "
            "and normalize-space(.)="
            f"'{product_type}']"
        )

        try:

            product_type_option = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, product_type_option_xpath)
                )
            )

        except TimeoutException:

            print(
                f"Product Type option '{product_type}' "
                "was not immediately visible."
            )

            # Debug available options
            options = self.driver.find_elements(
                By.XPATH,
                "//li[contains(@class,'select2-results__option')]"
            )

            print("Available Product Type options:")

            for option in options:

                try:

                    if option.is_displayed():

                        print(
                            f" - '{option.text.strip()}'"
                        )

                except StaleElementReferenceException:

                    continue

            raise

        print(
            "Product Type option found:",
            product_type_option.text
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            product_type_option
        )

        product_type_option.click()

        print(
            f"Product Type '{product_type}' selected"
        )

        # -----------------------------------------------------
        # Verify selected value
        # -----------------------------------------------------

        selected_product_type = self.wait.until(
            EC.presence_of_element_located(
                (By.ID, "SearchProductTypeId")
            )
        )

        selected_value = (
            selected_product_type.get_attribute("value")
        )

        print(
            "SearchProductTypeId value:",
            selected_value
        )

        # -----------------------------------------------------
        # For "All", nopCommerce uses value 0
        # -----------------------------------------------------

        if product_type == "All":

            assert selected_value == "0", (
                "Product Type 'All' was not selected correctly. "
                f"Expected value '0', got '{selected_value}'"
            )

            print(
                "Product Type 'All' verification PASSED"
            )

    # =========================================================
    # SELECT BY PUBLISHED TYPE
    # =========================================================

    def SelectByPublishedType(self, published_type):

        # ---------------------------------------------------------
        # 1. Locate Published Type dropdown
        # ---------------------------------------------------------
        published_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drpPublishedtype)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            published_dropdown
        )

        print("Published Type dropdown found")

        # ---------------------------------------------------------
        # 2. Click dropdown
        # ---------------------------------------------------------
        published_dropdown.click()

        # ---------------------------------------------------------
        # 3. Wait for Select2 results container
        # ---------------------------------------------------------
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//ul[contains(@class,'select2-results__options')]"
                )
            )
        )

        # ---------------------------------------------------------
        # 4. Locate required option
        # ---------------------------------------------------------
        published_option_xpath = (
            "//ul[contains(@class,'select2-results__options')]"
            "//li[contains(@class,'select2-results__option') "
            f"and normalize-space(.)='{published_type}']"
        )

        published_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, published_option_xpath)
            )
        )

        print(
            "Published option found:",
            published_option.text
        )

        # ---------------------------------------------------------
        # 5. Scroll option into view
        # ---------------------------------------------------------
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            published_option
        )

        # ---------------------------------------------------------
        # 6. Click option
        # ---------------------------------------------------------
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

        try:

            # -------------------------------------------------
            # Wait for product table
            # -------------------------------------------------

            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.products_table_xpath)
                )
            )

            print("Product table found")

            # -------------------------------------------------
            # Wait until at least one product row exists
            # -------------------------------------------------

            self.wait.until(
                lambda driver: len(
                    driver.find_elements(
                        By.XPATH,
                        self.product_rows_xpath
                    )
                ) > 0
            )

            # -------------------------------------------------
            # Get all product rows
            # -------------------------------------------------

            rows = self.driver.find_elements(
                By.XPATH,
                self.product_rows_xpath
            )

            print(
                "Total product rows found:",
                len(rows)
            )

            actual_rows = []

            # -------------------------------------------------
            # IMPORTANT:
            # Do NOT use row.text here.
            #
            # Bulk Edit rows contain INPUT elements.
            # Firefox returns row.text == '' even though
            # the input has a value.
            # -------------------------------------------------

            for index, row in enumerate(rows, start=1):

                try:

                    # -----------------------------------------
                    # Find product name input
                    # -----------------------------------------

                    name_input = row.find_element(
                        By.XPATH,
                        ".//input[contains(@id,'name-')]"
                    )

                    product_name = (
                        name_input.get_attribute("value")
                        or ""
                    ).strip()

                    # -----------------------------------------
                    # Find SKU input
                    # -----------------------------------------

                    sku_input = row.find_element(
                        By.XPATH,
                        ".//input[contains(@id,'sku-')]"
                    )

                    sku = (
                        sku_input.get_attribute("value")
                        or ""
                    ).strip()

                    print(
                        f"Row {index}: "
                        f"Product='{product_name}', "
                        f"SKU='{sku}'"
                    )

                    # -----------------------------------------
                    # Ignore empty row
                    #
                    # Your current table contains:
                    # product-select-62
                    # name-62 value=""
                    # sku-62 value=""
                    #
                    # This is not a real product.
                    # -----------------------------------------

                    if not product_name and not sku:

                        print(
                            f"Row {index} ignored "
                            "(empty product row)"
                        )

                        continue

                    # -----------------------------------------
                    # Add real product row
                    # -----------------------------------------

                    actual_rows.append(row)

                except StaleElementReferenceException:

                    print(
                        f"Row {index} became stale. "
                        "Skipping row."
                    )

                    continue

                except Exception as e:

                    print(
                        f"Unable to process row {index}: {e}"
                    )

                    continue

            print(
                "Actual product rows:",
                len(actual_rows)
            )

            return actual_rows

        except TimeoutException:

            print(
                "Search result table/product rows "
                "did not load"
            )

            return []

    # =========================================================
    # VERIFY PRODUCT DISPLAYED
    # =========================================================

    def isProductDisplayed(self, product_name):

        product_xpath = (
            "//table[contains(@class,'table-hover') "
            "and contains(@class,'table-bordered') "
            "and contains(@class,'table-striped')]"
            "//tbody//tr[contains(@class,'product-row')]"
            "//input[contains(@id,'name-') "
            f"and @value='{product_name}']"
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