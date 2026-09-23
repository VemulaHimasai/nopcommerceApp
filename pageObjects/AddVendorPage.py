from selenium.common import TimeoutException
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

        print("Waiting for Vendor menu item...")

        try:

            # -------------------------------------------------
            # Wait until Vendor menu item exists in the DOM
            # -------------------------------------------------
            vendor_menu_item = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.lnkVendors_menu_item_xpath)
                )
            )

            print("Vendor menu item found in DOM.")

            print(
                "Vendor menu displayed:",
                vendor_menu_item.is_displayed()
            )

            print(
                "Vendor menu enabled:",
                vendor_menu_item.is_enabled()
            )

            # -------------------------------------------------
            # Scroll into view
            # -------------------------------------------------
            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'nearest'
                });
                """,
                vendor_menu_item
            )

            # -------------------------------------------------
            # Re-find immediately before clicking
            # -------------------------------------------------
            vendor_menu_item = self.driver.find_element(
                By.XPATH,
                self.lnkVendors_menu_item_xpath
            )

            # -------------------------------------------------
            # JavaScript click
            # -------------------------------------------------
            self.driver.execute_script(
                "arguments[0].click();",
                vendor_menu_item
            )

            print(
                "Vendor menu item clicked successfully."
            )

            # -------------------------------------------------
            # Wait for Vendor List navigation
            # -------------------------------------------------
            self.wait.until(
                EC.url_contains("/Admin/Vendor/List")
            )

            print(
                "Vendor list page loaded."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Page title:",
                self.driver.title
            )

        except TimeoutException:

            print(
                "TIMEOUT while opening Vendor List."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Page title:",
                self.driver.title
            )

            # -------------------------------------------------
            # Diagnostic: check Vendor link
            # -------------------------------------------------
            try:

                vendor_links = self.driver.find_elements(
                    By.XPATH,
                    self.lnkVendors_menu_item_xpath
                )

                print(
                    "Vendor menu elements found:",
                    len(vendor_links)
                )

                for index, element in enumerate(vendor_links):

                    try:

                        print(
                            f"Vendor link {index}: "
                            f"displayed={element.is_displayed()}, "
                            f"enabled={element.is_enabled()}, "
                            f"text={repr(element.text)}, "
                            f"href={element.get_attribute('href')}"
                        )

                    except Exception:

                        print(
                            f"Vendor link {index}: "
                            "could not read element state"
                        )

            except Exception as diagnostic_error:

                print(
                    "Vendor link diagnostic failed:",
                    diagnostic_error
                )

            raise

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
    def setVendorName(self, name):
        vendor_name = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.vendor_name_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_name
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.vendor_name_xpath)
            )
        )

        vendor_name.click()
        vendor_name.clear()
        vendor_name.send_keys(name)

        # Wait until the entered value is available
        self.wait.until(
            lambda driver: driver.find_element(
                By.XPATH,
                self.vendor_name_xpath
            ).get_attribute("value") == name
        )

        # Get the element again after the wait
        vendor_name = self.driver.find_element(
            By.XPATH,
            self.vendor_name_xpath
        )

        entered_value = vendor_name.get_attribute("value")

        print("Expected Vendor Name:", repr(name))
        print("Actual Vendor Name:", repr(entered_value))

        assert entered_value == name, (
            f"Vendor name was not entered. "
            f"Expected: {name}, Actual: {entered_value}"
        )

    def setVendorDesc(self, description):
        vendor_desc = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.vendor_desc_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_desc
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.vendor_desc_xpath)
            )
        )

        vendor_desc.click()
        vendor_desc.clear()
        vendor_desc.send_keys(description)

        print(
            "Expected Vendor Description:",
            repr(description)
        )

        entered_value = vendor_desc.get_attribute("textContent")

        print(
            "Actual Vendor Description:",
            repr(entered_value)
        )
    def setVendorEmail(self, email):
        vendor_email = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.vendor_email_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            vendor_email
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.vendor_email_xpath)
            )
        )

        vendor_email.click()
        vendor_email.clear()
        vendor_email.send_keys(email)

        # Wait until the entered value is available
        self.wait.until(
            lambda driver: driver.find_element(
                By.XPATH,
                self.vendor_email_xpath
            ).get_attribute("value") == email
        )

        # Get the element again after the wait
        vendor_email = self.driver.find_element(
            By.XPATH,
            self.vendor_email_xpath
        )

        entered_value = vendor_email.get_attribute("value")

        print("Expected Vendor Name:", repr(email))
        print("Actual Vendor Name:", repr(entered_value))

        assert entered_value == email, (
            f"Vendor name was not entered. "
            f"Expected: {email}, Actual: {entered_value}"
        )



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





