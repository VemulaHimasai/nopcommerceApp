from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
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
    delete_button_xpath = ".//td[last()]/a"

    #results table
    table_log_results_xpath = "//table[@id='activityLog-grid']"

    no_data_message_xpath = (
        "//table[@id='activityLog-grid']//td"
        "[normalize-space()='No data available in table']"
    )

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

        search_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btn_search_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            search_btn
        )

        # Wait until the search request updates the table
        self.wait.until(
            lambda driver: driver.execute_script(
                "return typeof jQuery !== 'undefined' && jQuery.active === 0;"
            )
        )

        print("Activity Log search completed")

    def getNoOfRows(self):

        rows_xpath = (
            "//table[@id='activityLog-grid']//tbody/tr"
        )

        for attempt in range(3):

            try:

                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.table_log_results_xpath)
                    )
                )

                self.wait.until(
                    lambda driver: len(
                        driver.find_elements(By.XPATH, rows_xpath)
                    ) > 0
                )

                rows = self.driver.find_elements(
                    By.XPATH,
                    rows_xpath
                )

                print("Total table rows found:", len(rows))

                # Dynamic DataTable no-data row
                if len(rows) == 1:

                    row_text = rows[0].text.strip()

                    print(
                        "First row text:",
                        repr(row_text)
                    )

                    if (
                            "No data available in table" in row_text
                            or "No matching records found" in row_text
                    ):
                        return 0

                # Actual activity rows
                return len(rows)

            except StaleElementReferenceException:

                print(
                    f"Activity Log table refreshed. "
                    f"Retry {attempt + 1}/3"
                )

        raise Exception(
            "Unable to read Activity Log rows because "
            "the Activity Log table kept refreshing."
        )
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

    def setActivity_LogType(self, log_type):
        activity_log_type = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.activity_log_type_select_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            activity_log_type
        )

        selected = self.driver.execute_script("""
            var select = arguments[0];
            var text = arguments[1].trim();

            for (var i = 0; i < select.options.length; i++) {
                if (select.options[i].text.trim() === text) {
                    select.selectedIndex = i;

                    select.dispatchEvent(
                        new Event('change', {bubbles: true})
                    );

                    return true;
                }
            }

            return false;
        """, activity_log_type, log_type)

        if not selected:
            raise Exception(
                f"Activity log type '{log_type}' not found"
            )

        selected_option = Select(
            activity_log_type
        ).first_selected_option.text

        print("Expected Activity Log Type:", repr(log_type))
        print("Actual Activity Log Type  :", repr(selected_option))

        assert selected_option.strip() == log_type.strip(), \
            f"Expected '{log_type}', but got '{selected_option}'"

    def deleteSingleActivity(self,log_type):
        rows = self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH,self.activity_log_row_xpath)
        ))
        for row in rows:
            row_text = row.text.strip()
            if "No data available in table" in row_text:
                continue
            if log_type.strip() in row_text:
                delete_button = row.find_element(By.XPATH,self.delete_button_xpath)
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", delete_button)
                self.wait.until(lambda driver:(
                    delete_button.is_displayed()
                    and delete_button.is_enabled()
                ))
                self.driver.execute_script("arguments[0].click();", delete_button)
                return True
        raise Exception(f"Activity log type '{log_type}' not found")

    def clearall_logs(self):
        btn_clear_log = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btn_clear_alllog_xpath)
        ))
        self.driver.execute_script("arguments[0].click();", btn_clear_log)

    def isNoDataMessageDisplayed(self):
        try:
            message = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.no_data_message_xpath)
                )
            )

            return message.is_displayed()

        except TimeoutException:
            return False








