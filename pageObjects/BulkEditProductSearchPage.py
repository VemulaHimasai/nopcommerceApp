from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BulkEditProductSearchPage:
    txtsearchproduct_name = "//input[@id='SearchProductName']"

    #vendor dropdown
    drpVendor = (
        "//label[normalize-space()='Vendor']"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//span[contains(@class,'select2-selection') and @role='combobox']"
    )

    #product type dropdown
    drpProducttype = (
        "//span[@role='combobox' "
        "and @aria-labelledby='select2-SearchProductTypeId-container']"
    )


    #drppublished
    drpPublishedtype =(
        "//span[contains(@class,'select2-container') "
        "and contains(@class,'select2-container--default')]"
        "//span[@role='combobox']"
    )

    #search button
    btnSearch = "//button[normalize-space()='Search']"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)


    def setProductName(self, product_name):
        product_name_field = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,self.txtsearchproduct_name)
        ))
        product_name_field.clear()
        product_name_field.send_keys(product_name)

    def SelectByVendor(self, vendor):

        vendor_dropdown = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.drpVendor)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_dropdown
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drpVendor)
            )
        )

        vendor_dropdown.click()

        vendor_option_xpath = (
            f"//li[contains(@class,'select2-results__option') "
            f"and normalize-space(.)='{vendor}']"
        )

        vendor_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, vendor_option_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_option
        )

        vendor_option.click()

        selected_vendor = self.driver.find_element(By.ID,"SearchVendorId")

        print( "SearchVendorId value:",selected_vendor.get_attribute("value"))

        print(f"Vendor '{vendor}' selected")

    def SelectByProductType(self, product_type):
       product_type_dropdown = self.wait.until(EC.element_to_be_clickable(
           (By.XPATH,self.drpProducttype)
       ))
       self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",product_type_dropdown)
       product_type_dropdown.click()
       product_type_option_xpath = (
            f"//li[contains(@class,'select2-results__option') "
            f"and normalize-space(.)='{product_type}']"
        )
       product_type_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,product_type_option_xpath)
        ))
       product_type_option.click()
       print(f"Product Type '{product_type}' selected")

    def SelectByPublishedType(self,published_type):
        published_dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.drpPublishedtype)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",published_dropdown)
        published_option_xpath = (
            f"//li[contains(@class,'select2-results__option') "
            f"and normalize-space(.)='{published_type}']"
        )
        published_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,published_option_xpath)
        ))
        published_option.click()
        print(f"Published type '{published_type}' selected")


    def clickSearch(self):
        search_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnSearch)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_btn)
        search_btn.click()

    def isProductDisplayed(self,product_name):
        product_xpath = (
            "//table[@class='table table-hover table-bordered table-striped']"
            f"//tbody//tr[.//input[contains(@id,'name-') "
            f"and @value='{product_name}']]"
        )
        try:
            product = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,product_xpath)
            ))
            print(f"Product '{product_name}' is displayed in search results")
            return product.is_displayed()
        except TimeoutException:
            print(f"Product '{product_name}' is not displayed in search results")
            return False

    def getSearchResults(self):
       product_list = self.wait.until(EC.presence_of_element_located(
           (By.ID,"product-list")
       ))
       self.wait.until(
           lambda driver:(
               product_list.get_attribute("innerHTML").strip() !=""
           )
       )
       rows = product_list.find_elements(By.XPATH,"./tr")
       print("Number of rows: ", len(rows))
       print("\nLoaded info:")
       try:
           loaded_info = self.driver.find_element(By.ID,"loaded-info")
           print(loaded_info.text)
       except:
           print("loaded-info not found")

       print("\nTable HTML:")
       print(product_list.get_attribute("innerHTML"))

       if len(rows) == 1 and "No data available in table" in rows[0].text:
           print("No data available in table")
           return []
       for row in rows:
           print(row.text)

       return rows







