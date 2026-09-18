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

        print(
            "Waiting for First Name field..."
        )

        for attempt in range(1, 4):

            try:

                first_name = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.txtFirstName_id
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
                    first_name
                )

                first_name = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            self.txtFirstName_id
                        )
                    )
                )

                first_name.click()
                first_name.clear()

                actual_value = (
                    self.driver.find_element(
                        By.ID,
                        self.txtFirstName_id
                    ).get_attribute("value") or ""
                ).strip()

                if actual_value == "":

                    print(
                        "First Name field cleared successfully."
                    )

                    return

                print(
                    "First Name field was not cleared."
                )

            except StaleElementReferenceException:

                print(
                    f"First Name field became stale. "
                    f"Retrying ({attempt}/3)..."
                )

                if attempt < 3:
                    time.sleep(0.5)

            except TimeoutException:

                print(
                    f"First Name field timeout. "
                    f"Attempt {attempt}/3"
                )

                if attempt < 3:
                    time.sleep(0.5)

                else:
                    raise

        raise AssertionError(
            "Unable to clear First Name field."
        )

    # =================================================
    # Set First Name
    # =================================================

    def setFirstName(self, firstName):

        firstName = str(firstName).strip()

        if not firstName:

            raise ValueError(
                "First name cannot be empty."
            )

        for attempt in range(1, 4):

            try:

                print(
                    f"Setting First Name: {firstName} "
                    f"(attempt {attempt}/3)"
                )

                # -------------------------------------------------
                # Locate First Name field
                # -------------------------------------------------

                first_name = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.txtFirstName_id
                        )
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
                        (
                            By.ID,
                            self.txtFirstName_id
                        )
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
                    f"Retrying ({attempt}/3)..."
                )

                if attempt < 3:
                    time.sleep(0.5)

                    continue

                raise

            except TimeoutException:

                print(
                    f"First Name value verification timed out. "
                    f"Attempt {attempt}/3"
                )

                try:

                    current_value = (
                        self.driver.find_element(
                            By.ID,
                            self.txtFirstName_id
                        ).get_attribute("value") or ""
                    ).strip()

                    print(
                        "Current First Name field value:",
                        repr(current_value)
                    )

                except Exception as e:

                    print(
                        "Unable to read First Name field:",
                        e
                    )

                if attempt < 3:

                    time.sleep(0.5)

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

        for attempt in range(1, 4):

            try:

                save_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.btnSave_xpath
                        )
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
                        (
                            By.XPATH,
                            self.btnSave_xpath
                        )
                    )
                )

                print(
                    "Clicking Save..."
                )

                try:

                    save_button.click()

                except StaleElementReferenceException:

                    print(
                        "Save button became stale. "
                        "Re-locating..."
                    )

                    save_button = self.wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                self.btnSave_xpath
                            )
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        save_button
                    )

                print(
                    "Save button clicked."
                )

                break

            except StaleElementReferenceException:

                print(
                    f"Save button became stale. "
                    f"Retrying ({attempt}/3)..."
                )

                if attempt < 3:
                    time.sleep(0.5)

            except TimeoutException:

                print(
                    f"Save button timeout. "
                    f"Attempt {attempt}/3"
                )

                if attempt < 3:
                    time.sleep(0.5)

                else:
                    raise

        # =================================================
        # WAIT FOR AJAX PROCESSING
        # =================================================

        try:

            ajax_busy_xpath = "//*[@id='ajaxBusy']"

            ajax_busy_elements = self.driver.find_elements(
                By.XPATH,
                ajax_busy_xpath
            )

            if ajax_busy_elements:

                try:

                    if ajax_busy_elements[0].is_displayed():

                        print(
                            "AJAX processing detected. "
                            "Waiting for completion..."
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

                    else:

                        print(
                            "AJAX busy indicator is already hidden."
                        )

                except StaleElementReferenceException:

                    print(
                        "AJAX busy element became stale. "
                        "Continuing..."
                    )

            else:

                print(
                    "AJAX busy indicator not present."
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

        # =================================================
        # WAIT FOR CUSTOMER LIST REDIRECT
        # =================================================

        print(
            "Waiting for Customer List redirect..."
        )

        try:

            self.wait.until(
                EC.url_contains(
                    "/Admin/Customer/List"
                )
            )

            print(
                "Customer List redirect detected."
            )

            print(
                "Current URL after Save:",
                self.driver.current_url
            )

            print(
                "Current Title after Save:",
                self.driver.title
            )

        except TimeoutException:

            print(
                "Customer List redirect was not detected "
                "after Save."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Current Title:",
                self.driver.title
            )

            raise

    # =================================================
    # Verify Customer Updated Successfully
    # =================================================

    def isCustomerUpdatedSuccessfully(self):

        expected_message = (
            "The customer has been updated successfully"
        )

        print(
            "Waiting for customer update success message..."
        )

        for attempt in range(1, 4):

            try:

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
                        "Re-locating..."
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

                if attempt < 3:
                    time.sleep(0.5)

            except StaleElementReferenceException:

                print(
                    f"Success message became stale. "
                    f"Attempt {attempt}/3"
                )

                if attempt < 3:
                    time.sleep(0.5)

            except TimeoutException:

                print(
                    f"Customer update success message "
                    f"was not found. Attempt {attempt}/3"
                )

                if attempt < 3:

                    time.sleep(0.5)

                    continue

                break

        # =================================================
        # FAILURE DIAGNOSTICS
        # =================================================

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

                if attempt < 3:
                    time.sleep(0.5)

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

                    time.sleep(0.5)

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

        delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnDelete_xpath
                )
            )
        )

        print(
            "Clicking Delete..."
        )

        try:

            delete_button.click()

        except StaleElementReferenceException:

            print(
                "Delete button became stale. "
                "Re-locating..."
            )

            delete_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.btnDelete_xpath
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                delete_button
            )

        print(
            "Delete button clicked."
        )

        # =================================================
        # Wait briefly for normal Bootstrap activation
        # =================================================

        modal_xpath = (
            "//div[@id='customermodel-Delete-delete-confirmation' "
            "and @role='dialog']"
        )

        try:

            self.wait.until(
                lambda driver: driver.execute_script(
                    """
                    const modal = document.getElementById(
                        'customermodel-Delete-delete-confirmation'
                    );

                    if (!modal) {
                        return false;
                    }

                    const style =
                        window.getComputedStyle(modal);

                    return (
                        modal.classList.contains('show') &&
                        style.display !== 'none' &&
                        parseFloat(style.opacity) > 0
                    );
                    """
                )
            )

            print(
                "Delete confirmation modal opened normally."
            )

            return

        except TimeoutException:

            print(
                "Normal Bootstrap modal activation did not "
                "complete. Using Bootstrap API fallback..."
            )

        # =================================================
        # Bootstrap API fallback
        # =================================================

        bootstrap_result = self.driver.execute_script(
            """
            const modalId =
                '#customermodel-Delete-delete-confirmation';

            if (
                typeof window.jQuery === 'undefined' ||
                typeof jQuery.fn.modal !== 'function'
            ) {
                return {
                    success: false,
                    reason: 'jQuery/Bootstrap modal API unavailable'
                };
            }

            jQuery(modalId).modal('show');

            return {
                success: true
            };
            """
        )

        print(
            "Bootstrap fallback result:",
            bootstrap_result
        )

        # =================================================
        # Verify modal is active
        # =================================================

        self.wait.until(
            lambda driver: driver.execute_script(
                """
                const modal = document.getElementById(
                    'customermodel-Delete-delete-confirmation'
                );

                if (!modal) {
                    return false;
                }

                const style =
                    window.getComputedStyle(modal);

                return (
                    modal.classList.contains('show') &&
                    style.display !== 'none' &&
                    parseFloat(style.opacity) > 0
                );
                """
            )
        )

        print(
            "Delete confirmation modal opened successfully."
        )
    # =================================================
    # Confirm Delete
    # =================================================


    def confirmDelete(self):
        print(
            "Waiting for delete confirmation modal..."
        )

        # =================================================
        # Modal locator
        # =================================================

        modal_xpath = self.delete_confirmation_modal_xpath

        # =================================================
        # Wait for modal to exist in DOM
        # =================================================

        modal = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    modal_xpath
                )
            )
        )

        print(
            "Delete confirmation modal found in DOM."
        )

        # =================================================
        # Wait for Bootstrap modal to become active
        #
        # Bootstrap normally changes:
        #
        # class="modal fade"
        #
        # to:
        #
        # class="modal fade show"
        #
        # and display becomes block.
        # =================================================

        try:

            self.wait.until(
                lambda driver: driver.execute_script(
                    """
                    const modal = arguments[0];
    
                    if (!modal) {
                        return false;
                    }
    
                    const style =
                        window.getComputedStyle(modal);
    
                    return (
                        modal.classList.contains('show') &&
                        style.display !== 'none' &&
                        style.opacity !== '0'
                    );
                    """,
                    driver.find_element(
                        By.XPATH,
                        modal_xpath
                    )
                )
            )

        except TimeoutException:

            print(
                "Delete confirmation modal did not become "
                "active within the expected time."
            )

            # =================================================
            # Debug final modal state
            # =================================================

            try:

                modal = self.driver.find_element(
                    By.XPATH,
                    modal_xpath
                )

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
                        opacity: style.opacity,
                        ariaHidden: modal.getAttribute('aria-hidden')
                    };
                    """,
                    modal
                )

                print(
                    "Final delete modal state:",
                    modal_state
                )

            except Exception as e:

                print(
                    "Unable to inspect delete modal state:",
                    str(e)
                )

            raise

        print(
            "Delete confirmation modal is active."
        )

        # =================================================
        # Re-locate modal
        # =================================================

        modal = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    modal_xpath
                )
            )
        )

        # =================================================
        # Verify confirmation message
        # =================================================

        modal_message_xpath = (
                modal_xpath
                + "//div[contains(@class,'modal-body')]"
        )

        modal_message = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    modal_message_xpath
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
        # Wait until confirmation button is displayed
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
    
                return (
                    style.display !== 'none' &&
                    style.visibility !== 'hidden' &&
                    button.offsetWidth > 0 &&
                    button.offsetHeight > 0
                );
                """,
                driver.find_element(
                    By.XPATH,
                    self.btnConfirmDelete_xpath
                )
            )
        )

        # =================================================
        # Scroll confirmation button into view
        # =================================================

        confirm_delete_button = self.driver.find_element(
            By.XPATH,
            self.btnConfirmDelete_xpath
        )

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
        # Click confirmation Delete
        # =================================================

        print(
            "Clicking confirmation Delete button..."
        )

        try:

            self.driver.execute_script(
                "arguments[0].click();",
                confirm_delete_button
            )

        except StaleElementReferenceException:

            print(
                "Confirmation Delete button became stale. "
                "Re-locating..."
            )

            confirm_delete_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.btnConfirmDelete_xpath
                    )
                )
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

            self.wait.until(
                EC.url_contains(
                    "/Admin/Customer/List"
                )
            )

            print(
                "Customer List page opened after delete."
            )

            print(
                "Current URL after delete:",
                self.driver.current_url
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