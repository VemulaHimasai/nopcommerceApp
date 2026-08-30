from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Add Vendor Page
class AddVendor:

    #Vendor menu item
    lnkVendors_menu_item_xpath = "//a[@href='/Admin/Vendor/List']"

    #add new button
    btnAddVendor_xpath  = "//a[normalize-space()='Add new']"

    #vendor fields
    vendor_name_xpath = "//input[@id='Name']"
    vendor_desc_xpath = "//div[@role='textbox' and @contenteditable='true']"
    vendor_email_xpath = "//input[@id='Email']"

    btnvendorsave_xpath = "//button[@name='save']"

    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def clickonVendorMenuItem(self):
        vendor_menu_item = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,self.lnkVendors_menu_item_xpath)
            )
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", vendor_menu_item)
        self.driver.execute_script("arguments[0].click();", vendor_menu_item)

        #wait until vendors page is loaded
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,self.btnAddVendor_xpath)
            )
        )


    #Add New Vendor
    def clickonAddNew(self):
        add_new_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,self.btnAddVendor_xpath)
            )
        )

        print("Button found:", add_new_button.text)
        print("Button href:", add_new_button.get_attribute("href"))

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_new_button)
        self.driver.execute_script("arguments[0].click();", add_new_button)

        # Wait until Add Vendor page is loaded
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.vendor_name_xpath)
        ))

        print("Add Vendor page opened")
        print("Current URL:", self.driver.current_url)
        print("Page title:", self.driver.title)

    #enter vendor name
    def setVendorName(self,name):
        vendor_name = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.vendor_name_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", vendor_name)
        vendor_name.clear()
        vendor_name.send_keys(name)

        entered_value = vendor_name.get_attribute("value")

        print("Expected Vendor Name:", repr(name))
        print("Actual Vendor Name:", repr(entered_value))

        assert entered_value == name, \
        f"Vendor name was not entered. Expected: {name}, Actual: {entered_value}"


    #enter vendor description
    def setVendorDesc(self,description):
        vendor_desc = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.vendor_desc_xpath)
        ))
        vendor_desc.clear()
        vendor_desc.send_keys(description)

    #enter vendor email
    def setVendorEmail(self,email):
        vendor_email = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.vendor_email_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", vendor_email)
        vendor_email.clear()
        vendor_email.send_keys(email)
        entered_value = vendor_email.get_attribute("value")
        print("Expected Vendor Email:", repr(email))
        print("Actual Vendor Email:", repr(entered_value))

        assert entered_value == email, \
            f"Vendor name was not entered. Expected: {email}, Actual: {entered_value}"



    #click save
    def clickSave(self):
        save_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnvendorsave_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button)
        self.driver.execute_script("arguments[0].click();", save_button)

    def editVendorName(self,new_vendor_name):
        vendor_name = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.vendor_name_xpath)
        ))
        vendor_name.clear()
        vendor_name.send_keys(new_vendor_name)





