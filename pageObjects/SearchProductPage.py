
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchProduct:

    # ---------------------------------------------------------
    # Product Name
    # ---------------------------------------------------------
    txtproductname_xpath = "//input[@id='SearchProductName']"

    # ---------------------------------------------------------
    # Product Type
    # ---------------------------------------------------------
    drp_producttype = "//span[@id='select2-SearchProductTypeId-container']"

    # ---------------------------------------------------------
    # SKU
    # ---------------------------------------------------------
    txtsku_xpath = "//input[@id='GoDirectlyToSku']"
    btngo_xpath = "//button[@id='go-to-product-by-sku']"

    # ---------------------------------------------------------
    # Published
    # ---------------------------------------------------------
    drp_published = "//span[@id='select2-SearchPublishedId-container']"

    # ---------------------------------------------------------
    # Vendor
    # ---------------------------------------------------------
    drp_vendor_xpath = "//span[@id='select2-SearchVendorId-container']"

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------
    btnSearch_xpath = "//button[@id='search-products']"

    # ---------------------------------------------------------
    # Product Table
    # ---------------------------------------------------------
    tbl_producttable_xpath = "//table[@id='products-grid']"

    # ---------------------------------------------------------
    # SKU field on Edit Product page
    # ---------------------------------------------------------
    txtsku_edit_xpath = "//input[@id='Sku']"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # =========================================================
    # VENDOR
    # =========================================================

    def selectVendor(self, vendor):

        vendor_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drp_vendor_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_dropdown
        )

        print("Vendor dropdown found")

        vendor_dropdown.click()

        print("Vendor dropdown clicked")

        # Wait for Select2 results container
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//ul[contains(@class,'select2-results__options')]"
                )
            )
        )

        vendor_option_xpath = (
            "//ul[contains(@class,'select2-results__options')]"
            "//li[contains(@class,'select2-results__option') "
            f"and normalize-space(.)='{vendor}']"
        )

        vendor_option = self.wait.until(
            EC.element_to_be_clickable(
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

        vendor_option.click()

        print(
            f"Vendor '{vendor}' selected"
        )

    # =========================================================
    # PRODUCT TYPE
    # =========================================================

    def selectProductType(self, producttype):

        producttype_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drp_producttype)
            )
        )

        producttype_dropdown.click()

        producttype_xpath = (
            f"//li[normalize-space(.)='{producttype}']"
        )

        producttype_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, producttype_xpath)
            )
        )

        producttype_option.click()

        print("Product Type selected:", producttype)

    # =========================================================
    # PUBLISHED
    # =========================================================

    def selectPublishedItem(self, published):

        published_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drp_published)
            )
        )

        published_dropdown.click()

        published_item_xpath = (
            f"//li[normalize-space(.)='{published}']"
        )

        published_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, published_item_xpath)
            )
        )

        published_option.click()

        print("Published Item selected:", published)

    # =========================================================
    # PRODUCT NAME
    # =========================================================

    def setProductName(self, product_name):

        product_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtproductname_xpath)
            )
        )

        product_name_field.clear()
        product_name_field.send_keys(product_name)

        print("Product name entered:", product_name)

    # ---------------------------------------------------------
    # Clear Product Name
    # ---------------------------------------------------------

    def clearProductName(self):

        product_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtproductname_xpath)
            )
        )

        product_name_field.clear()

        print("Product name cleared")

    # =========================================================
    # SEARCH
    # =========================================================

    def clickSearch(self):

        search_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnSearch_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            search_button
        )

        print("Search button clicked")

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.tbl_producttable_xpath)
            )
        )

        self.wait.until(
            lambda driver: len(
                driver.find_elements(
                    By.XPATH,
                    self.tbl_producttable_xpath + "//tbody/tr"
                )
            ) > 0
        )

        print("Search results table loaded")

    # =========================================================
    # PRODUCT PRESENT
    # =========================================================

    def isProductPresent(self, product_name):

        product_xpath = (
            f"//table[@id='products-grid']"
            f"//tbody//tr"
            f"//td[contains(normalize-space(.),'{product_name}')]"
        )

        try:

            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, product_xpath)
                )
            )

            print(
                f"Product found in search results: {product_name}"
            )

            return True

        except TimeoutException:

            print(
                f"Product not found in search results: {product_name}"
            )

            print("Current URL:", self.driver.current_url)
            print("Current Title:", self.driver.title)

            return False

    # =========================================================
    # SKU
    # =========================================================

    def setSKU(self, sku):

        sku_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtsku_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            sku_field
        )

        sku_field.clear()
        sku_field.send_keys(sku)

        print("SKU entered:", sku)

    # =========================================================
    # CLICK GO
    # =========================================================

    def clickGo(self):

        go_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btngo_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            go_button
        )

        print("Go button found")
        print("Go button text:", go_button.text)
        print("Go button type:", go_button.get_attribute("type"))
        print("Go button id:", go_button.get_attribute("id"))
        print("Go button disabled:", go_button.get_attribute("disabled"))

        print(
            "SKU before Go:",
            self.driver.find_element(
                By.XPATH,
                self.txtsku_xpath
            ).get_attribute("value")
        )

        old_url = self.driver.current_url

        print("URL before Go:", old_url)

        go_button.click()

        print("Go button clicked")

        # Wait a few seconds for any AJAX/redirect operation
        try:

            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.current_url != old_url
            )

            print(
                "URL changed:",
                self.driver.current_url
            )

        except TimeoutException:

            print(
                "URL did NOT change after Go."
            )

        print(
            "URL after Go:",
            self.driver.current_url
        )

        print(
            "Title after Go:",
            self.driver.title
        )

        # ---------------------------------------------------------
        # Check whether SKU edit field exists
        # ---------------------------------------------------------

        sku_fields = self.driver.find_elements(
            By.XPATH,
            self.txtsku_edit_xpath
        )

        print(
            "Edit Product SKU fields found:",
            len(sku_fields)
        )

        # ---------------------------------------------------------
        # Check for validation/error messages
        # ---------------------------------------------------------

        body_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        print("----- PAGE TEXT AFTER GO -----")
        print(body_text[:3000])
        print("----- END PAGE TEXT -----")
    # =========================================================
    # VERIFY SKU
    # =========================================================

    def verifySKU(self, expected_sku):

        print(
            "Verifying SKU:",
            expected_sku
        )

        try:

            sku_field = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.txtsku_edit_xpath)
                )
            )

            # Wait until the field actually contains a value
            self.wait.until(
                lambda driver: (
                    sku_field.get_attribute("value") or ""
                ).strip() != ""
            )

            actual_sku = (
                sku_field.get_attribute("value") or ""
            ).strip()

            expected_sku = str(expected_sku).strip()

            print(
                "Expected SKU:",
                expected_sku
            )

            print(
                "Actual SKU:",
                actual_sku
            )

            if actual_sku == expected_sku:

                print(
                    "SKU verification PASSED"
                )

                return True

            print(
                "SKU verification FAILED"
            )

            return False

        except StaleElementReferenceException:

            print(
                "SKU field became stale. "
                "Locating it again..."
            )

            try:

                sku_field = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, self.txtsku_edit_xpath)
                    )
                )

                actual_sku = (
                    sku_field.get_attribute("value") or ""
                ).strip()

                expected_sku = str(expected_sku).strip()

                print(
                    "Expected SKU:",
                    expected_sku
                )

                print(
                    "Actual SKU after retry:",
                    actual_sku
                )

                return actual_sku == expected_sku

            except TimeoutException:

                print(
                    "Could not locate SKU field after retry."
                )

                return False

        except TimeoutException:

            print(
                "SKU field not found:",
                self.txtsku_edit_xpath
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Current Title:",
                self.driver.title
            )

            return False

    # =========================================================
    # SKU PRODUCT PRESENT
    # =========================================================

    def isSKUProductPresent(self, sku):

        sku_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody//tr//td"
            f"[contains(normalize-space(.),'{sku}')]"
        )

        try:

            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, sku_xpath)
                )
            )

            print(
                "Product with SKU found in search results:",
                sku
            )

            return True

        except TimeoutException:

            print(
                "Product with SKU not found in search results:",
                sku
            )

            return False

    # =========================================================
    # VENDOR PRODUCT PRESENT
    # =========================================================

    def isVendorProductPresent(self, vendor):

        vendor_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody//tr//td"
            f"[contains(normalize-space(.),'{vendor}')]"
        )

        try:

            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, vendor_xpath)
                )
            )

            print(
                "Product with Vendor found in search results:",
                vendor
            )

            return True

        except TimeoutException:

            print(
                "Product with Vendor not found in search results:",
                vendor
            )

            return False

    # =========================================================
    # NO DATA AVAILABLE
    # =========================================================

    def isNoDataAvailable(self):

        no_data_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody//td[contains(@class,'dt-empty')]"
        )

        try:

            no_data = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, no_data_xpath)
                )
            )

            actual_text = no_data.text.strip()

            print(
                "Search result message:",
                actual_text
            )

            return actual_text == "No data available in table"

        except TimeoutException:

            print(
                "No 'No data available in table' message found"
            )

            return False

    # =========================================================
    # NO RECORDS
    # =========================================================

    def isNoRecordsDisplayed(self):

        records_xpath = (
            "//div[contains(@class,'dt-info')]"
        )

        try:

            records = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, records_xpath)
                )
            )

            actual_text = records.text.strip()

            print(
                "Records:",
                actual_text
            )

            return actual_text == "No records"

        except TimeoutException:

            print(
                "No 'No records' text found"
            )

            return False

