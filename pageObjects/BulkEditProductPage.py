import random

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BulkEditProductPage:

    # =========================================================
    # BULK EDIT / ADD NEW
    # =========================================================

    btnbulkedit_xpath = "//a[normalize-space()='Bulk edit products']"
    btnAddnew_xpath = "//a[normalize-space()='Add new']"

    # =========================================================
    # BULK EDIT FIELDS
    # =========================================================

    txtProductName_xpath = "//input[@id='name--1']"
    txtSKU_xpath = "//input[@id='sku--1']"

    # Prices
    new_price_xpath = "//input[@id='price--1']"
    old_price_xpath = "//input[@id='old-price--1']"

    # Stock
    stkquantity_xpath = "//input[@id='quantity--1']"

    # =========================================================
    # SAVE BUTTONS
    # =========================================================

    btnsaveselected_xpath = (
        "//button[@id='bulk-edit-save-selected']"
    )

    btnsaveall_xpath = (
        "//button[@id='bulk-edit-save-all']"
    )

    # =========================================================
    # BULK EDIT PRODUCTS TABLE
    # =========================================================

    products_table_xpath = (
        "//table[@class='table table-hover table-bordered table-striped']"
    )

    # =========================================================
    # CHECKBOXES
    # =========================================================

    checkboxes_table = (
        "//table[@class='table table-hover table-bordered table-striped']"
        "//tbody//tr/td[1]/input"
    )

    checkbox_table_head = (
        "//table[@class='table table-hover table-bordered table-striped']"
        "/thead/tr/th//input"
    )

    # =========================================================
    # BACK TO PRODUCT LIST
    # =========================================================

    lnk_backproductslist = (
        "//a[normalize-space()='back to product list']"
    )

    # =========================================================
    # INITIALIZE
    # =========================================================

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # =========================================================
    # SCROLL TO PRODUCTS TABLE
    # =========================================================

    def scrollToProductsTable(self):

        products_table = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.products_table_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({"
            "block:'center', inline:'nearest'"
            "});",
            products_table
        )

        print("Products table scrolled into view")

    # =========================================================
    # GET PRODUCT CHECKBOXES
    # =========================================================

    def getProductCheckboxes(self):

        self.scrollToProductsTable()

        checkboxes = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, self.checkboxes_table)
            )
        )

        print(
            "Total number of checkboxes:",
            len(checkboxes)
        )

        return checkboxes

    # =========================================================
    # SELECT PRODUCT CHECKBOX BY ROW
    # =========================================================

    def SelectProductCheckbox(self, row_number):

        checkboxes = self.getProductCheckboxes()

        if row_number < 1 or row_number > len(checkboxes):

            raise IndexError(
                f"Invalid row number: {row_number}. "
                f"Available rows: {len(checkboxes)}"
            )

        checkbox = checkboxes[row_number - 1]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({"
            "block:'center', inline:'nearest'"
            "});",
            checkbox
        )

        if not checkbox.is_selected():

            self.driver.execute_script(
                "arguments[0].click();",
                checkbox
            )

        print(
            f"Product checkbox selected at row {row_number}"
        )

    # =========================================================
    # CLICK SAVE SELECTED
    # =========================================================

    def clickSaveSelected(self):

        btnsave_selected = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnsaveselected_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            btnsave_selected
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btnsave_selected
        )

        print("Save Selected button clicked")

    # =========================================================
    # CONFIRM SAVE SELECTED
    # =========================================================

    def clickConfirmSelected(self):

        confirm_selected_xpath = (
            "//button[@id="
            "'bulk-edit-save-selected-action-confirmation-submit-button']"
        )

        try:

            confirm_selected_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, confirm_selected_xpath)
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                confirm_selected_btn
            )

            self.driver.execute_script(
                "arguments[0].click();",
                confirm_selected_btn
            )

            print("Save Selected confirmation clicked")

        except TimeoutException:

            print(
                "Save Selected confirmation button not found"
            )

            raise

    # =========================================================
    # CLICK BACK TO PRODUCTS LIST
    # =========================================================

    def clickBacktoProductsList(self):

        backproducts_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.lnk_backproductslist)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            backproducts_link
        )

        self.driver.execute_script(
            "arguments[0].click();",
            backproducts_link
        )

        print("Back to Products List clicked")

        # Wait until Products List URL is loaded
        self.wait.until(
            EC.url_contains("/Admin/Product/List")
        )

        # Wait for products DataTable
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//table[@id='products-grid']")
            )
        )

        print("Products list page loaded")

    # =========================================================
    # VERIFY PRODUCT IN PRODUCTS TABLE
    # =========================================================

    def isProductAddedInTable(self, product_name):

        product_xpath = (
            "//table[@id='products-grid']"
            "//tbody//tr"
            f"[td[contains(normalize-space(.), '{product_name}')]]"
        )

        def find_product(driver):

            try:

                rows = driver.find_elements(
                    By.XPATH,
                    product_xpath
                )

                for row in rows:

                    try:

                        if (
                            row.is_displayed()
                            and product_name in row.text.strip()
                        ):
                            return True

                    except StaleElementReferenceException:
                        continue

                return False

            except StaleElementReferenceException:
                return False

        try:

            self.wait.until(find_product)

            print(
                f"Product '{product_name}' is present in the table"
            )

            return True

        except TimeoutException:

            print(
                f"Product '{product_name}' is not present in the table"
            )

            try:
                print(
                    "Current URL:",
                    self.driver.current_url
                )

                print(
                    "Current Title:",
                    self.driver.title
                )

            except Exception:
                pass

            return False

    # =========================================================
    # CLICK ADD NEW
    # =========================================================

    def clickAddNew(self):

        add_new_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnAddnew_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_new_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            add_new_button
        )

        print("Add new button clicked")

        # IMPORTANT:
        # Wait until the Bulk Edit Add New field is loaded
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtProductName_xpath)
            )
        )

        print("Bulk Edit Add New page loaded")

    # =========================================================
    # CLICK BULK EDIT PRODUCTS
    # =========================================================

    def clickBulkEditProducts(self):

        bulk_edit_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnbulkedit_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            bulk_edit_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            bulk_edit_button
        )

        print("Bulk Edit products button clicked")

        # IMPORTANT:
        # Wait until Bulk Edit table is actually loaded
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.products_table_xpath)
            )
        )

        print("Bulk Edit products page loaded")

    # =========================================================
    # SET PRODUCT NAME
    # =========================================================

    def setProductName(self, product_name=None):

        if product_name is None:

            product_name = (
                "Test Product "
                + str(random.randint(1000, 9999))
            )

        for attempt in range(3):

            try:

                product_name_field = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, self.txtProductName_xpath)
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
                    f"Product name entered: {product_name}"
                )

                return product_name

            except StaleElementReferenceException:

                print(
                    "Product name field became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

        raise TimeoutException(
            "Product name field could not be located."
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

        sku_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtSKU_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            sku_field
        )

        sku_field.clear()

        sku_field.send_keys(sku)

        print(f"SKU entered: {sku}")

        return sku

    # =========================================================
    # SET NEW PRICE
    # =========================================================

    def setNewPrice(self, new_price=None):

        if new_price is None:
            new_price = 2000

        new_price_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.new_price_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            new_price_field
        )

        new_price_field.clear()

        new_price_field.send_keys(
            str(new_price)
        )

        print(
            f"New price entered: {new_price}"
        )

        return new_price

    # =========================================================
    # SET OLD PRICE
    # =========================================================

    def setOldPrice(self, old_price=None):

        if old_price is None:
            old_price = 1000

        old_price_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.old_price_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            old_price_field
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

    def setStockQuantity(self, stk_qntity=None):

        if stk_qntity is None:
            stk_qntity = 1000

        stk_qntity_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.stkquantity_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            stk_qntity_field
        )

        stk_qntity_field.clear()

        stk_qntity_field.send_keys(
            str(stk_qntity)
        )

        print(
            f"Stock quantity entered: {stk_qntity}"
        )

        return stk_qntity

    # =========================================================
    # CLICK SAVE ALL
    # =========================================================

    def clickSaveAll(self):

        btnsave = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnsaveall_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            btnsave
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btnsave
        )

        print("Save all button clicked")

    # =========================================================
    # CONFIRM SAVE ALL
    # =========================================================

    def clickConfirmSaveAll(self):

        confirm_xpath = (
            "//button[@id="
            "'bulk-edit-save-all-action-confirmation-submit-button']"
        )

        btn_confirm_saveall = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, confirm_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            btn_confirm_saveall
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn_confirm_saveall
        )

        print("Confirm all button clicked")

    # =========================================================
    # PRINT BULK EDIT PRODUCT ROWS
    # =========================================================

    def printProductRows(self):

        rows = self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//table[@class="
                    "'table table-hover table-bordered table-striped']"
                    "//tbody//tr"
                )
            )
        )

        print(
            f"Total Rows: {len(rows)}"
        )

        for index, row in enumerate(rows):

            try:

                name = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                ).get_attribute("value")

            except Exception:

                name = ""

            try:

                sku = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'sku-')]"
                ).get_attribute("value")

            except Exception:

                sku = ""

            print(
                f"Row {index}: "
                f"Product Name='{name}', "
                f"SKU='{sku}'"
            )

    # =========================================================
    # SELECT PRODUCT BY NAME
    # =========================================================

    def selectProductByName(self, product_name):

        rows_xpath = (
            "//table[@class="
            "'table table-hover table-bordered table-striped']"
            "//tbody//tr"
        )

        for attempt in range(3):

            try:

                rows = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, rows_xpath)
                    )
                )

                for index, row in enumerate(
                    rows,
                    start=1
                ):

                    try:

                        name_field = row.find_element(
                            By.XPATH,
                            ".//input[contains(@id,'name-')]"
                        )

                        current_product_name = (
                            name_field.get_attribute("value")
                        )

                        if (
                            current_product_name
                            == product_name
                        ):

                            checkbox = row.find_element(
                                By.XPATH,
                                ".//td[1]"
                                "//input[@type='checkbox']"
                            )

                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({"
                                "block:'center', "
                                "inline:'nearest'"
                                "});",
                                checkbox
                            )

                            if not checkbox.is_selected():

                                self.driver.execute_script(
                                    "arguments[0].click();",
                                    checkbox
                                )

                            print(
                                f"Product '{product_name}' "
                                f"checkbox selected at row {index}"
                            )

                            return

                    except StaleElementReferenceException:

                        continue

                print(
                    f"Product '{product_name}' "
                    f"not found. Retrying..."
                )

            except StaleElementReferenceException:

                print(
                    "Bulk Edit table became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

        raise TimeoutException(
            f"Product '{product_name}' "
            "was not found in the Bulk Edit table"
        )