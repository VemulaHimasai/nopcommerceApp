import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================================================
# Edit Customer Page
# =========================================================

class EditCustomerPage:

    # -------------------------------------------------
    # Locators
    # -------------------------------------------------

    txtFirstName_id = "FirstName"

    btnSave_xpath = "//button[@name='save']"

    success_message_xpath = (
        "//div[contains(@class,'alert-success') "
        "and contains(normalize-space(.), "
        "'The customer has been updated successfully')]"
    )

    btnDelete_xpath = "//span[@id='customer-delete']"

    delete_confirmation_modal_xpath = (
        "//div[@id='customermodel-Delete-delete-confirmation' "
        "and @role='dialog']"
    )

    btnConfirmDelete_xpath = (
        "//div[@id='customermodel-Delete-delete-confirmation']"
        "//button[@type='submit' "
        "and contains(@class,'btn-danger') "
        "and normalize-space()='Delete']"
    )

    # Back to customer list
    btnBackToCustomerList_xpath = (
        "//a[normalize-space()='back to customer list']"
    )

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            self.driver,
            20
        )

    # =================================================
    # Clear First Name
    # =================================================

    def clearFirstName(self):

        first_name = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.txtFirstName_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            first_name
        )

        first_name.clear()

    # =================================================
    # Set First Name
    # =================================================

    def setFirstName(self, firstName):

        firstName = str(firstName).strip()

        if not firstName:

            raise ValueError(
                "First name cannot be empty."
            )

        for attempt in range(3):

            try:

                print(
                    f"Setting First Name: {firstName} "
                    f"(attempt {attempt + 1}/3)"
                )

                # -------------------------------------------------
                # Locate First Name field
                # -------------------------------------------------

                first_name = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, self.txtFirstName_id)
                    )
                )

                # -------------------------------------------------
                # Scroll into view
                # -------------------------------------------------

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    first_name
                )

                # -------------------------------------------------
                # Re-locate after scrolling
                # -------------------------------------------------

                first_name = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, self.txtFirstName_id)
                    )
                )

                # -------------------------------------------------
                # Click and clear
                # -------------------------------------------------

                first_name.click()
                first_name.clear()

                # -------------------------------------------------
                # Enter value
                # -------------------------------------------------

                first_name.send_keys(firstName)

                # -------------------------------------------------
                # Verify entered value
                # -------------------------------------------------

                self.wait.until(
                    lambda driver: (
                        driver.find_element(
                            By.ID,
                            self.txtFirstName_id
                        ).get_attribute("value") or ""
                    ).strip() == firstName
                )

                # -------------------------------------------------
                # Read actual value
                # -------------------------------------------------

                actual_value = (
                    self.driver.find_element(
                        By.ID,
                        self.txtFirstName_id
                    ).get_attribute("value") or ""
                ).strip()

                print(
                    "Expected First Name:",
                    repr(firstName)
                )

                print(
                    "Actual First Name  :",
                    repr(actual_value)
                )

                # -------------------------------------------------
                # Final verification
                # -------------------------------------------------

                if actual_value == firstName:

                    print(
                        "First Name entered successfully"
                    )

                    return

            except StaleElementReferenceException:

                print(
                    f"First Name field became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt < 2:

                    time.sleep(1)

                    continue

                raise

            except TimeoutException:

                print(
                    f"First Name value verification timed out. "
                    f"Attempt {attempt + 1}/3"
                )

                try:

                    current_value = (
                        self.driver.find_element(
                            By.ID,
                            self.txtFirstName_id
                        ).get_attribute("value")
                    )

                    print(
                        "Current First Name field value:",
                        repr(current_value)
                    )

                except Exception as e:

                    print(
                        "Unable to read First Name field:",
                        e
                    )

                if attempt < 2:

                    time.sleep(1)

                    continue

                raise

        raise AssertionError(
            f"Unable to enter first name: {firstName}"
        )

    # =================================================
    # Click Save
    # =================================================

    def clickSave(self):

        print(
            "Waiting for Save button..."
        )

        save_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnSave_xpath)
            )
        )

        # -------------------------------------------------
        # Scroll Save button into view
        # -------------------------------------------------

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            save_button
        )

        # -------------------------------------------------
        # Re-locate after scrolling
        # -------------------------------------------------

        save_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnSave_xpath)
            )
        )

        print(
            "Clicking Save..."
        )

        save_button.click()

        print(
            "Save button clicked."
        )

        # =================================================
        # WAIT FOR AJAX PROCESSING
        # =================================================

        try:

            ajax_busy_xpath = (
                "//*[@id='ajaxBusy']"
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        ajax_busy_xpath
                    )
                )
            )

            print(
                "AJAX processing completed."
            )

        except TimeoutException:

            print(
                "ajaxBusy did not disappear within "
                "the expected time."
            )

        except Exception as e:

            print(
                "Unable to check ajaxBusy:",
                e
            )

        # -------------------------------------------------
        # Allow notification rendering
        # -------------------------------------------------

        time.sleep(0.5)

    # =================================================
    # Verify Customer Updated Successfully
    # =================================================

    def isCustomerUpdatedSuccessfully(self):

        expected_message = (
            "The customer has been updated successfully"
        )

        try:

            print(
                "Waiting for customer update success message..."
            )

            success_message = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        self.success_message_xpath
                    )
                )
            )

            try:

                message = success_message.text.strip()

            except StaleElementReferenceException:

                print(
                    "Success message became stale. "
                    "Retrying verification..."
                )

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
                "Success message:",
                repr(message)
            )

            if expected_message in message:
                print(
                    "Customer update verified successfully."
                )

                return True

            print(
                "Unexpected success message:",
                repr(message)
            )

            return False

        except TimeoutException:

            print(
                "Customer update success message "
                "was not found."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Page title:",
                self.driver.title
            )

            # -------------------------------------------------
            # Print current First Name
            # -------------------------------------------------

            try:

                current_first_name = (
                        self.driver.find_element(
                            By.ID,
                            self.txtFirstName_id
                        ).get_attribute("value") or ""
                ).strip()

                print(
                    "Current First Name after Save:",
                    repr(current_first_name)
                )

            except Exception as e:

                print(
                    "Unable to read First Name after Save:",
                    e
                )

            # -------------------------------------------------
            # Print body text
            # -------------------------------------------------

            try:

                print(
                    "Body text after Save:"
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

            # -------------------------------------------------
            # Save screenshot
            # -------------------------------------------------

            try:

                screenshot_path = (
                    ".\\Screenshots\\edit_customer_failure.png"
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

        except StaleElementReferenceException:

            print(
                "Success message became stale "
                "during verification."
            )

            return False

    # =================================================
    # Back to Customer List
    # =================================================

    def clickBackToCustomerList(self):

        print(
            "Waiting for Back to Customer List link..."
        )

        for attempt in range(1, 4):

            try:

                # -------------------------------------------------
                # Locate link
                # -------------------------------------------------

                back_button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.btnBackToCustomerList_xpath
                        )
                    )
                )

                print(
                    "Back to Customer List link found."
                )

                # -------------------------------------------------
                # Scroll into view
                # -------------------------------------------------

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    back_button
                )

                # -------------------------------------------------
                # Re-locate after scrolling
                # -------------------------------------------------

                back_button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.btnBackToCustomerList_xpath
                        )
                    )
                )

                print(
                    "Back to Customer List link is present."
                )

                # -------------------------------------------------
                # Click using JavaScript
                # -------------------------------------------------

                self.driver.execute_script(
                    "arguments[0].click();",
                    back_button
                )

                print(
                    "Back to Customer List clicked."
                )

                # -------------------------------------------------
                # Wait for Customer List URL
                # -------------------------------------------------

                self.wait.until(
                    EC.url_contains(
                        "/Admin/Customer/List"
                    )
                )

                print(
                    "Customer List page opened successfully."
                )

                return True

            except StaleElementReferenceException:

                print(
                    f"Back link became stale. "
                    f"Retrying ({attempt}/3)..."
                )

                time.sleep(1)

            except TimeoutException:

                print(
                    f"Back link timeout. Attempt {attempt}/3"
                )

                # -------------------------------------------------
                # Diagnostic information
                # -------------------------------------------------

                try:

                    print(
                        "Current URL:",
                        self.driver.current_url
                    )

                    print(
                        "Page title:",
                        self.driver.title
                    )

                    count = self.driver.execute_script(
                        """
                        return document.evaluate(
                            arguments[0],
                            document,
                            null,
                            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
                            null
                        ).snapshotLength;
                        """,
                        self.btnBackToCustomerList_xpath
                    )

                    print(
                        "Back link XPath match count:",
                        count
                    )

                except Exception as e:

                    print(
                        "Unable to collect diagnostics:",
                        e
                    )

                if attempt < 3:

                    time.sleep(1)

                    continue

                raise

        return False


    # =================================================
    # Click Delete
    # =================================================

    def clickDelete(self):

        print(
            "Waiting for Delete button..."
        )

        delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnDelete_xpath)
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

        delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnDelete_xpath)
            )
        )

        print(
            "Clicking Delete..."
        )

        delete_button.click()

        print(
            "Delete button clicked."
        )

    # =================================================
    # Confirm Delete
    # =================================================

    def confirmDelete(self):

        print(
            "Waiting for delete confirmation modal..."
        )

        # =================================================
        # Wait only for modal presence in DOM
        # =================================================

        modal = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.delete_confirmation_modal_xpath
                )
            )
        )

        print(
            "Delete confirmation modal found in DOM."
        )

        # =================================================
        # Debug modal state
        # =================================================

        modal_state = self.driver.execute_script(
            """
            const modal = arguments[0];

            const style =
                window.getComputedStyle(modal);

            return {
                id: modal.id,
                className: modal.className,
                display: style.display,
                visibility: style.visibility,
                opacity: style.opacity
            };
            """,
            modal
        )

        print(
            "Delete modal state:",
            modal_state
        )

        # =================================================
        # Verify confirmation message
        # =================================================

        modal_message = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.delete_confirmation_modal_xpath
                    + "//div[contains(@class,'modal-body')]"
                )
            )
        )

        print(
            "Delete confirmation message:",
            repr(
                modal_message.text.strip()
            )
        )

        # =================================================
        # Find confirmation Delete button
        # =================================================

        confirm_delete_button = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.btnConfirmDelete_xpath
                )
            )
        )

        print(
            "Confirmation Delete button found."
        )

        print(
            "Confirmation button text:",
            repr(
                confirm_delete_button.text.strip()
            )
        )

        # =================================================
        # Scroll to confirmation button
        # =================================================

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            confirm_delete_button
        )

        # =================================================
        # Re-locate button after scrolling
        # =================================================

        confirm_delete_button = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.btnConfirmDelete_xpath
                )
            )
        )

        # =================================================
        # Click Delete using JavaScript
        # =================================================

        print(
            "Clicking confirmation Delete button..."
        )

        self.driver.execute_script(
            "arguments[0].click();",
            confirm_delete_button
        )

        print(
            "Delete confirmation submitted."
        )

        # =================================================
        # Wait for Customer List redirect
        # =================================================

        try:

            WebDriverWait(
                self.driver,
                15
            ).until(
                EC.url_contains(
                    "/Admin/Customer/List"
                )
            )

            print(
                "Customer List page opened after delete."
            )

        except TimeoutException:

            print(
                "Customer List redirect did not occur."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            raise


