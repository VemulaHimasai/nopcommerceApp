from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchVendorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    vendor_table_xpath = "//table[@id='vendors-grid']"
    vendor_rows_xpath = "//table[@id='vendors-grid']//tbody/tr"
    previous_button_xpath = "//div[@id='vendors-grid_wrapper']//a[contains(@class,'previous')]"
    next_button_xpath = "//div[@id='vendors-grid_wrapper']//a[contains(@class,'next')]"

    delete_button_xpath = "//*[@id='vendor-delete']"
    confirm_delete_xpath = "//button[normalize-space()='Delete']"

    success_message_xpath = "//div[contains(@class,'alert-success')]"

    def waitForVendorList(self):
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.vendor_table_xpath)
        ))

    def getVendorRows(self):
        return self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, self.vendor_rows_xpath)
        ))

    def getFirstVendorRow(self):
        rows = self.getVendorRows()
        if not rows:
            return None
        return rows[0]

    def getFirstVendorName(self):
        row = self.getFirstVendorRow()
        if row is None:
            return None
        cells = row.find_elements(By.TAG_NAME,"td")
        if not cells:
            return None
        return cells[0].text.strip()

    def getVendorNameByRow(self,row_number):
        rows = self.getVendorRows()
        if row_number < 1 or row_number > len(rows):
            raise IndexError(f"Invalid row number: {row_number}."
                             f"Available rows: {len(rows)}")
        row = rows[row_number - 1]
        cells = row.find_elements(By.TAG_NAME,"td")
        if not cells:
            return None
        row_data = [cell.text.strip() for cell in cells]
        print(f"Row {row_number} data:",row_data)
        vendor_name = cells[0].text.strip()
        return vendor_name

    def clickEditFirstVendor(self):
        row = self.getFirstVendorRow()
        if row is None:
            raise Exception("No vendor found in the table")
        edit_button = row.find_element(By.XPATH,".//a[contains(@href,'/Admin/Vendor/Edit')]")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_button)
        self.wait.until(EC.element_to_be_clickable(edit_button))
        edit_button.click()


    def clickEditVendorByRow(self,row_number):
        rows = self.getVendorRows()
        if row_number < 1 or row_number > len(rows):
            raise Exception("Invalid row number")

        row = rows[row_number - 1]
        print(f"Clicking Edit for row {row_number}:", row.text)

        edit_button = row.find_element(By.XPATH,".//a[contains(@href,'/Admin/Vendor/Edit')]")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_button)
        self.wait.until(EC.element_to_be_clickable(edit_button))
        edit_button.click()

    def clickNextPage(self):
        next_button = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,self.next_button_xpath)
        ))
        classes = next_button.get_attribute("class")
        if classes and "disabled" in classes:
            print("Next button is disabled")
            return False
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_button)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.next_button_xpath)
        ))
        old_rows = self.getVendorRows()
        next_button.click()
        try:
            self.wait.until(EC.staleness_of(old_rows[0]))
        except Exception:
            pass
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.vendor_table_xpath)
        ))
        print("Next Page clicked")
        return True

    def clickPreviousPage(self):
        previous_button = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, self.previous_button_xpath)
        ))
        classes = previous_button.get_attribute("class")
        if classes and "disabled" in classes:
            print("Previous button is disabled")
            return False
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", previous_button)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.previous_button_xpath)
        ))
        old_rows = self.getVendorRows()
        previous_button.click()
        try:
            self.wait.until(EC.staleness_of(old_rows[0]))
        except Exception:
            pass
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.vendor_table_xpath)
        ))
        print("Previous Page clicked")
        return True

    def clickDeleteButton(self):
        delete_button = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.delete_button_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",delete_button)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.delete_button_xpath)
        ))
        delete_button.click()
        print("Delete button clicked successfully")

    def clickConfirmDelete(self):
        confirm_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.confirm_delete_xpath)
        ))
        confirm_button.click()
        print("Delete confirmation clicked successfully")

    def getSuccessMessage(self):
        message = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.success_message_xpath)
        ))
        return message.text.strip()

    def getVendorNameByOverallRow(self,overall_row_number):
        if overall_row_number < 1:
            raise ValueError("Row number must be greater than 0")
        remaining_row = overall_row_number
        while True:
            rows = self.getVendorRows()
            print(f"Current page contains {len(rows)} vendor rows")

            if remaining_row <= len(rows):
                row = rows[remaining_row - 1]
                cells = row.find_elements(By.TAG_NAME,"td")
                if not cells:
                    return None
                row_data = [cell.text.strip() for cell in cells]
                print(f"Overall row {overall_row_number} "
                f"found on current page at row {remaining_row}:",
                row_data)
                return cells[0].text.strip()
            remaining_row -= len(rows)
            print(f"Moving to next page. "
            f"Remaining row: {remaining_row}")
            if not self.clickNextPage():
                raise IndexError(f"Vendor row {overall_row_number} does not exist. "
                f"Reached the last page.")

    def clickEditVendorByOverallRow(self,overall_row_number):
        if overall_row_number < 1:
            raise ValueError("Row number must be greater than 0")
        remaining_row = overall_row_number
        while True:
            rows = self.getVendorRows()
            print(f"Current page contains {len(rows)} vendor rows")
            if remaining_row <= len(rows):
                row = rows[remaining_row - 1]
                print(f"Clicking Edit for overall row "
                f"{overall_row_number}, current-page row "
                f"{remaining_row}: {row.text}")
                edit_button = row.find_element(By.XPATH,".//a[contains(@href,'/Admin/Vendor/Edit')]")
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",edit_button)
                self.wait.until(EC.element_to_be_clickable(edit_button))
                edit_button.click()
                return
            remaining_row -= len(rows)
            if not self.clickNextPage():
                raise IndexError(f"Vendor row {overall_row_number} does not exist. "
                f"Reached the last page.")








