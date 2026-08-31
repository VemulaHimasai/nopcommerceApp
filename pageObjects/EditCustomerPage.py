import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# edit customer
class EditCustomerPage:

    txtFirstName_id = "FirstName"

    btnSave_xpath = "//button[@name='save']"

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
        self.wait = WebDriverWait(self.driver, 15)

    def clearFirstName(self):
        self.driver.find_element(
            By.ID,
            self.txtFirstName_id
        ).clear()

    def setFirstName(self, firstName):

        first_name = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.txtFirstName_id)
            )
        )

        first_name.clear()
        first_name.send_keys(firstName)

    def clickSave(self):

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnSave_xpath)
            )
        ).click()

    def clickDelete(self):

        delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnDelete_xpath)
            )
        )

        delete_button.click()

    def confirmDelete(self):

        # Wait for delete confirmation form/modal
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.delete_confirmation_form_xpath)
            )
        )

        print("Delete confirmation modal is visible")

        # Wait for Confirm Delete button
        confirm_delete_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnConfirmDelete_xpath)
            )
        )

        print(
            "Confirmation delete button:",
            confirm_delete_button.text
        )

        # Click Confirm Delete
        confirm_delete_button.click()

        # Wait until confirmation form/modal disappears
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, self.delete_confirmation_form_xpath)
            )
        )

        print("Customer delete confirmed")