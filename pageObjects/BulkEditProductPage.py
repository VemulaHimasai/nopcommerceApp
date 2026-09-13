
import random

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BulkEditProductPage:

    # =========================================================
    # LOCATORS
    # =========================================================

    btnbulkedit_xpath = (
        "//a[normalize-space()='Bulk edit products']"
    )

    btnAddnew_xpath = (
        "//a[normalize-space()='Add new']"
    )

    # Dynamic nopCommerce input IDs
    txtProductName_xpath = (
        "//input[contains(@id,'name-')]"
    )

    txtSKU_xpath = (
        "//input[contains(@id,'sku-')]"
    )

    new_price_xpath = (
        "//input[contains(@id,'price-')]"
    )

    old_price_xpath = (
        "//input[contains(@id,'old-price-')]"
    )

    stkquantity_xpath = (
        "//input[contains(@id,'quantity-')]"
    )

    # ---------------------------------------------------------
    # Save Selected
    # ---------------------------------------------------------

    btnSaveSelected_xpath = (
        "//button[@id='bulk-edit-save-selected']"
    )

    confirmSaveSelected_xpath = (
        "//button[@id="
        "'bulk-edit-save-selected-action-confirmation-submit-button']"
    )

    # ---------------------------------------------------------
    # Save All
    # ---------------------------------------------------------

    btnSaveAll_xpath = (
        "//button[@id='bulk-edit-save-all']"
    )

    confirmSaveAll_xpath = (
        "//button[@id="
        "'bulk-edit-save-all-action-confirmation-submit-button']"
    )

    # ---------------------------------------------------------
    # Product table
    # ---------------------------------------------------------

    products_table_xpath = (
        "//table[contains(@class,'table-hover') "
        "and contains(@class,'table-bordered') "
        "and contains(@class,'table-striped')]"
    )

    checkboxes_table = (
        "//table[contains(@class,'table-hover') "
        "and contains(@class,'table-bordered') "
        "and contains(@class,'table-striped')]"
        "//tbody//tr//input[@type='checkbox']"
    )

    checkbox_table_head = (
        "//table[contains(@class,'table-hover') "
        "and contains(@class,'table-bordered') "
        "and contains(@class,'table-striped')]"
        "/thead/tr/th//input"
    )

    # ---------------------------------------------------------
    # Back to Product List
    # ---------------------------------------------------------

    lnk_backproductslist = (
        "//a[normalize-space()='back to product list']"
    )

    # =========================================================
    # CONSTRUCTOR
    # =========================================================

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            self.driver,
            20
        )

        # Stores the newly created row
        self.new_product_row = None

        # Stable IDs of newly created fields
        self.new_product_name_id = None
        self.new_product_sku_id = None
        self.new_product_price_id = None
        self.new_product_old_price_id = None
        self.new_product_quantity_id = None

    # =========================================================
    # COMMON TABLE ROW LOCATOR
    # =========================================================

    def getProductRows(self):

        return self.driver.find_elements(
            By.XPATH,
            self.products_table_xpath + "//tbody//tr"
        )

    # =========================================================
    # SCROLL TO PRODUCT TABLE
    # =========================================================

    def scrollToProductsTable(self):

        table = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.products_table_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            table
        )

        return table

    # =========================================================
    # GET PRODUCT CHECKBOXES
    # =========================================================

    def getProductCheckboxes(self):

        self.scrollToProductsTable()

        return self.driver.find_elements(
            By.XPATH,
            self.checkboxes_table
        )

    # =========================================================
    # SELECT CHECKBOX BY ROW NUMBER
    # =========================================================

    def SelectProductCheckbox(self, row_number):

        checkboxes = self.getProductCheckboxes()

        if not checkboxes:

            raise TimeoutException(
                "No product checkboxes found."
            )

        if row_number < 1 or row_number > len(checkboxes):

            raise IndexError(
                f"Invalid row number {row_number}. "
                f"Available rows: 1-{len(checkboxes)}"
            )

        checkbox = checkboxes[row_number - 1]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            checkbox
        )

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

        print(
            f"Product checkbox selected at row "
            f"{row_number}"
        )

    # =========================================================
    # FIND NEW PRODUCT ROW
    # =========================================================

    def get_new_product_row(self, driver):

        try:

            # -------------------------------------------------
            # Get all current product-name fields
            # -------------------------------------------------

            name_fields = driver.find_elements(
                By.XPATH,
                self.txtProductName_xpath
            )

            if not name_fields:
                return False

            # -------------------------------------------------
            # If we already know the new product name ID,
            # reacquire the row directly.
            # -------------------------------------------------

            if self.new_product_name_id:

                try:

                    name_field = driver.find_element(
                        By.ID,
                        self.new_product_name_id
                    )

                    row = name_field.find_element(
                        By.XPATH,
                        "./ancestor::tr[1]"
                    )

                    sku_fields = row.find_elements(
                        By.XPATH,
                        ".//input[contains(@id,'sku-')]"
                    )

                    if not sku_fields:
                        return False

                    return row

                except (
                    NoSuchElementException,
                    StaleElementReferenceException
                ):

                    return False

            return False

        except (
            NoSuchElementException,
            StaleElementReferenceException
        ):

            return False

    # =========================================================
    # GET NEW PRODUCT FIELD
    # =========================================================

    def getNewProductField(self, field_xpath):

        if self.new_product_row is None:

            raise TimeoutException(
                "New product row has not been created. "
                "Call clickAddNew() first."
            )

        for attempt in range(5):

            try:

                field = self.new_product_row.find_element(
                    By.XPATH,
                    field_xpath
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    field
                )

                return field

            except StaleElementReferenceException:

                print(
                    f"New product row became stale. "
                    f"Retrying ({attempt + 1}/5)..."
                )

                # -------------------------------------------------
                # Reacquire the row using stable name input ID
                # -------------------------------------------------

                if self.new_product_name_id:

                    try:

                        name_field = self.wait.until(
                            EC.presence_of_element_located(
                                (
                                    By.ID,
                                    self.new_product_name_id
                                )
                            )
                        )

                        self.new_product_row = (
                            name_field.find_element(
                                By.XPATH,
                                "./ancestor::tr[1]"
                            )
                        )

                        continue

                    except (
                        StaleElementReferenceException,
                        TimeoutException,
                        NoSuchElementException
                    ):

                        continue

        raise TimeoutException(
            "Unable to locate field in new product row."
        )

    # =========================================================
    # CLICK ADD NEW
    # =========================================================

    def clickAddNew(self):

        print("Waiting for Add New button...")

        # ---------------------------------------------------------
        # Make sure Bulk Edit table exists
        # ---------------------------------------------------------

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.products_table_xpath
                )
            )
        )

        rows_xpath = (
            self.products_table_xpath
            + "//tbody//tr"
        )

        # ---------------------------------------------------------
        # Get rows BEFORE Add New
        # ---------------------------------------------------------

        rows_before = self.driver.find_elements(
            By.XPATH,
            rows_xpath
        )

        print(
            f"Bulk Edit rows before Add New: "
            f"{len(rows_before)}"
        )

        # ---------------------------------------------------------
        # Store existing name and SKU IDs
        #
        # We use these IDs to distinguish the new row from
        # existing rows.
        # ---------------------------------------------------------

        existing_name_ids = set()
        existing_sku_ids = set()

        for row in rows_before:

            try:

                name_fields = row.find_elements(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                )

                sku_fields = row.find_elements(
                    By.XPATH,
                    ".//input[contains(@id,'sku-')]"
                )

                for field in name_fields:

                    field_id = field.get_attribute("id")

                    if field_id:
                        existing_name_ids.add(field_id)

                for field in sku_fields:

                    field_id = field.get_attribute("id")

                    if field_id:
                        existing_sku_ids.add(field_id)

            except StaleElementReferenceException:

                continue

        print(
            f"Existing name input IDs: "
            f"{len(existing_name_ids)}"
        )

        print(
            f"Existing SKU input IDs: "
            f"{len(existing_sku_ids)}"
        )

        # ---------------------------------------------------------
        # Click Add New
        # ---------------------------------------------------------

        add_new_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnAddnew_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_new_button
        )

        # Re-fetch immediately before clicking
        add_new_button = self.driver.find_element(
            By.XPATH,
            self.btnAddnew_xpath
        )

        self.driver.execute_script(
            "arguments[0].click();",
            add_new_button
        )

        print("Add new button clicked")

        # =========================================================
        # WAIT FOR NEW PRODUCT ROW
        # =========================================================

        def find_new_product_fields(driver):

            try:

                name_fields = driver.find_elements(
                    By.XPATH,
                    self.txtProductName_xpath
                )

                if not name_fields:
                    return False

                # -------------------------------------------------
                # Find a name input that did not exist before
                # Add New.
                # -------------------------------------------------

                for name_field in name_fields:

                    try:

                        name_id = (
                            name_field.get_attribute("id")
                        )

                        if not name_id:
                            continue

                        if name_id in existing_name_ids:
                            continue

                        # -------------------------------------------------
                        # New name input found
                        # -------------------------------------------------

                        row = name_field.find_element(
                            By.XPATH,
                            "./ancestor::tr[1]"
                        )

                        # -------------------------------------------------
                        # Verify SKU exists in same row
                        # -------------------------------------------------

                        sku_fields = row.find_elements(
                            By.XPATH,
                            ".//input[contains(@id,'sku-')]"
                        )

                        if not sku_fields:
                            return False

                        sku_field = sku_fields[0]

                        sku_id = (
                            sku_field.get_attribute("id")
                        )

                        if not sku_id:
                            return False

                        # -------------------------------------------------
                        # Verify SKU is also new
                        # -------------------------------------------------

                        if sku_id in existing_sku_ids:

                            print(
                                f"New name field found, but SKU "
                                f"{sku_id} belongs to an existing row."
                            )

                            return False

                        # =================================================
                        # Store NEW field IDs
                        # =================================================

                        self.new_product_name_id = name_id
                        self.new_product_sku_id = sku_id

                        # -------------------------------------------------
                        # Price
                        # -------------------------------------------------

                        price_fields = row.find_elements(
                            By.XPATH,
                            ".//input[contains(@id,'price-')]"
                        )

                        if price_fields:

                            self.new_product_price_id = (
                                price_fields[0]
                                .get_attribute("id")
                            )

                        # -------------------------------------------------
                        # Old Price
                        # -------------------------------------------------

                        old_price_fields = row.find_elements(
                            By.XPATH,
                            ".//input[contains(@id,'old-price-')]"
                        )

                        if old_price_fields:

                            self.new_product_old_price_id = (
                                old_price_fields[0]
                                .get_attribute("id")
                            )

                        # -------------------------------------------------
                        # Quantity
                        # -------------------------------------------------

                        quantity_fields = row.find_elements(
                            By.XPATH,
                            ".//input[contains(@id,'quantity-')]"
                        )

                        if quantity_fields:

                            self.new_product_quantity_id = (
                                quantity_fields[0]
                                .get_attribute("id")
                            )

                        # -------------------------------------------------
                        # Store new row
                        # -------------------------------------------------

                        self.new_product_row = row

                        print(
                            "New product fields detected"
                        )

                        print(
                            "New Product Name input:",
                            self.new_product_name_id
                        )

                        print(
                            "New SKU input:",
                            self.new_product_sku_id
                        )

                        if self.new_product_price_id:

                            print(
                                "New Price input:",
                                self.new_product_price_id
                            )

                        if self.new_product_old_price_id:

                            print(
                                "New Old Price input:",
                                self.new_product_old_price_id
                            )

                        if self.new_product_quantity_id:

                            print(
                                "New Quantity input:",
                                self.new_product_quantity_id
                            )

                        return True

                    except StaleElementReferenceException:

                        return False

                return False

            except StaleElementReferenceException:

                return False

        # ---------------------------------------------------------
        # Wait until the new fields appear
        # ---------------------------------------------------------

        self.wait.until(
            find_new_product_fields
        )

        # =========================================================
        # REACQUIRE NEW ROW
        # =========================================================

        self.new_product_row = self.wait.until(
            self.get_new_product_row
        )

        # ---------------------------------------------------------
        # Scroll new row into view
        # ---------------------------------------------------------

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            self.new_product_row
        )

        print(
            "New Bulk Edit row created"
        )

        print(
            "Bulk Edit Add New row loaded"
        )

        return self.new_product_row

    # =========================================================
    # SET PRODUCT NAME
    # =========================================================

    def setProductName(self, product_name=None):

        if product_name is None:

            product_name = (
                "Test Product "
                + str(random.randint(1000, 9999))
            )

        for attempt in range(5):

            try:

                if not self.new_product_name_id:

                    raise TimeoutException(
                        "New product name field ID is not available."
                    )

                product_name_field = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.new_product_name_id
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    product_name_field
                )

                product_name_field.clear()

                product_name_field.send_keys(
                    product_name
                )

                print(
                    f"Product name entered: "
                    f"{product_name}"
                )

                return product_name

            except (
                StaleElementReferenceException,
                TimeoutException
            ):

                print(
                    f"Product name field not ready. "
                    f"Retrying ({attempt + 1}/5)..."
                )

        raise TimeoutException(
            "Unable to enter product name."
        )

    # =========================================================
    # SET SKU
    # =========================================================

    def setSKU(self, sku=None):

        if sku is None:

            sku = (
                "SKU "
                + str(random.randint(10000, 99999))
            )

        sku_field = self.getNewProductField(
            ".//input[contains(@id,'sku-')]"
        )

        sku_field.clear()

        sku_field.send_keys(
            sku
        )

        print(
            f"SKU entered: {sku}"
        )

        return sku

    # =========================================================
    # SET NEW PRICE
    # =========================================================

    def setNewPrice(self, price="2000"):

        price_field = self.getNewProductField(
            ".//input[contains(@id,'price-')]"
        )

        price_field.clear()

        price_field.send_keys(
            str(price)
        )

        print(
            f"New price entered: {price}"
        )

        return price

    # =========================================================
    # SET OLD PRICE
    # =========================================================

    def setOldPrice(self, old_price="1000"):

        old_price_field = self.getNewProductField(
            ".//input[contains(@id,'old-price-')]"
        )

        old_price_field.clear()

        old_price_field.send_keys(
            str(old_price)
        )

        print(
            f"Old price entered: {old_price}"
        )

        return old_price

    # =========================================================
    # SET STOCK QUANTITY
    # =========================================================

    def setStockQuantity(self, quantity="1000"):

        quantity_field = self.getNewProductField(
            ".//input[contains(@id,'quantity-')]"
        )

        quantity_field.clear()

        quantity_field.send_keys(
            str(quantity)
        )

        print(
            f"Stock quantity entered: {quantity}"
        )

        return quantity

    # =========================================================
    # CLICK BULK EDIT PRODUCTS
    # =========================================================

    def clickBulkEditProducts(self):

        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnbulkedit_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.products_table_xpath
                )
            )
        )

        print(
            "Bulk Edit products button clicked"
        )

        print(
            "Bulk Edit products page loaded"
        )

    # =========================================================
    # PRINT PRODUCT ROWS
    # =========================================================

    def printProductRows(self):

        rows = self.getProductRows()

        print(
            f"Total Rows: {len(rows)}"
        )

        for index, row in enumerate(rows):

            try:

                name_fields = row.find_elements(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                )

                sku_fields = row.find_elements(
                    By.XPATH,
                    ".//input[contains(@id,'sku-')]"
                )

                product_name = ""
                sku = ""

                if name_fields:

                    product_name = (
                        name_fields[0]
                        .get_attribute("value")
                        or ""
                    )

                if sku_fields:

                    sku = (
                        sku_fields[0]
                        .get_attribute("value")
                        or ""
                    )

                print(
                    f"Row {index + 1}: "
                    f"Product Name='{product_name}', "
                    f"SKU='{sku}'"
                )

            except StaleElementReferenceException:

                print(
                    f"Row {index + 1}: STALE ELEMENT"
                )

    # =========================================================
    # SELECT PRODUCT BY NAME
    # =========================================================

    def selectProductByName(self, product_name):

        product_name = product_name.strip()

        rows_xpath = (
            "//table[contains(@class,'table-hover') "
            "and contains(@class,'table-bordered') "
            "and contains(@class,'table-striped')]"
            "//tbody//tr"
        )

        for attempt in range(3):

            try:

                rows = self.driver.find_elements(
                    By.XPATH,
                    rows_xpath
                )

                for index, row in enumerate(rows):

                    try:

                        name_fields = row.find_elements(
                            By.XPATH,
                            ".//input[contains(@id,'name-')]"
                        )

                        if not name_fields:
                            continue

                        current_product_name = (
                            name_fields[0]
                            .get_attribute("value")
                            or ""
                        )

                        print(
                            f"Row {index + 1}: "
                            f"Product Name = "
                            f"'{current_product_name}'"
                        )

                        if (
                            current_product_name.strip()
                            == product_name
                        ):

                            checkbox = row.find_element(
                                By.XPATH,
                                ".//input[@type='checkbox']"
                            )

                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center'});",
                                checkbox
                            )

                            self.driver.execute_script(
                                "arguments[0].click();",
                                checkbox
                            )

                            print(
                                f"Product '{product_name}' "
                                f"checkbox selected at row "
                                f"{index + 1}"
                            )

                            return True

                    except StaleElementReferenceException:

                        continue

                raise TimeoutException(
                    f"Product '{product_name}' "
                    f"was not found in Bulk Edit table."
                )

            except StaleElementReferenceException:

                print(
                    f"Bulk Edit table became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

        raise TimeoutException(
            f"Product '{product_name}' "
            f"was not found after retries."
        )

    # =========================================================
    # SAVE SELECTED
    # =========================================================

    def clickSaveSelected(self):

        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnSaveSelected_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        print(
            "Save Selected button clicked"
        )

    # =========================================================
    # CONFIRM SAVE SELECTED
    # =========================================================

    def clickConfirmSelected(self):

        confirm_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.confirmSaveSelected_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            confirm_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            confirm_button
        )

        print(
            "Save Selected confirmation clicked"
        )

        # ---------------------------------------------------------
        # Wait for modal backdrop to disappear
        # ---------------------------------------------------------

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".modal-backdrop"
                )
            )
        )

        print(
            "Save Selected confirmation dialog closed"
        )

        # ---------------------------------------------------------
        # Wait for Bulk Edit table
        # ---------------------------------------------------------

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.products_table_xpath
                )
            )
        )

        print(
            "Bulk Edit table available after Save Selected"
        )

    # =========================================================
    # SAVE ALL
    # =========================================================

    def clickSaveAll(self):

        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnSaveAll_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        print(
            "Save All button clicked"
        )

    # =========================================================
    # CONFIRM SAVE ALL
    # =========================================================

    def clickConfirmSaveAll(self):

        confirm_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.confirmSaveAll_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            confirm_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            confirm_button
        )

        print(
            "Save All confirmation clicked"
        )

        # ---------------------------------------------------------
        # Wait for confirmation button/modal to disappear
        # ---------------------------------------------------------

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    self.confirmSaveAll_xpath
                )
            )
        )

        # ---------------------------------------------------------
        # Wait for Bootstrap backdrop
        # ---------------------------------------------------------

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".modal-backdrop"
                )
            )
        )

        print(
            "Save All confirmation dialog closed"
        )

        # ---------------------------------------------------------
        # Wait for Bulk Edit table
        # ---------------------------------------------------------

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.products_table_xpath
                )
            )
        )

        print(
            "Bulk Edit table available after Save All"
        )

    # =========================================================
    # BACK TO PRODUCTS LIST
    # =========================================================

    def clickBacktoProductsList(self):

        print(
            "Waiting for Save modal/backdrop to disappear..."
        )

        # =====================================================
        # STEP 1
        # Wait for modal backdrop
        # =====================================================

        try:

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".modal-backdrop"
                    )
                )
            )

            print(
                "Modal backdrop disappeared"
            )

        except TimeoutException:

            print(
                "Modal backdrop was not detected or "
                "did not disappear within timeout."
            )

        # =====================================================
        # STEP 2
        # Back link
        # =====================================================

        back_xpath = (
            "//a[@href='/Admin/Product/List']"
        )

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    back_xpath
                )
            )
        )

        print(
            "Back to Product List link found"
        )

        # =====================================================
        # STEP 3
        # Re-fetch and click link
        # =====================================================

        def click_back_link(driver):

            try:

                back_button = driver.find_element(
                    By.XPATH,
                    back_xpath
                )

                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    back_button
                )

                # Re-fetch immediately before clicking
                back_button = driver.find_element(
                    By.XPATH,
                    back_xpath
                )

                if not back_button.is_displayed():
                    return False

                if not back_button.is_enabled():
                    return False

                driver.execute_script(
                    "arguments[0].click();",
                    back_button
                )

                print(
                    "Back to Product List clicked"
                )

                return True

            except (
                StaleElementReferenceException,
                NoSuchElementException
            ):

                print(
                    "Back link became stale. "
                    "Re-fetching and retrying..."
                )

                return False

        # =====================================================
        # STEP 4
        # =====================================================

        self.wait.until(
            click_back_link
        )

        # =====================================================
        # STEP 5
        # Wait for Product List URL
        # =====================================================

        try:

            self.wait.until(
                EC.url_contains(
                    "/Admin/Product/List"
                )
            )

            print(
                "Returned to Products List URL"
            )

        except TimeoutException:

            print(
                "URL did not change after Back to Product List."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            # -------------------------------------------------
            # Fallback navigation
            # -------------------------------------------------

            base_url = (
                self.driver.current_url.split("/Admin")[0]
            )

            self.driver.get(
                base_url + "/Admin/Product/List"
            )

            self.wait.until(
                EC.url_contains(
                    "/Admin/Product/List"
                )
            )

        # =====================================================
        # STEP 6
        # Wait for Products List table
        # =====================================================

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "products-grid"
                )
            )
        )

        print(
            "Products List page loaded successfully"
        )

    # =========================================================
    # VERIFY PRODUCT IN PRODUCT LIST
    # =========================================================

    def isProductAddedInTable(self, product_name):

        product_name = product_name.strip()

        product_xpath = (
            "//table[@id='products-grid']"
            "//tbody//tr"
            "[td[contains(normalize-space(.), "
            f"'{product_name}')]]"
        )

        try:

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        product_xpath
                    )
                )
            )

            print(
                f"Product found in Products List: "
                f"{product_name}"
            )

            return True

        except TimeoutException:

            print(
                f"Product not found in Products List: "
                f"{product_name}"
            )

            return False

