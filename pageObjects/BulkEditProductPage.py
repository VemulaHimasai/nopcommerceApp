import random

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BulkEditProductPage:

    btnbulkedit_xpath = "//a[normalize-space()='Bulk edit products']"
    btnAddnew_xpath = "//a[normalize-space()='Add new']"

    txtProductName_xpath = "//input[@id='name--1']"
    txtSKU_xpath = "//input[@id='sku--1']"

    # Prices
    new_price_xpath = "//input[@id='price--1']"
    old_price_xpath = "//input[@id='old-price--1']"
    stkquantity_xpath = "//input[@id='quantity--1']"

    # Save buttons
    btnsaveselected_xpath = "//button[@id='bulk-edit-save-selected']"
    btnsaveall_xpath = "//button[@id='bulk-edit-save-all']"

    # Products table
    products_table_xpath = (
        "//table[@class='table table-hover table-bordered table-striped']"
    )

    # Checkboxes
    checkboxes_table = (
        "//table[@class='table table-hover table-bordered table-striped']"
        "//tbody//tr/td[1]/input"
    )

    checkbox_table_head = (
        "//table[@class='table table-hover table-bordered table-striped']"
        "/thead/tr/th//input"
    )

    lnk_backproductslist = "//a[normalize-space()='back to product list']"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def scrollToProductsTable(self):
        products_table = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.products_table_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', inline:'nearest'});",
            products_table
        )

        print("Products table scrolled into view")

    def getProductCheckboxes(self):
        self.scrollToProductsTable()

        checkboxes = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, self.checkboxes_table)
            )
        )

        print("Total number of checkboxes:", len(checkboxes))
        return checkboxes

    def SelectProductCheckbox(self, row_number):
        checkboxes = self.getProductCheckboxes()

        if row_number < 1 or row_number > len(checkboxes):
            raise IndexError(
                f"Invalid row number: {row_number}. "
                f"Available rows: {len(checkboxes)}"
            )

        checkbox = checkboxes[row_number - 1]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', inline:'nearest'});",
            checkbox
        )

        if not checkbox.is_selected():
            self.driver.execute_script(
                "arguments[0].click();",
                checkbox
            )

        print(f"Product checkbox selected at row {row_number}")

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

    def clickConfirmSelected(self):
        confirm_selected_xpath = (
            "//button[@id='bulk-edit-save-selected-action-confirmation-submit-button']"
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
            print("Save Selected confirmation button not found")
            raise

    def clickBacktoProductsList(self):
        try:
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

        except TimeoutException:
            print("No Back to Products List link found")
            raise

    def isProductAddedInTable(self, product_name):
        product_xpath = (
            "//table[@id='products-grid']"
            f"//tbody//tr[td[contains(normalize-space(.), '{product_name}')]]"
        )

        try:
            product = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, product_xpath)
                )
            )

            print(f"Product '{product_name}' is present in the table")
            return product.is_displayed()

        except TimeoutException:
            print(f"Product '{product_name}' is not present in the table")
            return False

    def clickAddNew(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnAddnew_xpath)
        )).click()
        print("Add new button clicked")

    def clickBulkEditProducts(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnbulkedit_xpath)
        )).click()
        print("Bulk Edit products button clicked")

    def setProductName(self,product_name=None):
        product_name_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.txtProductName_xpath)
        ))
        if product_name is None:
            product_name = "Test Product " + str(random.randint(1000,9999))
        product_name_field.clear()
        product_name_field.send_keys(product_name)
        return product_name

    def setSKU(self,sku=None):
        sku_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.txtSKU_xpath)
        ))
        if sku is None:
            sku = "SKU " + str(random.randint(10000,99999))
        sku_field.clear()
        sku_field.send_keys(sku)
        return sku
    def setNewPrice(self,new_price=None):
        new_price_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.new_price_xpath)
        ))
        if new_price is None:
            new_price = 2000
        new_price_field.clear()
        new_price_field.send_keys(str(new_price))
        return new_price

    def setOldPrice(self,old_price=None):
        old_price_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.old_price_xpath)
        ))
        if old_price is None:
            old_price = 1000
        old_price_field.clear()
        old_price_field.send_keys(str(old_price))
        return old_price

    def setStockQuantity(self,stk_qntity=None):
        stk_qntity_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.stkquantity_xpath)
        ))
        if stk_qntity is None:
            stk_qntity = 1000
        stk_qntity_field.clear()
        stk_qntity_field.send_keys(str(stk_qntity))
        return stk_qntity

    def clickSaveAll(self):
        btnsave = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnsaveall_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btnsave)
        self.driver.execute_script("arguments[0].click();", btnsave)
        print("Save all button clicked")

    def clickConfirmSaveAll(self):
        btn_confirm_saveall = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,"//button[@id='bulk-edit-save-all-action-confirmation-submit-button']")
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",btn_confirm_saveall)
        self.driver.execute_script("arguments[0].click();", btn_confirm_saveall)
        print("Confirm all button clicked")

    def printProductRows(self):
        rows = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@class='table table-hover table-bordered table-striped']//tbody//tr")
        ))
        print(f"Total Rows: {len(rows)}")
        for index, row in enumerate(rows):
            try:
                name = row.find_element(By.XPATH,".//input[contains(@id,'name-')]").get_attribute("value")
            except:
                name = ""
            try:
                sku = row.find_element(By.XPATH,".//input[contains(@id,'sku-')]").get_attribute("value")
            except:
                sku=""
            print(f"Row {index}: Product Name='{name}', SKU='{sku}'")

    def selectProductByName(self, product_name):

        rows = self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//table[@class='table table-hover table-bordered table-striped']"
                    "//tbody//tr"
                )
            )
        )

        for index, row in enumerate(rows, start=1):

            try:
                name_field = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                )

                current_product_name = name_field.get_attribute("value")

                if current_product_name == product_name:

                    checkbox = row.find_element(
                        By.XPATH,
                        ".//td[1]//input[@type='checkbox']"
                    )

                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center', inline:'nearest'});",
                        checkbox
                    )

                    if not checkbox.is_selected():
                        self.driver.execute_script(
                            "arguments[0].click();",
                            checkbox
                        )

                    print(
                        f"Product '{product_name}' checkbox selected "
                        f"at row {index}"
                    )

                    return

            except StaleElementReferenceException:
                continue

        raise TimeoutException(
            f"Product '{product_name}' was not found in the Bulk Edit table"
        )
