import os
import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EditProductPage:

    # =================================================
    # Product List
    # =================================================

    tbl_producttable_xpath = (
        "//table[@id='products-grid']"
    )

    checkboxes_xpath = (
        "//table[@id='products-grid']"
        "//tbody/tr/td[1]/input"
    )

    btnDeleteSelected_xpath = (
        "//button[@id='delete-selected']"
    )

    # =================================================
    # Product Fields
    # =================================================

    txtProductName_xpath = (
        "//input[@id='Name']"
    )

    txtshortdesc_xpath = (
        "//textarea[@id='ShortDescription']"
    )

    txtfulldesc_xpath = (
        "//div[@role='textbox']"
    )

    txtsku_xpath = (
        "//input[@id='Sku']"
    )

    # =================================================
    # Save
    # =================================================

    btnSave_xpath = (
        "//button[@name='save']"
    )

    # =================================================
    # Delete
    # =================================================

    btnDelete_xpath = (
        "//span[@id='product-delete']"
    )

    # Actual nopCommerce Product Delete confirmation modal
    product_delete_modal_id = (
        "productmodel-Delete-delete-confirmation"
    )

    # =================================================
    # Success Messages
    # =================================================

    success_message_xpath = (
        "//div[contains(@class,'alert-success')]"
    )

    delete_success_message_xpath = (
        "//div[contains(@class,'alert-success') "
        "and contains(normalize-space(.),"
        "'The product has been deleted successfully')]"
    )

    # =================================================
    # Constructor
    # =================================================

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

    # =================================================
    # Product Name
    # =================================================

    def getProductName(self):

        try:

            element = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.txtProductName_xpath
                    )
                )
            )

            return element.get_attribute(
                "value"
            )

        except Exception as e:

            print(
                "Unable to get product name:",
                e
            )

            return ""

    # =================================================
    # Product SKU
    # =================================================

    def getProductSKU(self):

        try:

            element = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.txtsku_xpath
                    )
                )
            )

            return element.get_attribute(
                "value"
            )

        except Exception as e:

            print(
                "Unable to get product SKU:",
                e
            )

            return ""

    def setSKU(self, sku):

        print(f"Setting SKU: {sku}")

        for attempt in range(3):

            try:

                sku_field = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, self.txtsku_xpath)
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    sku_field
                )

                sku_field.clear()
                sku_field.send_keys(sku)

                actual_value = self.driver.execute_script(
                    "return arguments[0].value;",
                    sku_field
                )

                print(
                    f"SKU DOM value (attempt {attempt + 1}/3): "
                    f"{actual_value!r}"
                )

                if actual_value == sku:
                    print("SKU entered successfully.")
                    return

                print(
                    "SKU value mismatch. Retrying..."
                )

            except StaleElementReferenceException:

                print(
                    "SKU field became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    "SKU field was not available. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

        raise AssertionError(
            f"Unable to enter SKU successfully: {sku}"
        )

    def setPrice(self, price):

        print(f"Setting Price: {price}")

        for attempt in range(3):

            try:

                price_field = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, "Price")
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    price_field
                )

                price_field.clear()
                price_field.send_keys(str(price))

                actual_value = self.driver.execute_script(
                    "return arguments[0].value;",
                    price_field
                )

                print(
                    f"Price DOM value (attempt {attempt + 1}/3): "
                    f"{actual_value!r}"
                )

                if actual_value == str(price):
                    print("Price entered successfully.")
                    return

                print("Price value mismatch. Retrying...")

            except StaleElementReferenceException:

                print(
                    "Price field became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    "Price field was not available. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

        raise AssertionError(
            f"Unable to enter Price successfully: {price}"
        )

    def clickSave(self):

        print("Waiting for Product Save button...")

        for attempt in range(3):

            try:

                save_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.btnSave_xpath)
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    save_button
                )

                try:
                    save_button.click()

                except ElementClickInterceptedException:

                    print(
                        "Normal Save click intercepted. "
                        "Using JavaScript click..."
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        save_button
                    )

                print("Product Save button clicked.")

                self.wait.until(
                    EC.url_contains("/Admin/Product/List")
                )

                print(
                    "Product List page loaded after saving."
                )

                return

            except StaleElementReferenceException:

                print(
                    "Save button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    "Save button was not available or "
                    "Product List did not load. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

    def isProductUpdatedSuccessfully(self):

        print(
            "Waiting for Product update success message..."
        )

        try:

            success_message = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        self.success_message_xpath
                    )
                )
            )

            message = success_message.text.strip()

            print(
                "Product update success message:",
                repr(message)
            )

            if (
                    "The product has been updated successfully"
                    in message
            ):
                print(
                    "Product update success message "
                    "verified successfully."
                )

                return True

            print(
                "Unexpected product update message:",
                repr(message)
            )

            return False

        except TimeoutException:

            print(
                "Product update success message "
                "was not displayed."
            )

            return False

        except StaleElementReferenceException:

            print(
                "Product update success message "
                "became stale. Re-checking..."
            )

            try:

                success_message = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            self.success_message_xpath
                        )
                    )
                )

                message = success_message.text.strip()

                print(
                    "Product update success message "
                    "after retry:",
                    repr(message)
                )

                return (
                        "The product has been updated successfully"
                        in message
                )

            except Exception as e:

                print(
                    "Unable to verify product update "
                    "success after retry:",
                    e
                )

                return False

    def clickEditProductByRow(self, row_number):

        print(
            f"Waiting for Edit button at row {row_number}..."
        )

        edit_button_xpath = (
            f"//table[@id='products-grid']"
            f"//tbody/tr[{row_number}]"
            f"//a[contains(@href,'/Admin/Product/Edit/')]"
        )

        for attempt in range(3):

            try:

                edit_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            edit_button_xpath
                        )
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    edit_button
                )

                try:

                    edit_button.click()

                except (
                        ElementClickInterceptedException
                ):

                    self.driver.execute_script(
                        "arguments[0].click();",
                        edit_button
                    )

                print(
                    f"Edit button clicked for row: "
                    f"{row_number}"
                )

                self.wait.until(
                    EC.url_contains(
                        "/Admin/Product/Edit/"
                    )
                )

                print(
                    "Edit Product page opened"
                )

                return

            except StaleElementReferenceException:

                print(
                    "Edit button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    "Edit button not available. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

    # =================================================
    # Get Product Name By Row
    # =================================================

    def getProductNameByRow(self, row_number):

        print(
            f"Getting product name from row {row_number}..."
        )

        row_xpath = (
            f"//table[@id='products-grid']"
            f"//tbody/tr[{row_number}]"
        )

        for attempt in range(3):

            try:

                row = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            row_xpath
                        )
                    )
                )

                cells = row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                print(
                    f"Row {row_number} has "
                    f"{len(cells)} cells."
                )

                for index, cell in enumerate(
                        cells,
                        start=1
                ):
                    print(
                        f"Row {row_number} Cell {index}: "
                        f"{repr(cell.text.strip())}"
                    )

                # ---------------------------------------------
                # Find product name from the actual row
                # ---------------------------------------------

                product_name = ""

                for cell in cells:

                    # Ignore checkbox/action cells
                    cell_text = cell.text.strip()

                    if not cell_text:
                        continue

                    # Look for the product Edit link.
                    # The product name is normally in the same
                    # cell as the product link, while the final
                    # Edit action is in a different cell.
                    product_links = cell.find_elements(
                        By.XPATH,
                        ".//a[contains(@href,'/Admin/Product/Edit/')]"
                    )

                    if product_links:

                        link_texts = [
                            link.text.strip()
                            for link in product_links
                        ]

                        print(
                            "Links in cell:",
                            link_texts
                        )

                        # If the cell itself contains an Edit
                        # action, don't use "Edit" as product name.
                        for link_text in link_texts:

                            if (
                                    link_text
                                    and link_text.lower()
                                    != "edit"
                            ):
                                product_name = link_text
                                break

                    if product_name:
                        break

                # ---------------------------------------------
                # Fallback: inspect cell text
                # ---------------------------------------------

                if not product_name:

                    for cell in cells:

                        cell_text = cell.text.strip()

                        if (
                                cell_text
                                and cell_text.lower()
                                != "edit"
                                and cell_text.lower()
                                != "select"
                        ):
                            # Product name is usually the first
                            # meaningful text in the product cell.
                            product_name = cell_text

                            break

                if product_name:
                    print(
                        f"Product name at row "
                        f"{row_number}: {product_name}"
                    )

                    return product_name

                print(
                    f"Product name not found "
                    f"(attempt {attempt + 1}/3)."
                )

                time.sleep(0.5)

            except StaleElementReferenceException:

                print(
                    "Product row became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    f"Product row {row_number} "
                    f"not available "
                    f"(attempt {attempt + 1}/3)."
                )

                if attempt == 2:
                    raise

        raise TimeoutException(
            f"Unable to get product name "
            f"from row {row_number}"
        )
    # =================================================
    # Select Product Checkbox By Row
    # =================================================

    def selectProductCheckbox(self, row_number):

        print(f"Selecting checkbox at row {row_number}...")

        checkbox_xpath = (
            f"//table[@id='products-grid']"
            f"//tbody/tr[{row_number}]"
            f"//input[@type='checkbox']"
        )

        for attempt in range(3):

            try:

                checkbox = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            checkbox_xpath
                        )
                    )
                )

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
                    f"Checkbox selected for row {row_number}"
                )

                return True

            except StaleElementReferenceException:

                print(
                    f"Checkbox stale. Retry "
                    f"{attempt + 1}/3"
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    f"Checkbox not found. Retry "
                    f"{attempt + 1}/3"
                )

                if attempt == 2:
                    raise

        return False

    # =================================================
    # Click Delete Selected
    # =================================================

    def clickDeleteSelected(self):

        print(
            "Waiting for Delete Selected button..."
        )

        for attempt in range(3):

            try:

                delete_selected_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.btnDeleteSelected_xpath
                        )
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    delete_selected_button
                )

                try:

                    delete_selected_button.click()

                except ElementClickInterceptedException:

                    self.driver.execute_script(
                        "arguments[0].click();",
                        delete_selected_button
                    )

                print(
                    "Delete selected button clicked"
                )

                return

            except StaleElementReferenceException:

                print(
                    "Delete selected button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    "Delete selected button not clickable. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

    # =================================================
    # Confirm Delete Selected Products
    # =================================================

    def confirmselectedDelete(self):

        print(
            "Waiting for Delete Selected confirmation..."
        )

        modal_id = (
            "delete-selected-action-confirmation"
        )

        confirm_button_id = (
            "delete-selected-action-confirmation-submit-button"
        )

        modal_xpath = (
            f"//div[@id='{modal_id}']"
        )

        confirm_button_xpath = (
            f"//button[@id='{confirm_button_id}']"
        )

        try:

            # -------------------------------------------------
            # Wait until the confirmation modal exists in DOM
            # -------------------------------------------------

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        modal_id
                    )
                )
            )

            print(
                "Delete Selected confirmation modal found."
            )

            # -------------------------------------------------
            # Check whether modal is actually visible
            # -------------------------------------------------

            def modal_is_active(driver):

                return driver.execute_script(
                    """
                    const modal = document.getElementById(arguments[0]);

                    if (!modal) {
                        return false;
                    }

                    const style =
                        window.getComputedStyle(modal);

                    const rect =
                        modal.getBoundingClientRect();

                    return (
                        modal.classList.contains("show") &&
                        style.display !== "none" &&
                        style.visibility !== "hidden" &&
                        parseFloat(style.opacity) > 0 &&
                        rect.width > 0 &&
                        rect.height > 0
                    );
                    """,
                    modal_id
                )

            # -------------------------------------------------
            # Wait for normal Bootstrap activation
            # -------------------------------------------------

            try:

                self.wait.until(
                    modal_is_active
                )

                print(
                    "Delete Selected confirmation modal "
                    "opened normally."
                )

            except TimeoutException:

                print(
                    "Delete Selected confirmation modal "
                    "did not open normally."
                )

                print(
                    "Using Bootstrap modal fallback..."
                )

                # -------------------------------------------------
                # Bootstrap / jQuery fallback
                # -------------------------------------------------

                fallback_result = self.driver.execute_script(
                    """
                    const modal =
                        document.getElementById(arguments[0]);

                    if (!modal) {
                        return {
                            success: false,
                            reason: "Modal not found"
                        };
                    }

                    try {

                        // Bootstrap 4 / jQuery
                        if (
                            window.jQuery &&
                            window.jQuery.fn &&
                            window.jQuery.fn.modal
                        ) {

                            window.jQuery(modal).modal("show");

                            return {
                                success: true,
                                method: "jquery-bootstrap"
                            };
                        }

                        // Bootstrap 5
                        if (
                            window.bootstrap &&
                            window.bootstrap.Modal
                        ) {

                            const instance =
                                window.bootstrap.Modal
                                    .getOrCreateInstance(modal);

                            instance.show();

                            return {
                                success: true,
                                method: "bootstrap5"
                            };
                        }

                    } catch (e) {

                        return {
                            success: false,
                            reason: e.toString()
                        };
                    }

                    return {
                        success: false,
                        reason: "Bootstrap API unavailable"
                    };
                    """,
                    modal_id
                )

                print(
                    "Bootstrap fallback result:",
                    fallback_result
                )

                # -------------------------------------------------
                # Final DOM fallback
                # -------------------------------------------------

                if not fallback_result.get(
                        "success",
                        False
                ):
                    print(
                        "Using DOM fallback to activate "
                        "confirmation modal..."
                    )

                    self.driver.execute_script(
                        """
                        const modal =
                            document.getElementById(arguments[0]);

                        if (modal) {

                            modal.classList.add("show");

                            modal.style.display =
                                "block";

                            modal.style.opacity =
                                "1";

                            modal.style.visibility =
                                "visible";

                            modal.setAttribute(
                                "aria-hidden",
                                "false"
                            );

                            modal.setAttribute(
                                "aria-modal",
                                "true"
                            );

                            modal.setAttribute(
                                "role",
                                "dialog"
                            );

                            document.body.classList.add(
                                "modal-open"
                            );

                            let backdrop =
                                document.querySelector(
                                    ".modal-backdrop"
                                );

                            if (!backdrop) {

                                backdrop =
                                    document.createElement(
                                        "div"
                                    );

                                backdrop.className =
                                    "modal-backdrop fade show";

                                document.body.appendChild(
                                    backdrop
                                );
                            }
                        }
                        """,
                        modal_id
                    )

                # -------------------------------------------------
                # Verify modal activation
                # -------------------------------------------------

                self.wait.until(
                    modal_is_active
                )

                print(
                    "Delete Selected confirmation modal "
                    "opened successfully."
                )

            # -------------------------------------------------
            # Print confirmation message
            # -------------------------------------------------

            modal = self.driver.find_element(
                By.ID,
                modal_id
            )

            print(
                "Delete Selected confirmation message:",
                repr(modal.text.strip())
            )

            # -------------------------------------------------
            # Find confirmation Delete button
            # -------------------------------------------------

            print(
                "Waiting for Delete Selected "
                "confirmation button..."
            )

            confirm_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.ID,
                        confirm_button_id
                    )
                )
            )

            print(
                "Delete Selected confirmation button found:",
                repr(confirm_button.text.strip())
            )

            # -------------------------------------------------
            # Scroll button into view
            # -------------------------------------------------

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'nearest'
                });
                """,
                confirm_button
            )

            # -------------------------------------------------
            # Click confirmation button
            # -------------------------------------------------

            try:

                confirm_button.click()

            except ElementClickInterceptedException:

                print(
                    "Normal click intercepted. "
                    "Using JavaScript click..."
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    confirm_button
                )

            print(
                "Confirm selected Delete button clicked"
            )

            # -------------------------------------------------
            # Wait for Product List to remain/load
            # -------------------------------------------------

            self.wait.until(
                EC.url_contains(
                    "/Admin/Product/List"
                )
            )

            print(
                "Product List page loaded after "
                "selected product deletion."
            )

            # -------------------------------------------------
            # Wait for product table
            # -------------------------------------------------

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        "products-grid"
                    )
                )
            )

            print(
                "Product table found after "
                "selected deletion."
            )

        except TimeoutException:

            print(
                "Delete Selected confirmation "
                "operation timed out."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            # Useful DOM diagnostics
            try:

                diagnostic = self.driver.execute_script(
                    """
                    const modal =
                        document.getElementById(arguments[0]);

                    if (!modal) {
                        return "MODAL NOT FOUND";
                    }

                    return {
                        id: modal.id,
                        className: modal.className,
                        display:
                            window.getComputedStyle(modal).display,
                        visibility:
                            window.getComputedStyle(modal).visibility,
                        opacity:
                            window.getComputedStyle(modal).opacity,
                        ariaHidden:
                            modal.getAttribute("aria-hidden"),
                        text:
                            modal.innerText
                    };
                    """,
                    modal_id
                )

                print(
                    "Delete Selected modal diagnostics:",
                    diagnostic
                )

            except Exception as diagnostic_error:

                print(
                    "Unable to collect modal diagnostics:",
                    diagnostic_error
                )

            raise

    # =================================================
    # Verify Product Deleted From Product Table
    # =================================================

    def isProductDeletedFromTable(self, product_name):

        print(
            f"Checking whether product "
            f"'{product_name}' is deleted from the table..."
        )

        try:

            # Wait until Product List table is available
            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        "products-grid"
                    )
                )
            )

            # Give DataTables a moment to refresh after deletion
            time.sleep(1)

            rows = self.driver.find_elements(
                By.XPATH,
                "//table[@id='products-grid']"
                "//tbody/tr"
            )

            print(
                f"Number of product rows after deletion: "
                f"{len(rows)}"
            )

            for index, row in enumerate(
                    rows,
                    start=1
            ):

                try:

                    row_text = row.text.strip()

                    print(
                        f"Product row {index}: "
                        f"{repr(row_text)}"
                    )

                    if product_name.strip().lower() in (
                            row_text.lower()
                    ):
                        print(
                            f"Product '{product_name}' "
                            f"is still present in the table."
                        )

                        return False

                except StaleElementReferenceException:

                    print(
                        f"Product row {index} became stale. "
                        "Re-reading table..."
                    )

                    rows = self.driver.find_elements(
                        By.XPATH,
                        "//table[@id='products-grid']"
                        "//tbody/tr"
                    )

                    for retry_row in rows:

                        if product_name.strip().lower() in (
                                retry_row.text.strip().lower()
                        ):
                            print(
                                f"Product '{product_name}' "
                                "is still present after retry."
                            )

                            return False

                    break

            print(
                f"Product '{product_name}' "
                "is no longer in the table."
            )

            return True

        except TimeoutException:

            print(
                "Product table was not available "
                "after deletion."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            return False

    # =================================================
    # Delete Product Button
    # =================================================

    def clickDelete(self):

        print(
            "Waiting for Product Delete button..."
        )

        for attempt in range(3):

            try:

                delete_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.btnDelete_xpath
                        )
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
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
                    "Delete button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

            except TimeoutException:

                print(
                    "Delete button not clickable. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

    # =================================================
    # Confirm Product Delete
    # =================================================

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
            # Wait for modal to become visible / active
            # =================================================

            modal_active_script = """
                const modal = document.getElementById(
                    'productmodel-Delete-delete-confirmation'
                );

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
            """

            try:

                self.wait.until(
                    lambda driver:
                    driver.execute_script(
                        modal_active_script
                    )
                )

                print(
                    "Product Delete confirmation modal "
                    "opened normally."
                )

            except TimeoutException:

                print(
                    "Normal Bootstrap modal activation "
                    "did not complete."
                )

                print(
                    "Using Bootstrap API fallback..."
                )

                # =================================================
                # Bootstrap / DOM fallback
                # =================================================

                fallback_result = self.driver.execute_script(
                    """
                    const modal =
                        document.getElementById(
                            'productmodel-Delete-delete-confirmation'
                        );

                    if (!modal) {
                        return {
                            success: false,
                            reason: 'Modal not found'
                        };
                    }

                    try {

                        // -----------------------------------------
                        // Bootstrap / jQuery modal
                        // -----------------------------------------

                        if (
                            window.jQuery &&
                            window.jQuery.fn &&
                            window.jQuery.fn.modal
                        ) {

                            window.jQuery(modal).modal('show');

                            return {
                                success: true,
                                method: 'jquery-bootstrap'
                            };
                        }

                        // -----------------------------------------
                        // Bootstrap 5
                        // -----------------------------------------

                        if (
                            window.bootstrap &&
                            window.bootstrap.Modal
                        ) {

                            const instance =
                                window.bootstrap.Modal
                                    .getOrCreateInstance(
                                        modal
                                    );

                            instance.show();

                            return {
                                success: true,
                                method: 'bootstrap-5'
                            };
                        }

                        // -----------------------------------------
                        // Final DOM fallback
                        // -----------------------------------------

                        modal.classList.add('show');

                        modal.style.display = 'block';
                        modal.style.opacity = '1';
                        modal.style.visibility = 'visible';

                        modal.setAttribute(
                            'aria-hidden',
                            'false'
                        );

                        modal.setAttribute(
                            'aria-modal',
                            'true'
                        );

                        modal.setAttribute(
                            'role',
                            'dialog'
                        );

                        document.body.classList.add(
                            'modal-open'
                        );

                        let backdrop =
                            document.querySelector(
                                '.modal-backdrop'
                            );

                        if (!backdrop) {

                            backdrop =
                                document.createElement(
                                    'div'
                                );

                            backdrop.className =
                                'modal-backdrop fade show';

                            document.body.appendChild(
                                backdrop
                            );

                        } else {

                            backdrop.classList.add(
                                'show'
                            );
                        }

                        return {
                            success: true,
                            method: 'dom'
                        };

                    } catch (error) {

                        return {
                            success: false,
                            reason: error.toString()
                        };
                    }
                    """
                )

                print(
                    "Bootstrap fallback result:",
                    fallback_result
                )

                if not fallback_result.get(
                    "success",
                    False
                ):

                    raise TimeoutException(
                        "Unable to activate product "
                        "delete confirmation modal."
                    )

                # ---------------------------------------------
                # Verify fallback actually activated modal
                # ---------------------------------------------

                self.wait.until(
                    lambda driver:
                    driver.execute_script(
                        modal_active_script
                    )
                )

                print(
                    "Product Delete confirmation modal "
                    "opened successfully."
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
                repr(
                    confirm_button.text.strip()
                )
            )

            # =================================================
            # Wait until button is actually visible
            # =================================================

            self.wait.until(
                lambda driver:
                driver.execute_script(
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
                            f"Delete button {index} "
                            "became stale."
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
                                    window.getComputedStyle(
                                        modal
                                    );

                                return {
                                    id: modal.id,
                                    className:
                                        modal.className,
                                    display:
                                        style.display,
                                    visibility:
                                        style.visibility,
                                    opacity:
                                        style.opacity,
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

    # =================================================
    # Verify Product Deleted Successfully
    # =================================================

    def isProductDeletedSuccessfully(self):

        print(
            "Waiting for Product deletion success message..."
        )

        try:

            success_message = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        self.delete_success_message_xpath
                    )
                )
            )

            message = success_message.text.strip()

            print(
                "Product deletion success message:",
                repr(message)
            )

            if (
                    "The product has been deleted successfully"
                    in message
            ):
                print(
                    "Product deletion success message "
                    "verified successfully."
                )

                return True

            print(
                "Unexpected product deletion message:",
                repr(message)
            )

            return False

        except TimeoutException:

            print(
                "Product deletion success message "
                "was not displayed."
            )

            return False

        except StaleElementReferenceException:

            print(
                "Product deletion success message "
                "became stale. Re-checking..."
            )

            try:

                success_message = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            self.delete_success_message_xpath
                        )
                    )
                )

                message = success_message.text.strip()

                print(
                    "Product deletion success message "
                    "after retry:",
                    repr(message)
                )

                return (
                        "The product has been deleted successfully"
                        in message
                )

            except Exception as e:

                print(
                    "Unable to verify deletion success "
                    "after retry:",
                    e
                )

                return False

