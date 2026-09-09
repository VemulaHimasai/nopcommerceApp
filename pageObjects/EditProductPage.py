import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EditProductPage:

    # ---------------------------------------------------------
    # Products table
    # ---------------------------------------------------------
    tbl_producttable_xpath = "//table[@id='products-grid']"

    checkboxes_xpath = "//table[@id='products-grid']//tbody/tr/td[1]/input"

    btnDeleteSelected_xpath = "//button[@id='delete-selected']"

    # ---------------------------------------------------------
    # Product fields
    # ---------------------------------------------------------
    txtProductName_xpath = "//input[@id='Name']"
    txtshortdesc_xpath = "//textarea[@id='ShortDescription']"
    txtfulldesc_xpath = "//div[@role='textbox']"
    txtsku_xpath = "//input[@id='Sku']"

    # ---------------------------------------------------------
    # Prices
    # ---------------------------------------------------------
    prices_section = "//div[@id='product-price']"
    numprice_xpath = "//input[@id='Price']"

    # ---------------------------------------------------------
    # Tax Category
    # ---------------------------------------------------------
    drptax_category = "//span[@id='select2-TaxCategoryId-container']"

    lstBooks_element = "//li[contains(text(),'Books')]"
    lstelecsoftware_xpath = "//li[contains(text(),'Electronics & Software')]"
    lstdownloadproducts_xpath = "//li[contains(text(),'Downloadable Products')]"
    lstjewelry_xpath = "//li[contains(text(),'Jewelry')]"
    lstapparel_xpath = "//li[contains(text(),'Apparel')]"

    # ---------------------------------------------------------
    # Shipping
    # ---------------------------------------------------------
    shipping_section = "//div[@id='product-shipping']"

    weight_xpath = "//input[@id='Weight']"
    length_xpath = "//input[@id='Length']"
    width_xpath = "//input[@id='Width']"
    height_xpath = "//input[@id='Height']"

    # ---------------------------------------------------------
    # Inventory
    # ---------------------------------------------------------
    inventory_section = "//div[@id='product-inventory']"

    drpinventory = "//span[@id='select2-ManageInventoryMethodId-container']"

    lst_donttrack = """//li[contains(., "Don't track inventory")]"""
    lst_track = "//li[normalize-space(.)='Track inventory']"
    lst_track_product = (
        "//li[normalize-space(.)="
        "'Track inventory by product attributes']"
    )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------
    btnSave_xpath = "//button[@name='save']"

    #delete
    btnDelete_xpath = "//span[@id='product-delete']"

    # ---------------------------------------------------------
    # Success message
    # ---------------------------------------------------------
    success_message_xpath = "//div[contains(@class,'alert-success')]"

    delete_success_message_xpath = (
        "//div[@class ='alert alert-success alert-dismissable']"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ---------------------------------------------------------
    # Click Edit button for a particular product
    # ---------------------------------------------------------
    def clickEditProduct(self, product_name):

        edit_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody//tr"
            f"[td[contains(normalize-space(.),"
            f"'{product_name}')]]"
            f"/td[8]/a[1]"
        )

        for attempt in range(3):

            try:

                edit_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, edit_xpath)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    edit_button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    edit_button
                )

                print(
                    f"Edit button clicked for product: "
                    f"{product_name}"
                )

                return

            except StaleElementReferenceException:

                print(
                    f"Edit button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

    # ---------------------------------------------------------
    # Edit Product Name
    # ---------------------------------------------------------
    def setProductName(self, product_name):

        product_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtProductName_xpath)
            )
        )

        product_name_field.clear()
        product_name_field.send_keys(product_name)

        print("Product name updated:", product_name)

    # ---------------------------------------------------------
    # Edit SKU
    # ---------------------------------------------------------
    def setSKU(self, sku):

        sku_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtsku_xpath)
            )
        )

        sku_field.clear()
        sku_field.send_keys(sku)

        print("SKU updated:", sku)

    # ---------------------------------------------------------
    # Edit Price
    # ---------------------------------------------------------
    def setPrice(self, price):

        self.scrollToSection(self.prices_section)

        price_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.numprice_xpath)
            )
        )

        price_field.clear()
        price_field.send_keys(str(price))

        print("Price updated:", price)

    # ---------------------------------------------------------
    # Save Product
    # ---------------------------------------------------------
    def clickSave(self):

        for attempt in range(3):

            try:

                save_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.btnSave_xpath)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    save_button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    save_button
                )

                print("Save Button clicked")

                return

            except StaleElementReferenceException:

                print(
                    f"Save button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    f"Save button not clickable. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

    # ---------------------------------------------------------
    # Verify Product Updated Successfully
    # ---------------------------------------------------------
    def isProductUpdatedSuccessfully(self):

        try:

            message = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.success_message_xpath)
                )
            )

            actual_message = message.text.strip()

            print("Success message:", actual_message)

            return message.is_displayed()

        except (
            StaleElementReferenceException,
            TimeoutException
        ):

            print(
                "Product update success message not found"
            )

            return False

    # ---------------------------------------------------------
    # Scroll to Section
    # ---------------------------------------------------------
    def scrollToSection(self, section_xpath):

        section = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, section_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            section
        )
    def clickDelete(self):
        delete_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnDelete_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",delete_button)
        self.driver.execute_script("arguments[0].click();",delete_button)
        print("Delete button clicked")

    def clickDeleteSelected(self):
        delete_selected_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnDeleteSelected_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",delete_selected_button)
        self.driver.execute_script("arguments[0].click();",delete_selected_button)
        print("Delete selected button clicked")

    def getProductCheckboxes(self):
        checkboxes = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, self.checkboxes_xpath)
        ))
        print("Total product checkboxes: ",len(checkboxes))
        return checkboxes

    def selectProductCheckbox(self,row_number):
        checkboxes = self.getProductCheckboxes()
        if row_number < 1 or row_number > len(checkboxes):
            raise IndexError(
                f"Invalid row number: {row_number}. "
                f"Available rows: {len(checkboxes)}"
            )
        checkbox = checkboxes[row_number - 1]
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",checkbox)
        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();",checkbox)
            print(f"Product checkbox selected at row: {row_number}")


    def confirmDelete(self):
       try:
           delete_modal_xpath = (
               "//div[contains(@class,'modal') and contains(@class,'show')]"
           )
           delete_modal = self.wait.until(EC.visibility_of_element_located(
               (By.XPATH, delete_modal_xpath)
           ))
           print("Delete confirmation modal found")
           confirm_button_xpath = (
               "//button[normalize-space()='Delete' "
               "and not(contains(@style,'display: none'))]"
           )
           confirm_button = self.wait.until(EC.element_to_be_clickable(
               (By.XPATH, confirm_button_xpath)
           ))
           print("Delete confirmation button found: ",confirm_button.text)
           self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",confirm_button)
           confirm_button.click()
           print("Delete Confirmation clicked")
           self.wait.until(
               EC.url_contains("/Admin/Product/List")
           )
           print("Product List page loaded after deletion")
           self.wait.until(EC.presence_of_element_located(
               (By.XPATH,self.tbl_producttable_xpath)
           ))
           print("Product table found")
           print("Product deletion completed")
       except TimeoutException:
           print("Delete Confirmation not found")
           raise


    def clickEditProductByRow(self,row_number):
        edit_xpath = (
            f"{self.tbl_producttable_xpath}" f"//tbody/tr[{row_number}]/td[8]/a[1]"
        )
        for attempt in range(3):
            try:
                edit_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, edit_xpath)
                ))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",edit_button)
                self.driver.execute_script("arguments[0].click();",edit_button)
                print(f"Edit button clicked for row: {row_number}")
                self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH,self.txtProductName_xpath)
                ))
                print("Edit Product page opened")
                return
            except StaleElementReferenceException:
                print(
                    f"Edit button became stale. " f"Retrying ({attempt + 1}/3)..."
                )
                if attempt == 2:
                    raise
            except TimeoutException:
                print(
                    f"Edit button became stale. " f"Retrying ({attempt + 1}/3)..."
                )
                if attempt == 2:
                    raise

    # ---------------------------------------------------------
    def isProductDeletedSuccessfully(self):

        try:

            message = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.delete_success_message_xpath)
                )
            )

            actual_message = message.text.strip()

            expected_message = "The product has been deleted successfully."

            print("Delete success message:", actual_message)

            return expected_message in actual_message

        except (
                StaleElementReferenceException,
                TimeoutException
        ):

            print("Product delete success message not found")

            return False

    def confirmselectedDelete(self):
        confirm_selected_btn_xpath = "//button[@id='delete-selected-action-confirmation-submit-button']"
        try:
            confirm_selected_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, confirm_selected_btn_xpath)
            ))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",confirm_selected_btn)
            self.driver.execute_script("arguments[0].click();",confirm_selected_btn)
            print("Confirm selected button clicked")
        except TimeoutException:
            print("Delete Selected Confirmation button not found")
            raise

    def getProductNameByRow(self,row_number):
        product_name_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody/tr[{row_number}]/td[3]"
        )
        product_name = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, product_name_xpath)
        )).text.strip()
        print(f"Product name at row {row_number}: {product_name}")
        return product_name

    def isProductDeletedFromTable(self,product_name):
        product_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody/tr/td[3]"
            f"[normalize-space()='{product_name}']"
        )
        try:
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, product_xpath)
            ))
            print(f"Product {product_name} is no longer in the table")
            return True
        except TimeoutException:
            print(f"Product {product_name} is still exists in the table")
            return False






