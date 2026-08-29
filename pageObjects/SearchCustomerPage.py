import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Search customer page
class SearchCustomer:

    txtEmail_id = "SearchEmail"
    txtFirstName_id = "SearchFirstName"
    txtLastName_id = "SearchLastName"

    btnSearch_id = "search-customers"

    tblSearchResults_xpath = (
        "//div[@id='customers-grid_wrapper']//table"
    )

    table_xpath = "//table[@id='customers-grid']"

    tableRows_xpath = (
        "//table[@id='customers-grid']//tbody/tr"
    )

    tableColumns_xpath = (
        "//table[@id='customers-grid']//tbody/tr/td"
    )

    checkboxes_xpath = (
        "//table[@id='customers-grid']//tbody/tr/td[1]"
        "//input[@type='checkbox']"
    )

    btnExport_drp_xpath = (
        "//button[contains(@class,'btn-success') "
        "and contains(@class,'dropdown-toggle')]"
    )

    exportSelected_xml_xpath = "//button[@id='exportxml-selected']"

    exportAll_xml_xpath = (
        "//button[normalize-space()='Export to XML (all found)']"
    )

    exportSelected_excel_xpath = (
        "//button[@id='exportexcel-selected']"
    )

    exportAll_excel_xpath = (
        "//button[normalize-space()='Export to Excel (all found)']"
    )

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(self, driver):

        self.driver = driver

        # IMPORTANT:
        # Create explicit wait object
        self.wait = WebDriverWait(
            self.driver,
            15,
            ignored_exceptions=[
                StaleElementReferenceException
            ]
        )

    # -------------------------------------------------
    # Search Email
    # -------------------------------------------------

    def setEmail(self, email):
        for attempt in range(3):
            try:
                email_field = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID,self.txtEmail_id)
                    )
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",email_field)
                # Re-locate after scrolling because DOM may refresh
                email_field = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, self.txtEmail_id)
                    )
                )
                email_field.click()
                email_field.clear()
                email_field.send_keys(email)

                entered_value = email_field.get_attribute("value")
                print("Expected email :", repr(email))
                print("Actual email   :", repr(entered_value))

                if entered_value != email:
                    raise AssertionError(f"Email was not entered correctly"
                                         f"Expected: {email}, Actual: {entered_value}")
                return
            except StaleElementReferenceException:
                print(f"StaleElementReferenceException - "
                      f"retrying ({attempt + 1}/3)")
                if attempt == 2:
                    raise
                time.sleep(3)

    # -------------------------------------------------
    # First Name
    # -------------------------------------------------

    def setFirstName(self, firstName):

        for attempt in range(3):
            try:
                first_name_field = self.wait.until(EC.element_to_be_clickable(
                    (By.ID,self.txtFirstName_id)
                ))

                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",first_name_field)

                first_name_field.click()

                first_name_field.clear()

                first_name_field.send_keys(firstName)

                entered_value = first_name_field.get_attribute("value")

                print("Expected First Name: ",repr(firstName))
                print("Actual First Name : ",repr(entered_value))

                if entered_value == firstName:
                    return
            except StaleElementReferenceException:
                if attempt == 2:
                    raise
        raise AssertionError(f"First Name was not entered correctly.")



    #-------------------------------------------------#
    # Clear First Name
    # -------------------------------------------------

    def clearFirstName(self):

        first_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.txtFirstName_id)
            )
        )

        first_name_field.clear()

    # -------------------------------------------------
    # Last Name
    # -------------------------------------------------

    def setLastName(self, lastName):

        for attempt in range(3):
            try:
                last_name_field = self.wait.until(EC.element_to_be_clickable(
                    (By.ID,self.txtLastName_id)
                ))

                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",last_name_field)

                last_name_field.click()

                last_name_field.clear()

                last_name_field.send_keys(lastName)

                entered_value = last_name_field.get_attribute("value")

                print("Expected Last Name: ",repr(lastName))
                print("Actual Last Name : ",repr(entered_value))

                if entered_value == lastName:
                    return
            except StaleElementReferenceException:
                if attempt == 2:
                    raise
        raise AssertionError(f"Last Name was not entered correctly.")

    # -------------------------------------------------
    # Search Button
    # -------------------------------------------------

    def clickSearch(self):

        for attempt in range(3):

            try:

                search_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, self.btnSearch_id)
                    )
                )

                search_button.click()

                return

            except StaleElementReferenceException:

                if attempt == 2:
                    raise

    # -------------------------------------------------
    # Scroll To Table
    # -------------------------------------------------

    def scrollToTable(self):

        table = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.table_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            table
        )

    # -------------------------------------------------
    # Number Of Rows
    # -------------------------------------------------

    def getNoOfRows(self):

        return len(
            self.driver.find_elements(
                By.XPATH,
                self.tableRows_xpath
            )
        )

    # -------------------------------------------------
    # Number Of Columns
    # -------------------------------------------------

    def getNoOfColumns(self):

        return len(
            self.driver.find_elements(
                By.XPATH,
                self.tableColumns_xpath
            )
        )

    # -------------------------------------------------
    # Search Customer By Email
    # -------------------------------------------------

    def searchCustomerByEmail(self, email):

        rows = self.driver.find_elements(
            By.XPATH,
            self.tableRows_xpath
        )

        for row in rows:

            emailid = row.find_element(
                By.XPATH,
                "./td[2]"
            ).text.strip()

            if emailid == email:
                return True

        return False

    # -------------------------------------------------
    # Search Customer By Name
    # -------------------------------------------------

    def searchCustomerByName(self, Name):

        rows = self.driver.find_elements(
            By.XPATH,
            self.tableRows_xpath
        )

        for row in rows:

            name = row.find_element(
                By.XPATH,
                "./td[3]"
            ).text.strip()

            if name == Name:
                return True

        return False

    # -------------------------------------------------
    # Get Customer Checkboxes
    # -------------------------------------------------

    def getCustomerCheckBoxes(self):

        return self.driver.find_elements(
            By.XPATH,
            self.checkboxes_xpath
        )

    # -------------------------------------------------
    # Export Dropdown
    # -------------------------------------------------

    def clickExport(self):

        export_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnExport_drp_xpath)
            )
        )

        export_button.click()

    # -------------------------------------------------
    # Export Selected XML
    # -------------------------------------------------

    def clickExportSelected_XML(self):

        selected_option_xml = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.exportSelected_xml_xpath)
            )
        )

        selected_option_xml.click()

    # -------------------------------------------------
    # Export All XML
    # -------------------------------------------------

    def clickExportAll_XML(self):

        all_option_xml = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.exportAll_xml_xpath)
            )
        )

        all_option_xml.click()

    # -------------------------------------------------
    # Export Selected Excel
    # -------------------------------------------------

    def clickExportSelected_Excel(self):

        selected_option_excel = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.exportSelected_excel_xpath)
            )
        )

        selected_option_excel.click()

    # -------------------------------------------------
    # Export All Excel
    # -------------------------------------------------

    def clickExportAll_Excel(self):

        all_option_excel = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.exportAll_excel_xpath)
            )
        )

        all_option_excel.click()

    # -------------------------------------------------
    # Select Customer Checkbox
    # -------------------------------------------------

    def selectCustomerCheckBox(self, index):

        checkboxes = self.getCustomerCheckBoxes()

        if not checkboxes:

            raise Exception(
                "No customer checkbox found"
            )

        if index >= len(checkboxes):

            raise Exception(
                f"Checkbox index {index} out of range. "
                f"Available checkboxes: {len(checkboxes)}"
            )

        checkbox = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"({self.checkboxes_xpath})"
                    f"[{index + 1}]"
                )
            )
        )

        if not checkbox.is_selected():

            checkbox.click()

    # -------------------------------------------------
    # Edit Customer
    # -------------------------------------------------

    def clickEditCustomer(self, index):

        rows = self.driver.find_elements(
            By.XPATH,
            self.tableRows_xpath
        )

        if not rows:

            raise Exception(
                "No customers found in the table"
            )

        if index >= len(rows):

            raise Exception(
                f"Customer index {index} out of range. "
                f"Available customers: {len(rows)}"
            )

        # ---------------------------------------------
        # Checkbox XPath based on row index
        # ---------------------------------------------

        checkbox_xpath = (
            f"({self.tableRows_xpath})"
            f"[{index + 1}]"
            f"//td[1]//input[@type='checkbox']"
        )

        checkbox = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, checkbox_xpath)
            )
        )

        if not checkbox.is_selected():

            checkbox.click()

        # ---------------------------------------------
        # Re-locate Edit button after checkbox click
        # ---------------------------------------------

        edit_button_xpath = (
            f"({self.tableRows_xpath})"
            f"[{index + 1}]"
            f"//td[last()]//a"
        )

        edit_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, edit_button_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            edit_button
        )

        # Re-locate once more after scrolling
        edit_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, edit_button_xpath)
            )
        )

        edit_button.click()