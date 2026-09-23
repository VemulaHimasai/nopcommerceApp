import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
    ElementClickInterceptedException
)


class BulkEditProductPage:

    # ============================================================
    # LOCATORS
    # ============================================================

    btnbulkedit_xpath = "//a[normalize-space()='Bulk edit products']"

    # Actual nopCommerce Add New button
    btnAddnew_xpath = "//a[@onclick='addNewRow()']"

    # Bulk Edit product fields
    txtProductName_xpath = "//input[contains(@id,'name-')]"
    txtSKU_xpath = "//input[contains(@id,'sku-')]"

    # Prices
    new_price_xpath = "//input[contains(@id,'price-')]"
    old_price_xpath = "//input[contains(@id,'old-price-')]"

    # Inventory
    stkquantity_xpath = "//input[contains(@id,'quantity-')]"

    # Save Selected
    btnSaveSelected_xpath = (
        "//button[@id='bulk-edit-save-selected']"
    )

    confirmSaveSelected_xpath = (
        "//button[@id="
        "'bulk-edit-save-selected-action-confirmation-submit-button']"
    )

    # Save All
    btnSaveAll_xpath = (
        "//button[@id='bulk-edit-save-all']"
    )

    confirmSaveAll_xpath = (
        "//button[@id="
        "'bulk-edit-save-all-action-confirmation-submit-button']"
    )

    # Bulk Edit table
    products_table_xpath = (
        "//table[contains(@class,'table-hover') "
        "and contains(@class,'table-bordered') "
        "and contains(@class,'table-striped')]"
    )

    # Product checkboxes
    checkboxes_table = (
        products_table_xpath
        + "//tbody//tr[contains(@class,'product-row')]"
        + "//input[@type='checkbox']"
    )

    checkbox_table_head = (
        products_table_xpath
        + "/thead/tr/th//input"
    )

    # Back to normal Product List
    lnk_backproductslist = (
        "//a[normalize-space()='back to product list']"
    )

    # Normal Product List table
    product_list_table_xpath = (
        "//table[@id='products-grid']"
    )

    # ============================================================
    # CONSTRUCTOR
    # ============================================================

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.5
        )

        # Newly added product row
        self.new_product_row = None

        # Dynamic IDs
        self.new_product_name_id = None
        self.new_product_sku_id = None
        self.new_product_price_id = None
        self.new_product_old_price_id = None
        self.new_product_quantity_id = None

        self.new_product_name = None

    # ============================================================
    # GENERIC HELPERS
    # ============================================================

    def scrollIntoView(self, element):

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            element
        )

    def jsClick(self, element):

        self.scrollIntoView(element)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    # ============================================================
    # PRODUCT ROW METHODS
    # ============================================================

    def getProductRows(self):

        """
        Return only actual product rows.

        DataTables may create rows such as:
        'No data available in table'.

        Those rows are intentionally excluded.
        """

        return self.driver.find_elements(
            By.XPATH,
            self.products_table_xpath
            + "//tbody//tr[contains(@class,'product-row')]"
        )

    def waitForProductRows(
            self,
            minimum_rows=1,
            timeout=20
    ):

        """
        Wait until actual .product-row elements exist.
        """

        rows_xpath = (
            self.products_table_xpath
            + "//tbody//tr[contains(@class,'product-row')]"
        )

        print(
            "\n========== WAIT FOR PRODUCT ROWS =========="
        )

        def rows_loaded(driver):

            try:

                rows = driver.find_elements(
                    By.XPATH,
                    rows_xpath
                )

                print(
                    f"Current product rows: {len(rows)}"
                )

                if len(rows) >= minimum_rows:
                    return rows

                return False

            except StaleElementReferenceException:

                return False

        return WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=0.5
        ).until(rows_loaded)

    # ============================================================
    # WAIT FOR SPECIFIC PRODUCT
    # ============================================================

    def waitForProductByName(
            self,
            product_name,
            timeout=20
    ):

        """
        Wait until a specific product exists inside Bulk Edit.

        Product names are stored in input value attributes.
        """

        product_name = product_name.strip()

        rows_xpath = (
            self.products_table_xpath
            + "//tbody//tr[contains(@class,'product-row')]"
        )

        print(
            "\n========== WAIT FOR PRODUCT =========="
        )

        print(
            f"Expected product: {product_name}"
        )

        def find_product(driver):

            try:

                rows = driver.find_elements(
                    By.XPATH,
                    rows_xpath
                )

                print(
                    f"Checking {len(rows)} product rows..."
                )

                for row in rows:

                    try:

                        name_fields = row.find_elements(
                            By.XPATH,
                            ".//input[contains(@id,'name-')]"
                        )

                        if not name_fields:
                            continue

                        current_name = (
                            name_fields[0]
                            .get_attribute("value")
                            or ""
                        ).strip()

                        if current_name == product_name:

                            print(
                                f"FOUND PRODUCT: "
                                f"{product_name}"
                            )

                            return row

                    except StaleElementReferenceException:

                        continue

                return False

            except StaleElementReferenceException:

                return False

        return WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=0.5
        ).until(find_product)

    # ============================================================
    # BULK EDIT NAVIGATION
    # ============================================================

    def clickBulkEditProducts(self):

        print(
            "\n========== OPEN BULK EDIT =========="
        )

        for attempt in range(3):

            try:

                element = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.btnbulkedit_xpath
                        )
                    )
                )

                self.jsClick(element)

                # Wait until the browser actually navigates
                self.wait.until(
                    lambda driver:
                    "/Admin/Product/BulkEdit"
                    in driver.current_url
                )

                print(
                    f"Current url: "
                    f"{self.driver.current_url}"
                )

                # Confirm Bulk Edit page content
                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.products_table_xpath
                        )
                    )
                )

                print(
                    "Bulk Edit Products page "
                    "opened successfully."
                )

                return True

            except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException,
                    TimeoutException
            ):

                print(
                    f"Bulk Edit click retry "
                    f"{attempt + 1}/3"
                )

                time.sleep(0.5)

        raise TimeoutException(
            "Unable to open Bulk Edit Products page."
        )
    # ============================================================
    # ADD NEW PRODUCT
    # ============================================================

    def clickAddNew(self):

        print(
            "\n========== ADD NEW PRODUCT ROW =========="
        )

        # --------------------------------------------------------
        # Wait for Bulk Edit page
        # --------------------------------------------------------

        self.wait.until(
            EC.url_contains(
                "/Admin/Product/BulkEdit"
            )
        )

        # --------------------------------------------------------
        # Wait for Add New anchor
        # --------------------------------------------------------

        add_new = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.btnAddnew_xpath
                )
            )
        )

        print(
            "Add New element found."
        )

        print(
            "Add New outerHTML:",
            add_new.get_attribute("outerHTML")
        )

        # --------------------------------------------------------
        # Count existing product rows
        # --------------------------------------------------------

        rows_before = self.driver.find_elements(
            By.CSS_SELECTOR,
            "tr.product-row"
        )

        rows_before_count = len(rows_before)

        print(
            f"Product rows before Add New: "
            f"{rows_before_count}"
        )

        # --------------------------------------------------------
        # Scroll to Add New
        # --------------------------------------------------------

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            add_new
        )

        # --------------------------------------------------------
        # Click actual Add New anchor
        # --------------------------------------------------------

        self.driver.execute_script(
            "arguments[0].click();",
            add_new
        )

        print(
            "Add New clicked."
        )

        # --------------------------------------------------------
        # Wait for new product row
        #
        # DataTables may temporarily show:
        #
        # 1
        # 0
        # 0
        # 48
        #
        # Therefore wait until the row count becomes greater
        # than the original count.
        # --------------------------------------------------------

        def new_row_created(driver):

            try:

                rows = driver.find_elements(
                    By.CSS_SELECTOR,
                    "tr.product-row"
                )

                print(
                    f"Product rows after Add New: "
                    f"{len(rows)}"
                )

                if len(rows) > rows_before_count:

                    return rows[-1]

                return False

            except StaleElementReferenceException:

                return False

        self.new_product_row = WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.5
        ).until(
            new_row_created
        )

        print(
            "New product row detected."
        )

        # --------------------------------------------------------
        # Wait for Name field in new row
        # --------------------------------------------------------

        def get_name_input(driver):

            try:

                if not self.new_product_row:
                    return False

                return self.new_product_row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                )

            except (
                StaleElementReferenceException,
                NoSuchElementException
            ):

                # Re-find rows
                rows = driver.find_elements(
                    By.CSS_SELECTOR,
                    "tr.product-row"
                )

                if not rows:
                    return False

                self.new_product_row = rows[-1]

                try:

                    return self.new_product_row.find_element(
                        By.XPATH,
                        ".//input[contains(@id,'name-')]"
                    )

                except (
                    StaleElementReferenceException,
                    NoSuchElementException
                ):

                    return False

        name_input = WebDriverWait(
            self.driver,
            20,
            poll_frequency=0.5
        ).until(
            get_name_input
        )

        # --------------------------------------------------------
        # Store dynamic field IDs
        # --------------------------------------------------------

        self.new_product_name_id = (
            name_input.get_attribute("id")
        )

        try:

            self.new_product_sku_id = (
                self.new_product_row
                .find_element(
                    By.XPATH,
                    ".//input[contains(@id,'sku-')]"
                )
                .get_attribute("id")
            )

        except (
            NoSuchElementException,
            StaleElementReferenceException
        ):

            self.new_product_sku_id = None

        try:

            self.new_product_price_id = (
                self.new_product_row
                .find_element(
                    By.XPATH,
                    ".//input[contains(@id,'price-')]"
                )
                .get_attribute("id")
            )

        except (
            NoSuchElementException,
            StaleElementReferenceException
        ):

            self.new_product_price_id = None

        try:

            self.new_product_old_price_id = (
                self.new_product_row
                .find_element(
                    By.XPATH,
                    ".//input[contains(@id,'old-price-')]"
                )
                .get_attribute("id")
            )

        except (
            NoSuchElementException,
            StaleElementReferenceException
        ):

            self.new_product_old_price_id = None

        try:

            self.new_product_quantity_id = (
                self.new_product_row
                .find_element(
                    By.XPATH,
                    ".//input[contains(@id,'quantity-')]"
                )
                .get_attribute("id")
            )

        except (
            NoSuchElementException,
            StaleElementReferenceException
        ):

            self.new_product_quantity_id = None

        print(
            "New product row created successfully."
        )

        print(
            "New product name input ID:",
            self.new_product_name_id
        )

        print(
            "New product SKU input ID:",
            self.new_product_sku_id
        )

        print(
            "New product price input ID:",
            self.new_product_price_id
        )

        print(
            "New product old price input ID:",
            self.new_product_old_price_id
        )

        print(
            "New product quantity input ID:",
            self.new_product_quantity_id
        )

        return self.new_product_row

    # ============================================================
    # GET FIELD FROM NEW PRODUCT ROW
    # ============================================================

    def getNewProductField(self, field_xpath):

        """
        Return a field belonging to the newly added product row.
        """

        if self.new_product_row is None:

            raise TimeoutException(
                "New product row is not available. "
                "Call clickAddNew() first."
            )

        for attempt in range(3):

            try:

                field = self.new_product_row.find_element(
                    By.XPATH,
                    field_xpath
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    field
                )

                return field

            except (
                StaleElementReferenceException,
                NoSuchElementException
            ):

                print(
                    f"New product row/field became stale. "
                    f"Retrying field lookup "
                    f"({attempt + 1}/3)..."
                )

                # Re-find the row using the stored name ID
                if self.new_product_name_id:

                    try:

                        name_element = self.wait.until(
                            EC.presence_of_element_located(
                                (
                                    By.ID,
                                    self.new_product_name_id
                                )
                            )
                        )

                        self.new_product_row = (
                            name_element.find_element(
                                By.XPATH,
                                "./ancestor::tr"
                                "[contains(@class,'product-row')]"
                            )
                        )

                    except (
                        TimeoutException,
                        StaleElementReferenceException,
                        NoSuchElementException
                    ):

                        # Last fallback:
                        rows = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            "tr.product-row"
                        )

                        if rows:

                            self.new_product_row = rows[-1]

                time.sleep(0.5)

        raise TimeoutException(
            f"Unable to locate new product field: "
            f"{field_xpath}"
        )

    # ============================================================
    # SET PRODUCT NAME
    # ============================================================

    def setProductName(self, product_name=None):

        if product_name is None:
            product_name = (
                f"Test Product "
                f"{random.randint(1000, 9999)}"
            )

        product_name = product_name.strip()

        field = self.getNewProductField(
            ".//input[contains(@id,'name-')]"
        )

        field.clear()
        field.send_keys(product_name)

        # Store the actual product name so Save All
        # completion can verify it dynamically.
        self.new_product_name = product_name

        print(
            f"Product name entered: "
            f"{product_name}"
        )

        return product_name

    # ============================================================
    # SET SKU
    # ============================================================

    def setSKU(self, sku=None):

        if sku is None:

            sku = (
                f"SKU"
                f"{int(time.time() * 100) % 100000}"
            )

        sku = sku.strip()

        field = self.getNewProductField(
            ".//input[contains(@id,'sku-')]"
        )

        field.clear()
        field.send_keys(sku)

        print(
            f"SKU entered: {sku}"
        )

        return sku

    # ============================================================
    # SET NEW PRICE
    # ============================================================

    def setNewPrice(self, price=2000):

        field = self.getNewProductField(
            ".//input[contains(@id,'price-')]"
        )

        field.clear()
        field.send_keys(str(price))

        print(
            f"New price entered: {price}"
        )

        return price

    # ============================================================
    # SET OLD PRICE
    # ============================================================

    def setOldPrice(self, old_price=1000):

        field = self.getNewProductField(
            ".//input[contains(@id,'old-price-')]"
        )

        field.clear()
        field.send_keys(str(old_price))

        print(
            f"Old price entered: {old_price}"
        )

        return old_price

    # ============================================================
    # SET STOCK QUANTITY
    # ============================================================

    def setStockQuantity(self, quantity=1000):

        field = self.getNewProductField(
            ".//input[contains(@id,'quantity-')]"
        )

        field.clear()
        field.send_keys(str(quantity))

        print(
            f"Stock quantity entered: {quantity}"
        )

        return quantity

    # ============================================================
    # PRINT PRODUCT ROWS
    # ============================================================

    def printProductRows(self):

        print(
            "\n========== PRODUCT ROWS =========="
        )

        rows = self.getProductRows()

        print(
            f"Total product rows: {len(rows)}"
        )

        for index, row in enumerate(
                rows,
                start=1
        ):

            try:

                name_fields = row.find_elements(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                )

                sku_fields = row.find_elements(
                    By.XPATH,
                    ".//input[contains(@id,'sku-')]"
                )

                name = (
                    name_fields[0]
                    .get_attribute("value")
                    if name_fields
                    else ""
                )

                sku = (
                    sku_fields[0]
                    .get_attribute("value")
                    if sku_fields
                    else ""
                )

                print(
                    f"Row {index}: "
                    f"Name={name} | SKU={sku}"
                )

            except StaleElementReferenceException:

                print(
                    f"Row {index}: STALE"
                )

    # ============================================================
    # GET CHECKBOXES
    # ============================================================

    def getProductCheckboxes(self):

        return self.driver.find_elements(
            By.XPATH,
            self.checkboxes_table
        )

    # ============================================================
    # SELECT PRODUCT BY NAME
    # ============================================================

    def selectProductByName(self, product_name):

        product_name = product_name.strip()

        print(
            "\n========== SELECT PRODUCT =========="
        )

        print(
            f"Product: {product_name}"
        )

        for attempt in range(3):

            try:

                row = self.waitForProductByName(
                    product_name,
                    timeout=20
                )

                checkbox = row.find_element(
                    By.XPATH,
                    ".//input["
                    "@type='checkbox' "
                    "and contains("
                    "@class,'product-select'"
                    ")"
                    "]"
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    checkbox
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    checkbox
                )

                print(
                    f"Product '{product_name}' "
                    f"checkbox selected successfully."
                )

                return True

            except (
                StaleElementReferenceException,
                NoSuchElementException
            ):

                print(
                    f"Product row became stale or "
                    f"checkbox unavailable. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                time.sleep(0.5)

        raise TimeoutException(
            f"Product '{product_name}' "
            f"could not be selected."
        )

    # ============================================================
    # SELECT CHECKBOX BY INDEX
    # ============================================================

    def SelectProductCheckbox(self, index=0):

        print(
            "\n========== SELECT CHECKBOX =========="
        )

        checkboxes = self.getProductCheckboxes()

        if not checkboxes:

            raise TimeoutException(
                "No product checkboxes found."
            )

        if index >= len(checkboxes):

            raise IndexError(
                f"Checkbox index {index} "
                f"is outside available range."
            )

        checkbox = checkboxes[index]

        self.jsClick(checkbox)

        print(
            f"Checkbox {index} selected."
        )

    # ============================================================
    # SAVE SELECTED
    # ============================================================

    def clickSaveSelected(self):

        print(
            "\n========== SAVE SELECTED =========="
        )

        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnSaveSelected_xpath
                )
            )
        )

        self.jsClick(button)

        print(
            "Save Selected clicked."
        )

    # ============================================================
    # CONFIRM SAVE SELECTED
    # ============================================================

    def confirmSaveSelected(self):

        print(
            "\n========== "
            "CONFIRM SAVE SELECTED "
            "=========="
        )

        confirm_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.confirmSaveSelected_xpath
                )
            )
        )

        self.jsClick(confirm_button)

        print(
            "Save Selected confirmation clicked."
        )

        self.waitForSaveCompletion()

    # ============================================================
    # SAVE ALL
    # ============================================================

    def clickSaveAll(self):

        print(
            "\n========== SAVE ALL =========="
        )

        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnSaveAll_xpath
                )
            )
        )

        self.jsClick(button)

        print(
            "Save All clicked."
        )



    # ============================================================
    # CONFIRM SAVE ALL
    # ============================================================

    def confirmSaveAll(self):

        print(
            "\n========== "
            "CONFIRM SAVE ALL "
            "=========="
        )

        confirm_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.confirmSaveAll_xpath
                )
            )
        )

        self.jsClick(confirm_button)

        print(
            "Save All confirmation clicked."
        )

        # --------------------------------------------------------
        # IMPORTANT:
        # Wait until nopCommerce has actually processed
        # the Save All operation.
        # --------------------------------------------------------

        self.waitForSaveCompletion()

    # ============================================================
    # WAIT FOR SAVE COMPLETION
    # ============================================================

    def waitForSaveCompletion(self):

        print(
            "\n========== "
            "WAIT FOR SAVE COMPLETION "
            "=========="
        )

        # --------------------------------------------------------
        # 1. Wait for confirmation modal to close
        # --------------------------------------------------------

        try:

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        self.confirmSaveAll_xpath
                    )
                )
            )

            print(
                "Save All confirmation modal closed."
            )

        except TimeoutException:

            print(
                "Save All confirmation button did not "
                "become invisible within expected time."
            )

        # --------------------------------------------------------
        # 2. Wait for modal backdrop to disappear
        # --------------------------------------------------------

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
                "Save All modal backdrop disappeared."
            )

        except TimeoutException:

            print(
                "Modal backdrop did not disappear "
                "within expected time."
            )

        # --------------------------------------------------------
        # 3. Wait for Bulk Edit table
        # --------------------------------------------------------

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.products_table_xpath
                )
            )
        )

        print(
            "Bulk Edit table is available."
        )

        # --------------------------------------------------------
        # 4. Wait until newly added product field contains
        #    a value.
        #
        # IMPORTANT:
        # Do not rely only on the generated element ID for
        # database verification.
        # --------------------------------------------------------

        if self.new_product_name_id:

            print(
                "Waiting for newly saved product field..."
            )

            def saved_product_available(driver):

                try:

                    element = driver.find_element(
                        By.ID,
                        self.new_product_name_id
                    )

                    if not element.is_displayed():
                        return False

                    value = (
                            element.get_attribute("value")
                            or ""
                    ).strip()

                    return bool(value)

                except (
                        NoSuchElementException,
                        StaleElementReferenceException
                ):

                    return False

            try:

                self.wait.until(
                    saved_product_available
                )

                print(
                    "New product field is populated "
                    "after Save All."
                )

            except TimeoutException:

                print(
                    "New product field could not be "
                    "verified after Save All."
                )

        # --------------------------------------------------------
        # 5. Wait for Bulk Edit rows
        # --------------------------------------------------------

        try:

            self.waitForProductRows(
                minimum_rows=1,
                timeout=20
            )

            print(
                "Bulk Edit product rows are available."
            )

        except TimeoutException:

            print(
                "Bulk Edit product rows were not "
                "available after Save All."
            )

            raise

        # --------------------------------------------------------
        # 6. IMPORTANT:
        #    If product name is available, verify that the
        #    product still exists in the Bulk Edit table.
        #
        #    This uses the PRODUCT NAME rather than the dynamic
        #    generated input ID.
        # --------------------------------------------------------

        if getattr(self, "new_product_name", None):

            print(
                "\nWaiting for saved product by name:"
            )

            print(
                f"Product Name: {self.new_product_name}"
            )

            try:

                self.waitForProductByName(
                    self.new_product_name,
                    timeout=20
                )

                print(
                    f"Product '{self.new_product_name}' "
                    "is available after Save All."
                )

            except TimeoutException:

                print(
                    f"Product '{self.new_product_name}' "
                    "was NOT found in Bulk Edit "
                    "after Save All."
                )

                raise

        print(
            "\nSave All operation completed."
        )


    # ============================================================
    # SELECT ALL PRODUCTS
    # ============================================================

    def selectAllProducts(self):

        print(
            "\n========== "
            "SELECT ALL PRODUCTS "
            "=========="
        )

        checkbox = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.checkbox_table_head
                )
            )
        )

        self.jsClick(checkbox)

        print(
            "Select All checkbox clicked."
        )

    # ============================================================
    # BACK TO PRODUCT LIST
    # ============================================================

    def clickBacktoProductsList(self):

        print(
            "\n========== BACK TO PRODUCT LIST =========="
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Opening Product List "
                    f"(attempt {attempt}/3)"
                )

                back_link = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//a[@href='/Admin/Product/List']"
                        )
                    )
                )

                self.jsClick(back_link)

                self.wait.until(
                    EC.url_contains("/Admin/Product/List")
                )

                print(
                    "Product List URL reached:",
                    self.driver.current_url
                )

                # ---------------------------------------------
                # Wait for normal Product List table
                # ---------------------------------------------

                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.product_list_table_xpath
                        )
                    )
                )

                print(
                    "Product List table is available."
                )

                # ---------------------------------------------
                # Wait for DataTables processing to finish
                # ---------------------------------------------

                try:

                    self.wait.until(
                        EC.invisibility_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "#products-grid_processing"
                            )
                        )
                    )

                    print(
                        "Product List processing completed."
                    )

                except TimeoutException:

                    print(
                        "Product List processing indicator "
                        "was not detected or did not disappear."
                    )

                return True

            except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException,
                    TimeoutException
            ):

                print(
                    f"Back navigation retry "
                    f"{attempt}/3"
                )

                if attempt < 3:
                    time.sleep(1)
                else:
                    raise

        return False

    # ============================================================
    # WAIT FOR PRODUCT IN NORMAL PRODUCT LIST
    # ============================================================

    def waitForProductInProductList(
            self,
            product_name,
            timeout=20
    ):

        product_name = product_name.strip()

        print(
            "\n========== "
            "WAIT FOR PRODUCT LIST PRODUCT "
            "=========="
        )

        print(
            f"Expected product: {product_name}"
        )

        product_xpath = (
            self.product_list_table_xpath
            + "//tbody//tr"
            + "[td[contains("
            "normalize-space(.),"
            f"'{product_name}'"
            ")]]"
        )

        def find_product(driver):

            try:

                elements = driver.find_elements(
                    By.XPATH,
                    product_xpath
                )

                if elements:

                    print(
                        f"FOUND product in Product List: "
                        f"{product_name}"
                    )

                    return elements[0]

                return False

            except StaleElementReferenceException:

                return False

        return WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=0.5
        ).until(
            find_product
        )

    # ============================================================
    # CHECK PRODUCT IN NORMAL PRODUCT LIST
    # ============================================================

    def isProductAddedInTable(self, product_name):

        try:

            self.waitForProductInProductList(
                product_name,
                timeout=20
            )

            print(
                f"Product '{product_name}' "
                f"is present in Product List."
            )

            return True

        except TimeoutException:

            print(
                f"Product '{product_name}' "
                f"is NOT present in Product List."
            )

            return False

    # ============================================================
    # NO DATA CHECK
    # ============================================================

    def isNoDataAvailable(self):

        print(
            "\n========== "
            "CHECK NO DATA "
            "=========="
        )

        no_data_xpath = (
            self.products_table_xpath
            + "//tbody//td[contains("
            "normalize-space(),"
            "'No data available in table'"
            ")]"
        )

        try:

            WebDriverWait(
                self.driver,
                5
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        no_data_xpath
                    )
                )
            )

            print(
                "No data message found."
            )

            return True

        except TimeoutException:

            print(
                "No data message NOT found."
            )

            return False