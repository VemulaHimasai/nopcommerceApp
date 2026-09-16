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

    # Delete confirmation modal
    delete_confirmation_form_xpath = (
        "//form[contains(@action,'/Admin/Customer/Delete/')]"
    )

    # Delete button inside confirmation modal
    btnConfirmDelete_xpath = (
        "//form[contains(@action,'/Admin/Customer/Delete/')]"
        "//button[@type='submit' "
        "and contains(@class,'btn-danger') "
        "and normalize-space()='Delete']"
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

            message = success_message.text.strip()

            print(
                "Success message:",
                repr(message)
            )

            if (
                "The customer has been updated successfully"
                in message
            ):

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

                self.driver.save_screenshot(
                    ".\\Screenshots\\edit_customer_failure.png"
                )

                print(
                    "Failure screenshot saved:"
                    " .\\Screenshots\\edit_customer_failure.png"
                )

            except Exception as e:

                print(
                    "Unable to save failure screenshot:",
                    e
                )

            return False

        except StaleElementReferenceException:

            print(
                "Success message became stale. "
                "Retrying verification..."
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
                    "Success message after retry:",
                    repr(message)
                )

                return (
                    "The customer has been updated successfully"
                    in message
                )

            except Exception as e:

                print(
                    "Unable to verify success message "
                    "after retry:",
                    e
                )

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

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.delete_confirmation_form_xpath
                )
            )
        )

        print(
            "Delete confirmation modal is visible."
        )

        confirm_delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnConfirmDelete_xpath
                )
            )
        )

        print(
            "Confirmation delete button:",
            confirm_delete_button.text
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
            confirm_delete_button
        )

        # -------------------------------------------------
        # Re-locate after scrolling
        # -------------------------------------------------

        confirm_delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnConfirmDelete_xpath
                )
            )
        )

        confirm_delete_button.click()

        print(
            "Delete confirmation submitted."
        )

        # -------------------------------------------------
        # Wait for modal to disappear
        # -------------------------------------------------

        try:

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        self.delete_confirmation_form_xpath
                    )
                )
            )

            print(
                "Customer delete confirmed."
            )

        except TimeoutException:

            print(
                "Delete confirmation modal did not "
                "disappear within the expected time."
            )