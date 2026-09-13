
import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# edit customer
class EditCustomerPage:

    txtFirstName_id = "FirstName"

    btnSave_xpath = "//button[@name='save']"

    success_message_xpath = (
        "//div[contains(@class,'alert-success') "
        "and contains(normalize-space(.),"
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
        "//button[@type='submit' and "
        "contains(@class,'btn-danger') and "
        "normalize-space()='Delete']"
    )

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            self.driver,
            15
        )

    # -------------------------------------------------
    # Clear First Name
    # -------------------------------------------------

    def clearFirstName(self):

        first_name = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.txtFirstName_id)
            )
        )

        first_name.clear()

    # -------------------------------------------------
    # Set First Name
    # -------------------------------------------------

    def setFirstName(self, firstName):

        firstName = str(firstName).strip()

        for attempt in range(3):

            try:
                print(
                    f"Setting First Name: {firstName} "
                    f"(attempt {attempt + 1}/3)"
                )

                # -------------------------------------------------
                # Locate field
                # -------------------------------------------------
                first_name = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, self.txtFirstName_id)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
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
                # Enter First Name
                # -------------------------------------------------
                first_name.send_keys(firstName)

                # -------------------------------------------------
                # Verify value by RE-LOCATING the element
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
                # Get actual value
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

                # Debug current value
                try:

                    current_value = self.driver.find_element(
                        By.ID,
                        self.txtFirstName_id
                    ).get_attribute("value")

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

    # -------------------------------------------------
    # Click Save
    # -------------------------------------------------

    def clickSave(self):

        save_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnSave_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            save_button
        )

        save_button.click()

    def isCustomerUpdatedSuccessfully(self):

        try:
            success_message = WebDriverWait(
                self.driver,
                20
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class,'alert-success') "
                        "and contains(normalize-space(.), "
                        "'The customer has been updated successfully')]"
                    )
                )
            )

            print(
                "Success message:",
                repr(success_message.text)
            )

            return True

        except Exception as e:

            print(
                "Success message was not found."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Page title:",
                self.driver.title
            )

            self.driver.save_screenshot(
                ".\\Screenshots\\edit_customer_failure.png"
            )

            return False

    # -------------------------------------------------
    # Verify Customer Updated
    # -------------------------------------------------


    def isCustomerUpdatedSuccessfully(self):

        try:

            # Wait for AJAX processing to finish
            try:
                self.wait.until(
                    EC.invisibility_of_element_located(
                        (By.ID, "ajaxBusy")
                    )
                )
            except:
                pass

            # Wait for success message
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

            return (
                    "The customer has been updated successfully"
                    in message
            )

        except Exception as e:

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

            print(
                "Body text after Save:"
            )

            print(
                self.driver.find_element(
                    By.TAG_NAME,
                    "body"
                ).text
            )

            self.driver.save_screenshot(
                ".\\Screenshots\\edit_customer_failure.png"
            )

            return False



    # -------------------------------------------------
    # Click Delete
    # -------------------------------------------------

    def clickDelete(self):

        delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnDelete_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            delete_button
        )

        delete_button.click()

    # -------------------------------------------------
    # Confirm Delete
    # -------------------------------------------------

    def confirmDelete(self):

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.delete_confirmation_form_xpath)
            )
        )

        print(
            "Delete confirmation modal is visible"
        )

        confirm_delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnConfirmDelete_xpath)
            )
        )

        print(
            "Confirmation delete button:",
            confirm_delete_button.text
        )

        confirm_delete_button.click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, self.delete_confirmation_form_xpath)
            )
        )

        print(
            "Customer delete confirmed"
        )

