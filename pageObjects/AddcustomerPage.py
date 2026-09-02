from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)


# Add Customer Page
class AddCustomer:

    # Customers menu
    lnkCustomers_menu_xpath = "//a[@href='#']//p[contains(text(),'Customers')]"
    lnkCustomers_menuitem_xpath = "//a[@href='/Admin/Customer/List']"

    # Add New button
    btnAddnew_xpath = "//a[contains(@href,'/Admin/Customer/Create')]"

    # Customer fields
    txtEmail_xpath = "//input[@id='Email']"
    txtPassword_xpath = "//input[@id='Password']"
    txtFirstName_xpath = "//input[@id='FirstName']"
    txtLastName_xpath = "//input[@id='LastName']"

    # Gender
    rdMaleGender_id = "Gender_Male"
    rdFemaleGender_id = "Gender_Female"

    # Customer Roles
    txtcustomerRoles_xpath = "//ul[@class='select2-selection__rendered']"
    lstAdministrator_xpath = "//li[contains(text(),'Administrators')]"
    lstForumModerator_xpath = "//li[contains(text(),'Forum Moderators')]"
    lstGuests_xpath = "//li[contains(text(),'Guests')]"
    lstRegistered_xpath = "//li[contains(text(),'Registered')]"
    lstVendors_xpath = "//li[contains(text(),'Vendors')]"


    # Vendor
    drpmgrofVendor_xpath = "//span[@id='select2-VendorId-container']"
    drpVendor1_xpath = (
        "//li[@class='select2-search select2-search--inline']"
        "//input[@role='searchbox']"
    )

    # Other fields
    txtCompanyName_xpath = "//input[@id='Company']"
    txtAdminContent_xpath = "//textarea[@id='AdminComment']"

    # Save
    btnSave_xpath = "//button[@name='save']"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # -----------------------------
    # Customers Navigation
    # -----------------------------

    def clickOnCustomersMenu(self):
        for attempt in range(3):
            try:
                customers_menu = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,self.lnkCustomers_menu_xpath)
                ))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",customers_menu)
                self.driver.execute_script("arguments[0].click();",customers_menu)
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,"//a[contains(@href,'/Admin/Customer/List')]")
                ))
                print("Customers menu opened")
                return
            except (StaleElementReferenceException,TimeoutException):
                print(f"Customers menu not ready. "
                f"Retrying ({attempt + 1}/3)...")
                if attempt == 2:
                    raise


    def clickonCustomersMenuItem(self):
        for attempt in range(3):
            try:
                customers_menu_item = self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH,self.lnkCustomers_menuitem_xpath)
                ))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",customers_menu_item)
                self.driver.execute_script("arguments[0].click();",customers_menu_item)
                self.wait.until(EC.url_contains("/Admin/Customer/List"))
                self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH,self.btnAddnew_xpath)
                ))
                print("Customers list page opened")
                print("Current Url: ",self.driver.current_url)
                return
            except (StaleElementReferenceException,TimeoutException):
                print(f"Customer menu item not ready. "
                f"Retrying ({attempt + 1}/3)...")
                if attempt < 2:
                    try:
                        customers_menu = self.wait.until(EC.element_to_be_clickable(
                            (By.XPATH,self.lnkCustomers_menu_xpath)
                        ))
                        self.driver.execute_script("arguments[0].click();",customers_menu)
                    except (StaleElementReferenceException,TimeoutException):
                        pass
                else:
                    raise




    # -----------------------------
    # Add New Customer
    # -----------------------------

    def clickonAddNew(self):

        add_new_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnAddnew_xpath)
            )
        )

        print("Button found:", add_new_button.text)
        print("Button href:", add_new_button.get_attribute("href"))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_new_button
        )

        # Firefox workaround: navigate using the actual href
        self.driver.get(
            add_new_button.get_attribute("href")
        )

        print("After Add New navigation")
        print("Current URL:", self.driver.current_url)
        print("Current Title:", self.driver.title)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtEmail_xpath)
            )
        )
    # -----------------------------
    # Customer Details
    # -----------------------------

    def setEmail(self, email):

        email_field = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.txtEmail_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            email_field
        )

        email_field.click()
        email_field.clear()
        email_field.send_keys(email)

        actual_value = email_field.get_attribute("value")

        print("Expected email:", repr(email))
        print("Actual email:", repr(actual_value))

        assert actual_value == email, (
            f"Email was not entered correctly. "
            f"Expected: {email}, Actual: {actual_value}"
        )

    def setPassword(self, password):

        password_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtPassword_xpath)
            )
        )

        password_field.clear()
        password_field.send_keys(password)

    def setFirstName(self, firstName):

        first_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtFirstName_xpath)
            )
        )

        first_name_field.clear()
        first_name_field.send_keys(firstName)

    def setLastName(self, lastName):

        last_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtLastName_xpath)
            )
        )

        last_name_field.clear()
        last_name_field.send_keys(lastName)

    # -----------------------------
    # Gender
    # -----------------------------

    def setGender(self, gender):

        if gender.lower() == "male":

            male = self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, self.rdMaleGender_id)
                )
            )

            male.click()

        elif gender.lower() == "female":

            female = self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, self.rdFemaleGender_id)
                )
            )

            female.click()

        else:
            raise ValueError(
                f"Invalid gender: {gender}. Use 'Male' or 'Female'."
            )

    # -----------------------------
    # Company
    # -----------------------------

    def setCompanyName(self, company):

        company_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtCompanyName_xpath)
            )
        )

        company_field.clear()
        company_field.send_keys(company)

    # -----------------------------
    # Admin Comment
    # -----------------------------

    def setAdminComment(self, comment):

        comment_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.txtAdminContent_xpath)
            )
        )

        comment_field.clear()
        comment_field.send_keys(comment)

    # -----------------------------
    # Save Customer
    # -----------------------------

    def clickSave(self):

        save_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnSave_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            save_button
        )

        save_button.click()

    def setCustomerRoles(self, role):

        # Click Customer Roles dropdown
        roles_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.txtcustomerRoles_xpath)
            )
        )

        roles_dropdown.click()

        # Select requested customer role
        role_option = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//li[contains(@class,'select2-results__option') "
                    f"and normalize-space()='{role}']"
                )
            )
        )

        print("Role option found:", repr(role_option.text))

        # Scroll role into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            role_option
        )

        # Click using JavaScript
        self.driver.execute_script(
            "arguments[0].click();",
            role_option
        )

        print("Clicked role:", role)

        # Verify that role was actually selected
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//li[contains(@class,'select2-selection__choice') "
                    f"and @title='{role}']"
                )
            )
        )

        print("Customer Role successfully selected:", role)

        # Guests cannot be both Registered and Guests
        if role.lower() == "guests":
            remove_registered = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//li[@title='Registered']"
                        "//span[@role='presentation']"
                    )
                )
            )

            remove_registered.click()
    def setManagerofVendor(self, vendor):
        # Click Manager of Vendor dropdown
        vendor_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drpmgrofVendor_xpath)
            )
        )

        vendor_dropdown.click()

        # Select vendor
        vendor_option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//li[contains(@class,'select2-results__option') "
                    f"and normalize-space()='{vendor}']"
                )
            )
        )

        vendor_option.click()