from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ActivityTypePage:
    lnkactivity_type_menu_item_xpath = "//a[@href='/Admin/ActivityLog/ActivityTypes']"
    activity_types_table_xpath = "//table[@id='activityLogType-grid']"
    btn_save_xpath = "//button[normalize-space()='Save']"
    success_message_xpath = (
        "//*[contains(normalize-space(), "
        "'The types have been updated successfully')]"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def clickActivityTypeMenuItem(self):
        activity_type_menu_item = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.lnkactivity_type_menu_item_xpath)
        ))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", activity_type_menu_item)
        self.driver.execute_script("arguments[0].click()", activity_type_menu_item)

    def isActivityTypePresent(self,activity_type):
        try:
            activity = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,f"{self.activity_types_table_xpath}"
                        f"//td[normalize-space()='{activity_type}']")
            ))
            return activity.is_displayed()
        except TimeoutException:
            return False

    def clickSave(self):
        save_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btn_save_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", save_button)
        self.driver.execute_script("arguments[0].click()", save_button)

    def isUpdateSuccessmessageDisplayed(self):
        try:
            success_message = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,self.success_message_xpath)
            ))
            return success_message.is_displayed()
        except TimeoutException:
            return False




