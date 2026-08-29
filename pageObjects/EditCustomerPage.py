import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#edit customer
class EditCustomerPage:
    txtFirstName_id = "FirstName"
    btnSave_xpath = "//button[@name='save']"

    btnDelete_xpath = "//span[@id='customer-delete']"

    btnConfirmDelete_xpath = "//button[normalize-space()='Delete']"

    def __init__(self, driver):
        self.driver = driver

    def clearFirstName(self):
        self.driver.find_element(By.ID, self.txtFirstName_id).clear()

    def setFirstName(self, firstName):
        first_name = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.txtFirstName_id))
        )
        first_name.clear()
        first_name.send_keys(firstName)

    def clickSave(self):
        self.driver.find_element(By.XPATH,self.btnSave_xpath).click()

    def clickDelete(self):
       delete_button = WebDriverWait(self.driver, 10).until(
           EC.element_to_be_clickable(
               (By.XPATH, self.btnDelete_xpath)
           )
       )
       delete_button.click()

    def confirmDelete(self):
        confirm_delete_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnConfirmDelete_xpath)
            )
        )
        confirm_delete_button.click()

