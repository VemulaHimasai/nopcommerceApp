import os

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EditProductPage:

    # =========================================================
    # Products table
    # =========================================================
    tbl_producttable_xpath = "//table[@id='products-grid']"

    checkboxes_xpath = (
        "//table[@id='products-grid']//tbody/tr/td[1]/input"
    )

    btnDeleteSelected_xpath = "//button[@id='delete-selected']"

    # =========================================================
    # Product fields
    # =========================================================
    txtProductName_xpath = "//input[@id='Name']"
    txtshortdesc_xpath = "//textarea[@id='ShortDescription']"
    txtfulldesc_xpath = "//div[@role='textbox']"
    txtsku_xpath = "//input[@id='Sku']"

    # =========================================================
    # Prices
    # =========================================================
    prices_section = "//div[@id='product-price']"
    numprice_xpath = "//input[@id='Price']"

    # =========================================================
    # Tax Category
    # =========================================================
    drptax_category = (
        "//span[@id='select2-TaxCategoryId-container']"
    )

    lstBooks_element = "//li[contains(text(),'Books')]"
    lstelecsoftware_xpath = (
        "//li[contains(text(),'Electronics & Software')]"
    )
    lstdownloadproducts_xpath = (
        "//li[contains(text(),'Downloadable Products')]"
    )
    lstjewelry_xpath = "//li[contains(text(),'Jewelry')]"
    lstapparel_xpath = "//li[contains(text(),'Apparel')]"

    # =========================================================
    # Shipping
    # =========================================================
    shipping_section = "//div[@id='product-shipping']"

    weight_xpath = "//input[@id='Weight']"
    length_xpath = "//input[@id='Length']"
    width_xpath = "//input[@id='Width']"
    height_xpath = "//input[@id='Height']"

    # =========================================================
    # Inventory
    # =========================================================
    inventory_section = "//div[@id='product-inventory']"

    drpinventory = (
        "//span[@id='select2-ManageInventoryMethodId-container']"
    )

    lst_donttrack = (
        """//li[contains(., "Don't track inventory")]"""
    )

    lst_track = (
        "//li[normalize-space(.)='Track inventory']"
    )

    lst_track_product = (
        "//li[normalize-space(.)="
        "'Track inventory by product attributes']"
    )

    # =========================================================
    # Save
    # =========================================================
    btnSave_xpath = "//button[@name='save']"

    # =========================================================
    # Delete
    # =========================================================
    btnDelete_xpath = "//span[@id='product-delete']"

    # =========================================================
    # Success messages
    # =========================================================
    success_message_xpath = (
        "//div[contains(@class,'alert-success')]"
    )

    delete_success_message_xpath = (
        "//div[contains(@class,'alert-success') "
        "and contains(normalize-space(.),"
        "'The product has been deleted successfully')]"
    )

    # =========================================================
    # Constructor
    # =========================================================
    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            15,
            poll_frequency=0.2
        )

        os.makedirs(
            ".\\Screenshots",
            exist_ok=True
        )

    # =========================================================
    # Click Edit button for a particular product
    # =========================================================
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

    # =========================================================
    # Edit Product Name
    # =========================================================
    def setProductName(self, product_name):

        product_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtProductName_xpath)
            )
        )

        product_name_field.clear()
        product_name_field.send_keys(product_name)

        print(
            "Product name updated:",
            product_name
        )

    # =========================================================
    # Edit SKU
    # =========================================================
    def setSKU(self, sku):

        sku_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtsku_xpath)
            )
        )

        sku_field.clear()
        sku_field.send_keys(sku)

        print(
            "SKU updated:",
            sku
        )

    # =========================================================
    # Edit Price
    # =========================================================
    def setPrice(self, price):

        self.scrollToSection(
            self.prices_section
        )

        price_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.numprice_xpath)
            )
        )

        price_field.clear()
        price_field.send_keys(str(price))

        print(
            "Price updated:",
            price
        )

    # =========================================================
    # Save Product
    # =========================================================
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

                print(
                    "Save Button clicked"
                )

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

    # =========================================================
    # Verify Product Updated Successfully
    # =========================================================
    def isProductUpdatedSuccessfully(self):

        try:

            message = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        self.success_message_xpath
                    )
                )
            )

            actual_message = message.text.strip()

            print(
                "Success message:",
                actual_message
            )

            return message.is_displayed()

        except (
            StaleElementReferenceException,
            TimeoutException
        ):

            print(
                "Product update success message not found"
            )

            return False

    # =========================================================
    # Scroll to Section
    # =========================================================
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

    # =========================================================
    # Click Delete
    # =========================================================
    def clickDelete(self):

        print(
            "Waiting for Product Delete button..."
        )

        for attempt in range(3):

            try:

                delete_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.btnDelete_xpath)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    delete_button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    delete_button
                )

                print(
                    "Delete button clicked"
                )

                return

            except StaleElementReferenceException:

                print(
                    f"Delete button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    f"Delete button not clickable. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

    # =========================================================
    # Click Delete Selected
    # =========================================================
    def clickDeleteSelected(self):

        delete_selected_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnDeleteSelected_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            delete_selected_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            delete_selected_button
        )

        print(
            "Delete selected button clicked"
        )

    # =========================================================
    # Get Product Checkboxes
    # =========================================================
    def getProductCheckboxes(self):

        checkboxes = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, self.checkboxes_xpath)
            )
        )

        print(
            "Total product checkboxes:",
            len(checkboxes)
        )

        return checkboxes

    # =========================================================
    # Select Product Checkbox
    # =========================================================
    def selectProductCheckbox(self, row_number):

        checkboxes = self.getProductCheckboxes()

        if (
            row_number < 1
            or row_number > len(checkboxes)
        ):

            raise IndexError(
                f"Invalid row number: {row_number}. "
                f"Available rows: {len(checkboxes)}"
            )

        checkbox = checkboxes[row_number - 1]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            checkbox
        )

        if not checkbox.is_selected():

            self.driver.execute_script(
                "arguments[0].click();",
                checkbox
            )

            print(
                f"Product checkbox selected at row: "
                f"{row_number}"
            )

    # =========================================================
    # Confirm Delete
    # =========================================================
    def confirmDelete(self):

        print(
            "Waiting for Product Delete Confirmation..."
        )

        # -------------------------------------------------
        # Product delete confirmation modal
        # -------------------------------------------------
        modal_xpath = (
            "//div[contains(@class,'modal') "
            "and @role='dialog']"
            "[.//button[normalize-space()='Delete']]"
        )

        # -------------------------------------------------
        # Confirmation Delete button inside the modal
        # -------------------------------------------------
        confirm_button_xpath = (
                modal_xpath
                + "//button["
                  "normalize-space()='Delete'"
                  "and not(@id='product-delete')"
                  "]"
        )

        try:

            # =================================================
            # Wait for confirmation modal to exist
            # =================================================

            print(
                "Waiting for Product Delete confirmation modal..."
            )

            modal = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        modal_xpath
                    )
                )
            )

            print(
                "Product Delete confirmation modal found."
            )

            # =================================================
            # Wait for modal to become visible/active
            # =================================================

            self.wait.until(
                lambda driver: driver.execute_script(
                    """
                    const modal = arguments[0];

                    if (!modal) {
                        return false;
                    }

                    const style =
                        window.getComputedStyle(modal);

                    const rect =
                        modal.getBoundingClientRect();

                    return (
                        modal.classList.contains('show') &&
                        style.display !== 'none' &&
                        style.visibility !== 'hidden' &&
                        parseFloat(style.opacity) > 0 &&
                        rect.width > 0 &&
                        rect.height > 0
                    );
                    """,
                    self.driver.find_element(
                        By.XPATH,
                        modal_xpath
                    )
                )
            )

            print(
                "Product Delete confirmation modal is active."
            )

            # =================================================
            # Print modal message for diagnostics
            # =================================================

            try:

                modal_message = self.driver.execute_script(
                    """
                    const modal = arguments[0];

                    const body =
                        modal.querySelector('.modal-body');

                    return body
                        ? body.innerText.trim()
                        : '';
                    """,
                    self.driver.find_element(
                        By.XPATH,
                        modal_xpath
                    )
                )

                print(
                    "Delete confirmation message:",
                    repr(modal_message)
                )

            except Exception as e:

                print(
                    "Unable to read confirmation message:",
                    e
                )

            # =================================================
            # Locate confirmation button
            # =================================================

            print(
                "Waiting for confirmation Delete button..."
            )

            confirm_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        confirm_button_xpath
                    )
                )
            )

            print(
                "Confirmation Delete button found:",
                repr(confirm_button.text.strip())
            )

            # =================================================
            # Wait until button is actually visible
            # =================================================

            self.wait.until(
                lambda driver: driver.execute_script(
                    """
                    const button = arguments[0];

                    if (!button) {
                        return false;
                    }

                    const style =
                        window.getComputedStyle(button);

                    const rect =
                        button.getBoundingClientRect();

                    return (
                        style.display !== 'none' &&
                        style.visibility !== 'hidden' &&
                        parseFloat(style.opacity) > 0 &&
                        rect.width > 0 &&
                        rect.height > 0
                    );
                    """,
                    self.driver.find_element(
                        By.XPATH,
                        confirm_button_xpath
                    )
                )
            )

            # =================================================
            # Scroll button into view
            # =================================================

            confirm_button = self.driver.find_element(
                By.XPATH,
                confirm_button_xpath
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'nearest'
                });
                """,
                confirm_button
            )

            # =================================================
            # Re-locate after scrolling
            # =================================================

            confirm_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        confirm_button_xpath
                    )
                )
            )

            print(
                "Clicking confirmation Delete button..."
            )

            # =================================================
            # JS click
            # =================================================

            try:

                self.driver.execute_script(
                    "arguments[0].click();",
                    confirm_button
                )

            except StaleElementReferenceException:

                print(
                    "Confirmation button became stale. "
                    "Re-locating..."
                )

                confirm_button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            confirm_button_xpath
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    confirm_button
                )

            print(
                "Product Delete confirmation clicked."
            )

            # =================================================
            # Wait for Product List redirect
            # =================================================

            print(
                "Waiting for Product List redirect..."
            )

            self.wait.until(
                EC.url_contains(
                    "/Admin/Product/List"
                )
            )

            print(
                "Product List page loaded after deletion."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            # =================================================
            # Wait for Product grid
            # =================================================

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.tbl_producttable_xpath
                    )
                )
            )

            print(
                "Product table found."
            )

            print(
                "Product deletion completed successfully."
            )

        except TimeoutException:

            print(
                "\n========== DELETE CONFIRMATION FAILURE =========="
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Current Title:",
                self.driver.title
            )

            # -------------------------------------------------
            # Count possible Delete buttons
            # -------------------------------------------------

            try:

                delete_buttons = self.driver.find_elements(
                    By.XPATH,
                    "//button[normalize-space()='Delete']"
                )

                print(
                    "Total Delete buttons on page:",
                    len(delete_buttons)
                )

                for index, button in enumerate(
                        delete_buttons,
                        start=1
                ):

                    try:

                        print(
                            f"Delete button {index}:",
                            {
                                "id": button.get_attribute("id"),
                                "class": button.get_attribute("class"),
                                "style": button.get_attribute("style"),
                                "displayed": button.is_displayed(),
                                "enabled": button.is_enabled(),
                                "text": button.text.strip()
                            }
                        )

                    except StaleElementReferenceException:

                        print(
                            f"Delete button {index} became stale."
                        )

            except Exception as e:

                print(
                    "Unable to inspect Delete buttons:",
                    e
                )

            # -------------------------------------------------
            # Inspect modal elements
            # -------------------------------------------------

            try:

                modals = self.driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class,'modal')]"
                )

                print(
                    "Total modal elements:",
                    len(modals)
                )

                for index, current_modal in enumerate(
                        modals,
                        start=1
                ):

                    try:

                        print(
                            f"Modal {index}:",
                            self.driver.execute_script(
                                """
                                const modal = arguments[0];
                                const style =
                                    window.getComputedStyle(modal);

                                return {
                                    id: modal.id,
                                    className: modal.className,
                                    display: style.display,
                                    visibility: style.visibility,
                                    opacity: style.opacity,
                                    ariaHidden:
                                        modal.getAttribute(
                                            'aria-hidden'
                                        )
                                };
                                """,
                                current_modal
                            )
                        )

                    except StaleElementReferenceException:

                        print(
                            f"Modal {index} became stale."
                        )

            except Exception as e:

                print(
                    "Unable to inspect modals:",
                    e
                )

            # -------------------------------------------------
            # Body text
            # -------------------------------------------------

            try:

                print(
                    "\nCurrent page body:"
                )

                print(
                    self.driver.find_element(
                        By.TAG_NAME,
                        "body"
                    ).text
                )

            except Exception as e:

                print(
                    "Unable to read page body:",
                    e
                )

            # -------------------------------------------------
            # Screenshot
            # -------------------------------------------------

            try:

                screenshot_path = (
                    ".\\Screenshots\\"
                    "delete_confirmation_failure.png"
                )

                self.driver.save_screenshot(
                    screenshot_path
                )

                print(
                    "Failure screenshot saved:",
                    screenshot_path
                )

            except Exception as e:

                print(
                    "Unable to save screenshot:",
                    e
                )

            print(
                "===============================================\n"
            )

            raise

    # =========================================================
    # Click Edit Product By Row
    # =========================================================
    def clickEditProductByRow(self, row_number):

        edit_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody/tr[{row_number}]/td[8]/a[1]"
        )

        for attempt in range(3):

            try:

                print(
                    f"Waiting for Edit button "
                    f"at row {row_number}..."
                )

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
                    f"Edit button clicked for row: "
                    f"{row_number}"
                )

                self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            self.txtProductName_xpath
                        )
                    )
                )

                print(
                    "Edit Product page opened"
                )

                return

            except StaleElementReferenceException:

                print(
                    f"Edit button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    f"Edit Product row {row_number} "
                    f"operation timed out. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:

                    print(
                        "Current URL:",
                        self.driver.current_url
                    )

                    print(
                        "Current Title:",
                        self.driver.title
                    )

                    raise

    # =========================================================
    # Verify Product Deleted Successfully
    # =========================================================
    def isProductDeletedSuccessfully(self):

        expected_message = (
            "The product has been deleted successfully"
        )

        try:

            print(
                "Waiting for product deletion "
                "success message..."
            )

            message = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        self.delete_success_message_xpath
                    )
                )
            )

            actual_message = message.text.strip()

            print(
                "Delete success message:",
                repr(actual_message)
            )

            if expected_message in actual_message:

                print(
                    "Product deletion verified successfully."
                )

                return True

            print(
                "Unexpected delete success message:",
                repr(actual_message)
            )

            return False

        except StaleElementReferenceException:

            print(
                "Delete success message became stale. "
                "Retrying verification..."
            )

            try:

                message = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            self.delete_success_message_xpath
                        )
                    )
                )

                actual_message = message.text.strip()

                print(
                    "Delete success message after retry:",
                    repr(actual_message)
                )

                return expected_message in actual_message

            except TimeoutException:

                print(
                    "Delete success message not found "
                    "after retry."
                )

                return False

        except TimeoutException:

            print(
                "Product delete success message not found."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Current Title:",
                self.driver.title
            )

            try:

                print(
                    "Body text after deletion:"
                )

                print(
                    self.driver.find_element(
                        By.TAG_NAME,
                        "body"
                    ).text
                )

            except Exception as e:

                print(
                    "Unable to read body text:",
                    e
                )

            try:

                screenshot_path = (
                    ".\\Screenshots\\"
                    "delete_product_failure.png"
                )

                self.driver.save_screenshot(
                    screenshot_path
                )

                print(
                    "Failure screenshot saved:",
                    screenshot_path
                )

            except Exception as e:

                print(
                    "Unable to save failure screenshot:",
                    e
                )

            return False

    # =========================================================
    # Confirm Selected Delete
    # =========================================================
    def confirmselectedDelete(self):

        confirm_selected_btn_xpath = (
            "//button[@id="
            "'delete-selected-action-confirmation-submit-button']"
        )

        try:

            confirm_selected_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        confirm_selected_btn_xpath
                    )
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

            print(
                "Confirm selected button clicked"
            )

        except TimeoutException:

            print(
                "Delete Selected Confirmation "
                "button not found"
            )

            raise

    # =========================================================
    # Get Product Name By Row
    # =========================================================
    def getProductNameByRow(self, row_number):

        product_name_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody/tr[{row_number}]/td[3]"
        )

        product_name = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    product_name_xpath
                )
            )
        ).text.strip()

        print(
            f"Product name at row {row_number}: "
            f"{product_name}"
        )

        return product_name

    # =========================================================
    # Verify Product Is Deleted From Table
    # =========================================================
    def isProductDeletedFromTable(self, product_name):

        product_xpath = (
            f"{self.tbl_producttable_xpath}"
            f"//tbody/tr/td[3]"
            f"[normalize-space()='{product_name}']"
        )

        try:

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        product_xpath
                    )
                )
            )

            print(
                f"Product '{product_name}' "
                f"is no longer in the table"
            )

            return True

        except TimeoutException:

            print(
                f"Product '{product_name}' "
                f"still exists in the table"
            )

            return False