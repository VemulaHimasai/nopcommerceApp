
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

        # -------------------------------------------------
        # Wait directly for the required Select2 option.
        # Do NOT wait separately for the <ul> container.
        # -------------------------------------------------
        vendor_option_xpath = (
            "//li[contains(@class,'select2-results__option') "
            f"and normalize-space(.)='{vendor}' "
            "and not(contains(@class,'select2-results__message'))]"
        )

        vendor_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, vendor_option_xpath)
            )
        )

        print("Vendor option found:", vendor_option.text)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_option
        )

        vendor_option.click()

        print(f"Vendor '{vendor}' selected")

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

        rows_xpath = (
            "//table[@id='products-grid']"
            "//tbody//tr"
        )

        def find_product(driver):

            try:

                rows = driver.find_elements(
                    By.XPATH,
                    rows_xpath
                )

                for index, row in enumerate(rows, start=1):

                    try:

                        row_text = row.text.strip()

                        # Ignore DataTables temporary/empty rows
                        if not row_text:
                            continue

                        if row_text.lower() == "loading...":
                            continue

                        if "No data available in table" in row_text:
                            continue

                        print(
                            f"Checking product row {index}: "
                            f"{row_text}"
                        )

                        cells = row.find_elements(
                            By.TAG_NAME,
                            "td"
                        )

                        # Product name is normally column 3
                        if len(cells) < 3:
                            continue

                        actual_product_name = (
                            cells[2].text.strip()
                        )

                        # Ignore blank/incomplete rows
                        if not actual_product_name:
                            continue

                        if actual_product_name == product_name:
                            print(
                                f"Product found: "
                                f"{actual_product_name}"
                            )

                            return True

                    except StaleElementReferenceException:

                        print(
                            f"Row {index} became stale. "
                            f"Retrying..."
                        )

                        return False

                return False

            except StaleElementReferenceException:

                return False

        try:

            self.wait.until(
                find_product
            )

            print(
                f"Product '{product_name}' "
                f"is displayed in search results"
            )

            return True

        except TimeoutException:

            print(
                f"Product not found in search results: "
                f"{product_name}"
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

        print("Verifying SKU:", expected_sku)

        expected_sku = str(expected_sku).strip()

        try:
            self.wait.until(
                lambda driver: (
                                       driver.find_element(
                                           By.XPATH,
                                           self.txtsku_edit_xpath
                                       ).get_attribute("value") or ""
                               ).strip() != ""
            )

            sku_field = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.txtsku_edit_xpath)
                )
            )

            actual_sku = (
                    sku_field.get_attribute("value") or ""
            ).strip()

            print("Expected SKU:", expected_sku)
            print("Actual SKU:", actual_sku)

            if actual_sku == expected_sku:
                print("SKU verification PASSED")
                return True

            print("SKU verification FAILED")
            return False

        except TimeoutException:

            print(
                "SKU field not found:",
                self.txtsku_edit_xpath
            )

            print("Current URL:", self.driver.current_url)
            print("Current Title:", self.driver.title)

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

    def printSearchResults(self):
        rows = self.driver.find_elements(By.XPATH,"//table[@id='products-grid']//tbody//tr")
        print(f"Total rows: {len(rows)}")
        for index,row in enumerate(rows,start=1):
            try:
                print(f"Search Row {index}: "
                f"{row.text.strip()}")
            except StaleElementReferenceException:
                print(f"Search Row {index}: STALE")

    # =========================================================
    # GET SKU BY PRODUCT NAME
    # =========================================================

    def getSKUByProductName(self, product_name):

        product_name = product_name.strip()

        # Search product by name
        self.setProductName(product_name)
        self.clickSearch()

        rows_xpath = (
            "//table[@id='products-grid']"
            "//tbody//tr"
        )

        try:

            def find_product_sku(driver):

                rows = driver.find_elements(
                    By.XPATH,
                    rows_xpath
                )

                for row in rows:

                    try:

                        cells = row.find_elements(By.TAG_NAME, "td")

                        row_text = row.text.strip()

                        print(
                            "Checking row:",
                            row_text
                        )

                        if product_name in row_text:

                            print(
                                "Product found:",
                                product_name
                            )

                            # Print all columns so we can confirm
                            # the SKU column position
                            for index, cell in enumerate(cells):
                                print(
                                    f"Column {index}:",
                                    cell.text.strip()
                                )

                            # SKU is normally column 4 in nopCommerce
                            sku = cells[3].text.strip()

                            if sku:
                                return sku

                    except StaleElementReferenceException:
                        continue

                return False

            sku = WebDriverWait(
                self.driver,
                20
            ).until(find_product_sku)

            print(
                f"Dynamic SKU for '{product_name}':",
                sku
            )

            return sku

        except TimeoutException:

            print(
                f"Could not find SKU for product: "
                f"{product_name}"
            )

            self.printSearchResults()

            return None

    # =========================================================
    # GET FIRST AVAILABLE PRODUCT AND SKU
    # =========================================================

    def getFirstProductAndSKU(self):

        rows_xpath = (
            "//table[@id='products-grid']"
            "//tbody//tr"
        )

        try:

            def find_valid_product(driver):

                rows = driver.find_elements(
                    By.XPATH,
                    rows_xpath
                )

                for index, row in enumerate(rows, start=1):

                    try:

                        row_text = row.text.strip()

                        print(
                            f"Checking product row {index}: "
                            f"{row_text}"
                        )

                        # Ignore temporary DataTables rows
                        if not row_text:
                            continue

                        if row_text.lower() == "loading...":
                            continue

                        if "No data available in table" in row_text:
                            continue

                        cells = row.find_elements(
                            By.TAG_NAME,
                            "td"
                        )

                        # Product name = cells[2]
                        # SKU         = cells[3]
                        if len(cells) < 4:
                            continue

                        product_name = cells[2].text.strip()
                        sku = cells[3].text.strip()

                        if not product_name:
                            continue

                        if not sku:
                            continue

                        print(
                            "Dynamic product found:",
                            product_name
                        )

                        print(
                            "Dynamic SKU found:",
                            sku
                        )

                        return product_name, sku

                    except StaleElementReferenceException:

                        print(
                            f"Row {index} became stale. Retrying..."
                        )

                        continue

                return False

            result = WebDriverWait(
                self.driver,
                20
            ).until(find_valid_product)

            return result

        except TimeoutException:

            print(
                "No valid product with SKU was found "
                "after waiting for Products table."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Current Title:",
                self.driver.title
            )

            self.printSearchResults()

            return None, None

    # =========================================================
    # GET FIRST AVAILABLE PRODUCT NAME
    # =========================================================

    def getFirstProductName(self):

        rows_xpath = (
            "//table[@id='products-grid']"
            "//tbody//tr"
        )

        try:

            def find_valid_product(driver):

                rows = driver.find_elements(
                    By.XPATH,
                    rows_xpath
                )

                for index, row in enumerate(rows, start=1):

                    try:

                        row_text = row.text.strip()

                        print(
                            f"Checking product row {index}: "
                            f"{row_text}"
                        )

                        # -------------------------------------------------
                        # Ignore DataTables temporary/loading rows
                        # -------------------------------------------------

                        if not row_text:
                            continue

                        if row_text.lower() == "loading...":
                            continue

                        if "No data available in table" in row_text:
                            continue

                        # -------------------------------------------------
                        # Get cells
                        # -------------------------------------------------

                        cells = row.find_elements(
                            By.TAG_NAME,
                            "td"
                        )

                        if len(cells) < 3:
                            continue

                        # -------------------------------------------------
                        # Product name is column index 2
                        # -------------------------------------------------

                        product_name = cells[2].text.strip()

                        if not product_name:
                            continue

                        print(
                            "Dynamic product name found:",
                            product_name
                        )

                        return product_name

                    except StaleElementReferenceException:

                        print(
                            f"Row {index} became stale"
                        )

                        continue

                return False

            # ---------------------------------------------------------
            # IMPORTANT:
            # Wait until an actual product is available,
            # not merely until the table exists.
            # ---------------------------------------------------------

            product_name = WebDriverWait(
                self.driver,
                20
            ).until(find_valid_product)

            return product_name

        except TimeoutException:

            print(
                "No valid product name was found "
                "after waiting for Products table."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Current Title:",
                self.driver.title
            )

            self.printSearchResults()

            return None
    # =========================================================
    # CLICK EDIT FOR PRODUCT NAME
    # =========================================================

    def clickEditByProductName(self, product_name):

        product_name = product_name.strip()

        row_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody//tr"
            f"[.//td[3][normalize-space()="
            f"'{product_name}']]"
        )

        edit_button_xpath = (
                row_xpath +
                "//a[contains(@href,'/Admin/Product/Edit')]"
        )

        try:

            def find_edit_button(driver):

                try:

                    rows = driver.find_elements(
                        By.XPATH,
                        row_xpath
                    )

                    for row in rows:

                        try:

                            row_text = row.text.strip()

                            print(
                                "Checking product row for edit:",
                                row_text
                            )

                            if product_name not in row_text:
                                continue

                            print(
                                "Product row found for edit:",
                                product_name
                            )

                            driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center'});",
                                row
                            )

                            edit_buttons = row.find_elements(
                                By.XPATH,
                                ".//a[contains(@href,'/Admin/Product/Edit')]"
                            )

                            if not edit_buttons:
                                continue

                            edit_button = edit_buttons[0]

                            if not edit_button.is_displayed():
                                continue

                            if not edit_button.is_enabled():
                                continue

                            return edit_button

                        except StaleElementReferenceException:
                            print(
                                "Product row became stale. Retrying..."
                            )
                            continue

                    return False

                except StaleElementReferenceException:
                    return False

            edit_button = WebDriverWait(
                self.driver,
                20
            ).until(find_edit_button)

            print(
                "Edit button found for:",
                product_name
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                edit_button
            )

            try:
                edit_button.click()

            except StaleElementReferenceException:

                print(
                    "Edit button became stale. "
                    "Finding it again..."
                )

                edit_button = WebDriverWait(
                    self.driver,
                    10
                ).until(find_edit_button)

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    edit_button
                )

                edit_button.click()

            print(
                "Edit clicked for product:",
                product_name
            )

            self.wait.until(
                EC.url_contains("/Admin/Product/Edit")
            )

            print(
                "Edit Product URL:",
                self.driver.current_url
            )

            return True

        except TimeoutException:

            print(
                "Could not find Edit button for product:",
                product_name
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            self.printSearchResults()

            return False