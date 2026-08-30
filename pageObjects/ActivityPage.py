from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class ActivityPage:

    lnkActivityLog_menu_item_xpath = "//a[@href='/Admin/ActivityLog/ActivityLogs']"

    created_from_xpath = "//input[@id='CreatedOnFrom']"
    created_to_xpath = "//input[@id='CreatedOnTo']"

    activity_log_type_xpath = "//span[@id='select2-ActivityLogTypeId-container']"
    activity_log_type_select_xpath = "//select[@id='ActivityLogTypeId']"

    ip_address_xpath = "//input[@id='IpAddress']"

    btn_search_xpath = "//button[@id='search-log']"

    btn_clear_alllog_xpath = "//button[@id='clearall']"

    # Activity Log scroll/body table
    table_log_xpath = "//div[contains(@class,'dt-scroll-body')]//table[contains(@class,'dataTable')]"
    table_log_rows_xpath = table_log_xpath + "//tbody/tr"
    table_log_cols_xpath = table_log_xpath + "//tbody/tr/td"

    activity_log_row_xpath = "//table[@id='activityLog-grid']//tbody/tr"
    delete_button_xpath = ".//td[6]/a[1]"

    #results table
    table_log_results_xpath = "//table[@id='activityLog-grid']"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def clickActivityPageMenuItem(self):
        activity_page = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.lnkActivityLog_menu_item_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", activity_page)
        self.driver.execute_script("arguments[0].click();", activity_page)

    def setCreatedFrom(self,date):
        created_from = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.created_from_xpath)
        ))
        created_from.clear()
        created_from.send_keys(date)

    def setCreatedTo(self,date):
        created_to = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.created_to_xpath)
        ))
        created_to.clear()
        created_to.send_keys(date)

    def clickActivityLogType(self):
        activity_type = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.activity_log_type_xpath)
        ))
        self.driver.execute_script("arguments[0].click();", activity_type)

    def setIpAddress(self,ip):
        ip_address = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.ip_address_xpath)
        ))
        ip_address.clear()
        ip_address.send_keys(ip)

    def clickSearch(self):
        search_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.btn_search_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_btn)
        self.driver.execute_script("arguments[0].click();", search_btn)

    def getNoOfRows(self):
        rows = self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, self.table_log_rows_xpath)
        ))
        return len(rows)


    def getNoOfColumns(self):
        rows = self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH,self.table_log_rows_xpath)
        ))
        first_row = rows[0]
        cols = first_row.find_elements(By.XPATH,"./td")
        return len(cols)

    def scrollToTable(self):
        result_table = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.table_log_results_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", result_table)

    def setActivity_LogType(self,log_type):
        activity_log_type =self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.activity_log_type_select_xpath)
        ))

        select = Select(activity_log_type)
        select.select_by_visible_text(log_type)

    def deleteSingleActivity(self,log_type):
        rows = self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH,self.activity_log_row_xpath)
        ))
        for row in rows:
            if log_type in row.text:
                delete_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH,self.delete_button_xpath)
                ))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", delete_button)
                self.driver.execute_script("arguments[0].click();", delete_button)

                return
        raise Exception(f"Activity log type {log_type} not found")

    def clearall_logs(self):
        btn_clear_log = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btn_clear_alllog_xpath)
        ))
        self.driver.execute_script("arguments[0].click();", btn_clear_log)








