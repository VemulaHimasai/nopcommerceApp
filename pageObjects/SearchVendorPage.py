from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Search Vendor Page
class SearchVendorPage:
    txt_VendorName_xpath = "//input[@id='SearchName']"
    txt_VendorEmail_xpath = "//input[@id='SearchEmail']"

    btnSearch_xpath = "//button[@id='search-vendors']"

    tblSearchResults_xpath ="//div[@class='dt-scroll-head']//table[contains(@class,'dataTable')]"

    table_xpath = "//table[@id='vendors-grid']"

    tableRows_xpath = "//table[@id='vendors-grid']//tbody/tr"

    tableColumns_xpath = "//table[@id='vendors-grid']//tbody/tr/td"

    # Edit button
    btnEdit_xpath = "//table[@id='vendors-grid']//tbody/tr[1]//a[contains(@href,'/Admin/Vendor/Edit')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            self.driver,
            15,
            ignored_exceptions=[
                StaleElementReferenceException
            ]
        )

    def setName(self,name):
        vendor_name = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.txt_VendorName_xpath)
        ))
        vendor_name.clear()
        vendor_name.send_keys(name)

    def setEmail(self,email):
        vendor_email = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.txt_VendorEmail_xpath)
        ))
        vendor_email.clear()
        vendor_email.send_keys(email)

    def clickSearch(self):
        search_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.btnSearch_xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_btn)
        self.driver.execute_script("arguments[0].click();", search_btn)


    def getNoOfRows(self):
        rows = self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, self.tableRows_xpath)
        ))
        return len(rows)

    def getNoOfColumns(self):
        cols = self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, self.tableColumns_xpath)
        ))
        return len(cols)

    def searchVendorByName(self,vendor_name):
        rows = self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, self.tableRows_xpath)
        ))

        for row in rows:
            try:
                row_text = row.text.strip()
                if vendor_name.lower() in row_text.lower():
                    print("Vendor found: " + vendor_name)
                    return True
            except StaleElementReferenceException:
                continue
        print("Vendor not found: " + vendor_name)
        return False

    def searchVendorByEmail(self,vendor_email):
        rows = self.wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, self.tableRows_xpath)
        ))

        for row in rows:
            try:
                row_text = row.text.strip()
                if vendor_email.lower() in row_text.lower():
                    print("Vendor found: " + vendor_email)
                    return True
            except StaleElementReferenceException:
                continue
        print("Vendor not found: " + vendor_email)
        return False

    def clickEditVendorByName(self,vendor_name):
        edit_xpath = (f"//table[@id='vendors-grid']//tbody/tr"
                      f"[contains(.,'{vendor_name}')]"
                      f"//a[contains(@href,'/Admin/Vendor/Edit')]")
        edit_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, edit_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_btn)
        self.driver.execute_script("arguments[0].click();", edit_btn)







