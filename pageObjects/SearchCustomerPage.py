
import time

from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException,
                                        NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Search Customer Page
class SearchCustomer:

    # -------------------------------------------------
    # Search Fields
    # -------------------------------------------------

    txtEmail_id = "SearchEmail"
    txtFirstName_id = "SearchFirstName"
    txtLastName_id = "SearchLastName"

    # -------------------------------------------------
    # Search Button
    # -------------------------------------------------

    btnSearch_id = "search-customers"

    # -------------------------------------------------
    # Customer Table
    # -------------------------------------------------

    tblSearchResults_xpath = (
        "//div[@id='customers-grid_wrapper']//table"
    )

    table_xpath = (
        "//table[@id='customers-grid']"
    )

    tableRows_xpath = (
        "//table[@id='customers-grid']//tbody/tr"
    )

    tableColumns_xpath = (
        "//table[@id='customers-grid']//tbody/tr/td"
    )

    # -------------------------------------------------
    # Customer Checkboxes
    # -------------------------------------------------

    checkboxes_xpath = (
        "//table[@id='customers-grid']//tbody/tr/td[1]"
        "//input[@type='checkbox']"
    )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    btnExport_drp_xpath = (
        "//button[contains(@class,'btn-success') "
        "and contains(@class,'dropdown-toggle')]"
    )

    exportSelected_xml_xpath = (
        "//button[@id='exportxml-selected']"
    )

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

        self.wait = WebDriverWait(
            self.driver,
            15
        )

    # =================================================
    # SEARCH EMAIL
    # =================================================



    def setEmail(self, email):

        for attempt in range(3):

            try:
                # Wait until the email field exists in the DOM
                email_field = self.wait.until(
                    EC.presence_of_element_located(
                        (By.ID, self.txtEmail_id)
                    )
                )

                # Scroll to the field
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    email_field
                )

                # Wait until it is visible and enabled
                self.wait.until(
                    lambda driver: (
                            driver.find_element(
                                By.ID,
                                self.txtEmail_id
                            ).is_displayed()
                            and
                            driver.find_element(
                                By.ID,
                                self.txtEmail_id
                            ).is_enabled()
                    )
                )

                # Re-locate the element after the wait
                email_field = self.driver.find_element(
                    By.ID,
                    self.txtEmail_id
                )

                email_field.click()
                email_field.clear()
                email_field.send_keys(email)

                # Verify the value
                self.wait.until(
                    lambda driver: (
                            driver.find_element(
                                By.ID,
                                self.txtEmail_id
                            ).get_attribute("value") == email
                    )
                )

                entered_value = self.driver.find_element(
                    By.ID,
                    self.txtEmail_id
                ).get_attribute("value")

                print("Expected email :", repr(email))
                print("Actual email   :", repr(entered_value))

                if entered_value != email:
                    raise AssertionError(
                        f"Email was not entered correctly. "
                        f"Expected: {email}, "
                        f"Actual: {entered_value}"
                    )

                print("Email entered successfully")

                return

            except StaleElementReferenceException:

                print(
                    f"Email field became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

            except TimeoutException:

                print(
                    f"Email field was not ready. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        raise AssertionError(
            f"Unable to enter email: {email}"
        )



    # =================================================
    # FIRST NAME
    # =================================================

    def setFirstName(self, firstName):

        for attempt in range(3):

            try:

                first_name_field = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, self.txtFirstName_id)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    first_name_field
                )

                first_name_field = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, self.txtFirstName_id)
                    )
                )

                first_name_field.click()
                first_name_field.clear()
                first_name_field.send_keys(firstName)

                # Re-locate element before reading value
                entered_value = self.wait.until(
                    lambda driver: driver.find_element(
                        By.ID,
                        self.txtFirstName_id
                    ).get_attribute("value")
                )

                print(
                    "Expected First Name:",
                    repr(firstName)
                )

                print(
                    "Actual First Name  :",
                    repr(entered_value)
                )

                if entered_value == firstName:
                    return

                raise AssertionError(
                    f"First Name was not entered correctly. "
                    f"Expected: {firstName}, "
                    f"Actual: {entered_value}"
                )

            except StaleElementReferenceException:

                print(
                    f"First Name field became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        raise AssertionError(
            f"Unable to enter first name: {firstName}"
        )



    # =================================================
    # CLEAR FIRST NAME
    # =================================================

    def clearFirstName(self):

        first_name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.txtFirstName_id)
            )
        )

        first_name_field.clear()

    # =================================================
    # LAST NAME
    # =================================================

    def setLastName(self, lastName):

        for attempt in range(3):

            try:

                last_name_field = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, self.txtLastName_id)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    last_name_field
                )

                last_name_field = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, self.txtLastName_id)
                    )
                )

                last_name_field.click()
                last_name_field.clear()
                last_name_field.send_keys(lastName)

                # Verify entered value
                self.wait.until(
                    lambda driver:
                    driver.find_element(
                        By.ID,
                        self.txtLastName_id
                    ).get_attribute("value") == lastName
                )

                entered_value = self.driver.find_element(
                    By.ID,
                    self.txtLastName_id
                ).get_attribute("value")

                print(
                    "Expected Last Name:",
                    repr(lastName)
                )

                print(
                    "Actual Last Name  :",
                    repr(entered_value)
                )

                if entered_value != lastName:

                    raise AssertionError(
                        f"Last Name was not entered correctly. "
                        f"Expected: {lastName}, "
                        f"Actual: {entered_value}"
                    )

                return

            except StaleElementReferenceException:

                print(
                    f"Last Name field became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        raise AssertionError(
            f"Unable to enter last name: {lastName}"
        )

    # =================================================
    # SEARCH BUTTON
    # =================================================

    def clickSearch(self):

        for attempt in range(3):

            try:

                search_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, self.btnSearch_id)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    search_button
                )

                search_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, self.btnSearch_id)
                    )
                )

                search_button.click()

                # Wait for table
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.table_xpath)
                    )
                )

                return

            except StaleElementReferenceException:

                print(
                    f"Search button became stale. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        raise AssertionError(
            "Unable to click Search button."
        )

    # =================================================
    # SCROLL TO TABLE
    # =================================================

    def scrollToTable(self):

        table = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.table_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            table
        )

    # =================================================
    # WAIT FOR TABLE
    # =================================================

    def waitForTable(self):

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.table_xpath)
            )
        )

    # =================================================
    # WAIT FOR REAL CUSTOMER ROWS
    # =================================================

    def waitForCustomerRows(self):

        def real_customer_rows_loaded(driver):

            rows = driver.find_elements(
                By.XPATH,
                self.tableRows_xpath
            )

            for row in rows:

                try:

                    columns = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    # A real customer row has at least 2 columns
                    # and the Email column contains a value.
                    if len(columns) >= 2:

                        email = columns[1].text.strip()

                        if email:
                            return True

                except StaleElementReferenceException:

                    return False

            return False

        self.wait.until(real_customer_rows_loaded)

    # =================================================
    # NUMBER OF ROWS
    # =================================================

    def getNoOfRows(self):

        self.waitForTable()

        return len(
            self.driver.find_elements(
                By.XPATH,
                self.tableRows_xpath
            )
        )

    # =================================================
    # NUMBER OF COLUMNS
    # =================================================

    def getNoOfColumns(self):

        self.waitForTable()

        return len(
            self.driver.find_elements(
                By.XPATH,
                self.tableColumns_xpath
            )
        )

    # =================================================
    # GET TABLE DATA
    # =================================================

    def getTableData(self):

        self.waitForTable()

        for attempt in range(3):

            try:

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                table_data = []

                for row in rows:

                    columns = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    row_data = [
                        column.text.strip()
                        for column in columns
                    ]

                    table_data.append(row_data)

                return table_data

            except StaleElementReferenceException:

                print(
                    f"Customer table refreshed while reading data. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        raise AssertionError(
            "Unable to read customer table data."
        )

    # =================================================
    # GET CUSTOMER NAMES
    # =================================================

    def getCustomerNames(self):

        for attempt in range(3):

            try:

                self.waitForTable()

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                customer_names = []

                for row in rows:

                    columns = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if not columns:
                        continue

                    customer_name = columns[0].text.strip()

                    if not customer_name:
                        continue

                    if customer_name == "Loading...":
                        continue

                    if "No data available" in customer_name:
                        continue

                    customer_names.append(customer_name)

                print(
                    "Customer names:",
                    customer_names
                )

                return customer_names

            except StaleElementReferenceException:

                print(
                    f"Customer table refreshed while reading names. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        raise AssertionError(
            "Unable to read customer names."
        )

    # =================================================
    # SEARCH CUSTOMER BY EMAIL
    # =================================================

    def searchCustomerByEmail(self, email):

        for attempt in range(3):

            try:

                self.waitForTable()

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                for row in rows:

                    columns = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if len(columns) < 2:
                        continue

                    emailid = columns[1].text.strip()

                    if emailid == email:
                        return True

                return False

            except StaleElementReferenceException:

                print(
                    f"Customer table refreshed while searching "
                    f"email '{email}'. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        return False

    # =================================================
    # SEARCH CUSTOMER BY NAME
    # =================================================

    def searchCustomerByName(self, Name):

        for attempt in range(3):

            try:

                self.waitForTable()

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                for row in rows:

                    columns = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if len(columns) < 3:
                        continue

                    name = columns[2].text.strip()

                    if name == Name:
                        return True

                return False

            except StaleElementReferenceException:

                print(
                    f"Customer table refreshed while searching "
                    f"name '{Name}'. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        return False

    # =================================================
    # GET CUSTOMER CHECKBOXES
    # =================================================

    def getCustomerCheckBoxes(self):

        return self.driver.find_elements(
            By.XPATH,
            self.checkboxes_xpath
        )

    # =================================================
    # SELECT CUSTOMER CHECKBOX
    # =================================================

    def selectCustomerCheckBox(self, index):

        checkboxes = self.getCustomerCheckBoxes()

        if not checkboxes:

            raise AssertionError(
                "No customer checkbox found."
            )

        if index < 0 or index >= len(checkboxes):

            raise IndexError(
                f"Checkbox index {index} out of range. "
                f"Available checkboxes: {len(checkboxes)}"
            )

        checkbox_xpath = (
            f"({self.checkboxes_xpath})"
            f"[{index + 1}]"
        )

        checkbox = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, checkbox_xpath)
            )
        )

        if not checkbox.is_selected():

            checkbox.click()

    # =================================================
    # EXPORT DROPDOWN
    # =================================================

    def clickExport(self):

        export_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnExport_drp_xpath)
            )
        )

        export_button.click()

    # =================================================
    # EXPORT SELECTED XML
    # =================================================

    def clickExportSelected_XML(self):

        selected_option_xml = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.exportSelected_xml_xpath)
            )
        )

        selected_option_xml.click()

    # =================================================
    # EXPORT ALL XML
    # =================================================

    def clickExportAll_XML(self):

        all_option_xml = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.exportAll_xml_xpath)
            )
        )

        all_option_xml.click()

    # =================================================
    # EXPORT SELECTED EXCEL
    # =================================================

    def clickExportSelected_Excel(self):

        selected_option_excel = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.exportSelected_excel_xpath)
            )
        )

        selected_option_excel.click()

    # =================================================
    # EXPORT ALL EXCEL
    # =================================================

    def clickExportAll_Excel(self):

        all_option_excel = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.exportAll_excel_xpath)
            )
        )

        all_option_excel.click()

    # =================================================
    # EDIT CUSTOMER BY INDEX
    # =================================================

    def clickEditCustomer(self, index):

        for attempt in range(3):

            try:

                self.waitForTable()

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                if not rows:

                    raise AssertionError(
                        "No customers found in the table."
                    )

                if index < 0 or index >= len(rows):

                    raise IndexError(
                        f"Customer index {index} out of range. "
                        f"Available customers: {len(rows)}"
                    )

                # -----------------------------------------
                # Checkbox
                # -----------------------------------------

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

                # -----------------------------------------
                # Edit Button
                # -----------------------------------------

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
                    "arguments[0].scrollIntoView({block:'center'});",
                    edit_button
                )

                # Re-locate after scrolling
                edit_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, edit_button_xpath)
                    )
                )

                edit_button.click()

                return

            except StaleElementReferenceException:

                print(
                    f"Customer table refreshed while editing "
                    f"index {index}. "
                    f"Retrying ({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

        raise AssertionError(
            f"Unable to edit customer at index {index}."
        )

    # =================================================
    # EDIT CUSTOMER BY EMAIL
    # =================================================

    def clickEditCustomerByEmail(self, email):

        email = email.strip()

        max_pages = 100
        page_count = 0

        while page_count < max_pages:

            page_count += 1

            print(
                f"\n========== CHECKING CUSTOMER PAGE {page_count} =========="
            )

            # =========================================================
            # WAIT FOR CUSTOMER TABLE
            # =========================================================

            self.waitForTable()

            # =========================================================
            # WAIT FOR DATATABLES PROCESSING TO FINISH
            # =========================================================

            processing_xpaths = [
                "//div[@id='customers-grid_processing']",
                "//div[contains(@class,'dataTables_processing')]"
            ]

            for processing_xpath in processing_xpaths:

                try:

                    processing_element = self.driver.find_element(
                        By.XPATH,
                        processing_xpath
                    )

                    if processing_element.is_displayed():
                        print(
                            "Customer DataTable is processing..."
                        )

                        self.wait.until(
                            EC.invisibility_of_element_located(
                                (
                                    By.XPATH,
                                    processing_xpath
                                )
                            )
                        )

                        print(
                            "Customer DataTable processing completed."
                        )

                        break

                except (
                        NoSuchElementException,
                        StaleElementReferenceException
                ):

                    continue

                except TimeoutException:

                    print(
                        "DataTable processing indicator did not "
                        "disappear within the expected time."
                    )

                    break

            # =========================================================
            # WAIT FOR CUSTOMER ROWS
            # =========================================================

            self.wait.until(
                lambda driver: (
                        len(
                            driver.find_elements(
                                By.XPATH,
                                self.tableRows_xpath
                            )
                        ) > 0
                )
            )

            # =========================================================
            # SEARCH CURRENT PAGE
            # =========================================================

            restart_current_page = False

            try:

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                print(
                    f"Rows found on current page: {len(rows)}"
                )

                # =====================================================
                # DEBUG CURRENT PAGE
                # =====================================================

                for row_number, row in enumerate(
                        rows,
                        start=1
                ):

                    try:

                        row_text = row.text.strip()

                        print(
                            f"Row {row_number}: "
                            f"{row_text[:200]}"
                        )

                    except StaleElementReferenceException:

                        print(
                            f"Row {row_number} became stale "
                            f"during debug."
                        )

                # =====================================================
                # SEARCH EACH ROW
                # =====================================================

                for row_index in range(len(rows)):

                    row_xpath = (
                        f"({self.tableRows_xpath})"
                        f"[{row_index + 1}]"
                    )

                    try:

                        row = self.driver.find_element(
                            By.XPATH,
                            row_xpath
                        )

                        columns = row.find_elements(
                            By.TAG_NAME,
                            "td"
                        )

                        if len(columns) < 2:
                            continue

                        row_email = (
                            columns[1]
                            .text
                            .strip()
                        )

                        print(
                            f"Row {row_index + 1} email: "
                            f"{row_email}"
                        )

                        # =================================================
                        # CUSTOMER FOUND
                        # =================================================

                        if row_email.lower() == email.lower():

                            print(
                                f"\nCustomer found: '{email}'"
                            )

                            print(
                                f"Customer row position: "
                                f"{row_index + 1}"
                            )

                            # ---------------------------------------------
                            # Edit button inside matching row
                            # ---------------------------------------------

                            edit_button_xpath = (
                                f"{row_xpath}"
                                f"//td[last()]//a"
                            )

                            self.wait.until(
                                EC.presence_of_element_located(
                                    (
                                        By.XPATH,
                                        edit_button_xpath
                                    )
                                )
                            )

                            edit_button = self.driver.find_element(
                                By.XPATH,
                                edit_button_xpath
                            )

                            self.driver.execute_script(
                                """
                                arguments[0].scrollIntoView({
                                    block: 'center',
                                    inline: 'nearest'
                                });
                                """,
                                edit_button
                            )

                            self.wait.until(
                                EC.element_to_be_clickable(
                                    (
                                        By.XPATH,
                                        edit_button_xpath
                                    )
                                )
                            )

                            # Re-locate after scrolling/waiting
                            edit_button = self.driver.find_element(
                                By.XPATH,
                                edit_button_xpath
                            )

                            print(
                                "Clicking Edit button..."
                            )

                            try:

                                edit_button.click()

                            except (
                                    StaleElementReferenceException
                            ):

                                print(
                                    "Edit button became stale. "
                                    "Re-locating..."
                                )

                                edit_button = self.wait.until(
                                    EC.element_to_be_clickable(
                                        (
                                            By.XPATH,
                                            edit_button_xpath
                                        )
                                    )
                                )

                                self.driver.execute_script(
                                    "arguments[0].click();",
                                    edit_button
                                )

                            print(
                                f"Edit clicked successfully "
                                f"for '{email}'"
                            )

                            return

                    except StaleElementReferenceException:

                        print(
                            f"Row {row_index + 1} became stale."
                        )

                        print(
                            "Restarting search from the beginning "
                            "of the current page..."
                        )

                        restart_current_page = True
                        break

            except StaleElementReferenceException:

                print(
                    "Customer table became stale while searching."
                )

                restart_current_page = True

            # =========================================================
            # RESTART CURRENT PAGE
            # =========================================================

            if restart_current_page:
                print(
                    f"Refreshing search state for page "
                    f"{page_count}..."
                )

                self.wait.until(
                    lambda driver: (
                            len(
                                driver.find_elements(
                                    By.XPATH,
                                    self.tableRows_xpath
                                )
                            ) > 0
                    )
                )

                continue

            # =========================================================
            # CUSTOMER NOT FOUND ON CURRENT PAGE
            # =========================================================

            print(
                f"Customer '{email}' not found on page "
                f"{page_count}."
            )

            # =========================================================
            # FIND NEXT BUTTON
            # =========================================================

            next_button_xpaths = [

                # Standard nopCommerce/DataTables
                (
                    "//div[@id='customers-grid_wrapper']"
                    "//a[contains(@class,'paginate_button') "
                    "and normalize-space()='Next']"
                ),

                # Generic DataTables
                (
                    "//a[contains(@class,'paginate_button') "
                    "and normalize-space()='Next']"
                ),

                # DataTables <li class="next">
                (
                    "//li[contains(@class,'next')]"
                    "//a[normalize-space()='Next']"
                ),

                # Any visible Next link
                (
                    "//a[normalize-space()='Next']"
                ),

                # Button fallback
                (
                    "//button[normalize-space()='Next']"
                )
            ]

            next_button = None
            next_button_xpath_used = None

            # =========================================================
            # FIND VISIBLE NEXT BUTTON
            # =========================================================

            for next_xpath in next_button_xpaths:

                try:

                    candidates = self.driver.find_elements(
                        By.XPATH,
                        next_xpath
                    )

                    for candidate in candidates:

                        try:

                            if candidate.is_displayed():
                                next_button = candidate
                                next_button_xpath_used = next_xpath

                                print(
                                    "Next button found using locator:"
                                )

                                print(
                                    next_xpath
                                )

                                break

                        except StaleElementReferenceException:

                            continue

                    if next_button is not None:
                        break

                except Exception:

                    continue

            # =========================================================
            # NEXT BUTTON NOT FOUND
            # =========================================================

            if next_button is None:

                print(
                    "\nNext button was not found."
                )

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                print(
                    "Current page:",
                    page_count
                )

                # -----------------------------------------------------
                # DEBUG PAGINATION
                # -----------------------------------------------------

                try:

                    pagination_elements = self.driver.find_elements(
                        By.XPATH,
                        """
                        //div[contains(@class,'dataTables_paginate')]
                        //*[
                            self::a
                            or self::button
                            or self::li
                        ]
                        """
                    )

                    print(
                        "Pagination elements found:",
                        len(pagination_elements)
                    )

                    for element in pagination_elements:

                        try:

                            print(
                                "Pagination text:",
                                repr(element.text),
                                "| class:",
                                element.get_attribute("class"),
                                "| aria-disabled:",
                                element.get_attribute(
                                    "aria-disabled"
                                )
                            )

                        except StaleElementReferenceException:

                            continue

                except Exception as e:

                    print(
                        "Unable to inspect pagination:",
                        e
                    )

                raise AssertionError(
                    f"Customer '{email}' was not found. "
                    f"'Next' button is not available on page "
                    f"{page_count}."
                )

            # =========================================================
            # CHECK NEXT BUTTON STATUS
            # =========================================================

            classes = (
                    next_button.get_attribute("class")
                    or ""
            )

            aria_disabled = (
                    next_button.get_attribute("aria-disabled")
                    or ""
            )

            print(
                "Next button class:",
                classes
            )

            print(
                "Next aria-disabled:",
                aria_disabled
            )

            if (
                    "disabled" in classes.lower()
                    or
                    aria_disabled.lower() == "true"
            ):
                raise AssertionError(
                    f"Customer '{email}' was not found "
                    f"on any customer page."
                )

            # =========================================================
            # CAPTURE CURRENT FIRST ROW EMAIL
            # =========================================================

            old_first_email = ""

            try:

                old_first_row = self.driver.find_element(
                    By.XPATH,
                    f"({self.tableRows_xpath})[1]"
                )

                old_columns = old_first_row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                if len(old_columns) >= 2:
                    old_first_email = (
                        old_columns[1]
                        .text
                        .strip()
                    )

            except (
                    StaleElementReferenceException,
                    NoSuchElementException
            ):

                old_first_email = ""

            print(
                "Current first-row email:",
                old_first_email
            )

            # =========================================================
            # SCROLL TO NEXT
            # =========================================================

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'nearest'
                });
                """,
                next_button
            )

            # =========================================================
            # RELOCATE NEXT
            # =========================================================

            try:

                next_button = self.driver.find_element(
                    By.XPATH,
                    next_button_xpath_used
                )

            except (
                    NoSuchElementException,
                    StaleElementReferenceException
            ):

                next_button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//a[normalize-space()='Next']"
                        )
                    )
                )

            # =========================================================
            # CLICK NEXT
            # =========================================================

            print(
                "Clicking Next..."
            )

            try:

                next_button.click()

            except (
                    StaleElementReferenceException
            ):

                print(
                    "Next button became stale. "
                    "Re-locating and retrying..."
                )

                next_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            next_button_xpath_used
                        )
                    )
                )

                next_button.click()

            print(
                "Next button clicked."
            )

            # =========================================================
            # WAIT FOR DATATABLE PROCESSING
            # =========================================================

            for processing_xpath in processing_xpaths:

                try:

                    processing_element = self.driver.find_element(
                        By.XPATH,
                        processing_xpath
                    )

                    if processing_element.is_displayed():
                        print(
                            "Customer DataTable started processing."
                        )

                        self.wait.until(
                            EC.invisibility_of_element_located(
                                (
                                    By.XPATH,
                                    processing_xpath
                                )
                            )
                        )

                        print(
                            "Customer DataTable processing completed."
                        )

                        break

                except (
                        NoSuchElementException,
                        StaleElementReferenceException
                ):

                    continue

            # =========================================================
            # WAIT FOR TABLE ROWS
            # =========================================================

            self.wait.until(
                lambda driver: (
                        len(
                            driver.find_elements(
                                By.XPATH,
                                self.tableRows_xpath
                            )
                        ) > 0
                )
            )

            # =========================================================
            # WAIT FOR TABLE CONTENT TO CHANGE
            # =========================================================

            if old_first_email:

                try:

                    self.wait.until(
                        lambda driver: (
                                len(
                                    driver.find_elements(
                                        By.XPATH,
                                        self.tableRows_xpath
                                    )
                                ) > 0
                                and
                                len(
                                    driver.find_elements(
                                        By.XPATH,
                                        f"({self.tableRows_xpath})[1]//td"
                                    )
                                ) >= 2
                                and
                                driver.find_element(
                                    By.XPATH,
                                    f"({self.tableRows_xpath})[1]//td[2]"
                                ).text.strip()
                                != old_first_email
                        )
                    )

                    print(
                        "Customer table contents changed."
                    )

                except TimeoutException:

                    print(
                        "First row did not change within "
                        "the expected time."
                    )

                    print(
                        "Continuing with current table contents."
                    )

            # =========================================================
            # PAGE READY
            # =========================================================

            self.waitForCustomerRows()

            print(
                f"Page {page_count + 1} is ready."
            )

        # =========================================================
        # MAX PAGE LIMIT
        # =========================================================

        raise AssertionError(
            f"Unable to find/edit customer with email: "
            f"{email} after checking {max_pages} pages."
        )


    def isCustomerFirstNameUpdated(
            self,
            email,
            expected_first_name
    ):

        print(
            f"\nVerifying customer '{email}' "
            f"has First Name '{expected_first_name}'..."
        )

        for attempt in range(3):

            try:

                # -------------------------------------------------
                # Wait for customer table
                # -------------------------------------------------

                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.table_xpath
                        )
                    )
                )

                # -------------------------------------------------
                # Wait for real customer rows
                # -------------------------------------------------

                self.waitForCustomerRows()

                # -------------------------------------------------
                # Get current rows
                # -------------------------------------------------

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                print(
                    f"Rows available for verification: {len(rows)}"
                )

                # -------------------------------------------------
                # Search customer by email
                # -------------------------------------------------

                for row_index in range(len(rows)):

                    row_xpath = (
                        f"({self.tableRows_xpath})"
                        f"[{row_index + 1}]"
                    )

                    try:

                        row = self.driver.find_element(
                            By.XPATH,
                            row_xpath
                        )

                        cells = row.find_elements(
                            By.TAG_NAME,
                            "td"
                        )

                        if len(cells) < 3:
                            continue

                        # -----------------------------------------
                        # Email = td[2]
                        # -----------------------------------------

                        actual_email = (
                            cells[1]
                            .text
                            .strip()
                        )

                        if actual_email != email:
                            continue

                        # -----------------------------------------
                        # Customer Name = td[3]
                        # -----------------------------------------

                        customer_name = (
                            cells[2]
                            .text
                            .strip()
                        )

                        print(
                            f"Customer found at row "
                            f"{row_index + 1}"
                        )

                        print(
                            "Customer email:",
                            repr(actual_email)
                        )

                        print(
                            "Customer name:",
                            repr(customer_name)
                        )

                        # -----------------------------------------
                        # Extract First Name
                        # -----------------------------------------

                        name_parts = customer_name.split()

                        if not name_parts:
                            print(
                                "Customer name is empty."
                            )

                            return False

                        actual_first_name = name_parts[0]

                        print(
                            "Expected First Name:",
                            repr(expected_first_name)
                        )

                        print(
                            "Actual First Name  :",
                            repr(actual_first_name)
                        )

                        # -----------------------------------------
                        # Verify
                        # -----------------------------------------

                        if actual_first_name == expected_first_name:
                            print(
                                "Customer First Name "
                                "updated successfully."
                            )

                            return True

                        print(
                            "Customer First Name "
                            "was not updated."
                        )

                        return False

                    except StaleElementReferenceException:

                        print(
                            f"Row {row_index + 1} became stale "
                            f"during verification."
                        )

                        raise

                # -------------------------------------------------
                # Customer not found on current page
                # -------------------------------------------------

                print(
                    f"Customer '{email}' was not found "
                    f"on the current page."
                )

                return False

            except StaleElementReferenceException:

                print(
                    f"Customer table became stale. "
                    f"Retrying verification "
                    f"({attempt + 1}/3)..."
                )

                if attempt == 2:
                    raise

                time.sleep(1)

            except TimeoutException:

                print(
                    "Customer table or rows were not available "
                    "for verification."
                )

                if attempt == 2:
                    return False

                time.sleep(1)

        return False

    # ==========================================================
    # VERIFY CUSTOMER NAME AFTER EDIT
    # ==========================================================

    def isCustomerNameUpdated(self, email, expected_name):

        print(
            "\n========== VERIFY CUSTOMER UPDATE =========="
        )

        print(
            f"Searching email   : {email}"
        )

        print(
            f"Expected name     : {expected_name}"
        )

        email = email.strip()

        max_pages = 100
        page_count = 0

        while page_count < max_pages:

            page_count += 1

            print(
                f"\n========== VERIFYING CUSTOMER PAGE "
                f"{page_count} =========="
            )

            # =========================================================
            # WAIT FOR CUSTOMER TABLE
            # =========================================================

            self.waitForTable()

            # =========================================================
            # WAIT FOR DATATABLE PROCESSING
            # =========================================================

            processing_xpaths = [
                "//div[@id='customers-grid_processing']",
                "//div[contains(@class,'dataTables_processing')]"
            ]

            for processing_xpath in processing_xpaths:

                try:

                    processing_element = self.driver.find_element(
                        By.XPATH,
                        processing_xpath
                    )

                    if processing_element.is_displayed():
                        print(
                            "Customer DataTable is processing..."
                        )

                        self.wait.until(
                            EC.invisibility_of_element_located(
                                (
                                    By.XPATH,
                                    processing_xpath
                                )
                            )
                        )

                        print(
                            "Customer DataTable processing completed."
                        )

                        break

                except (
                        NoSuchElementException,
                        StaleElementReferenceException
                ):

                    continue

                except TimeoutException:

                    print(
                        "DataTable processing indicator did not "
                        "disappear within the expected time."
                    )

                    break

            # =========================================================
            # WAIT FOR ROWS
            # =========================================================

            self.wait.until(
                lambda driver: (
                        len(
                            driver.find_elements(
                                By.XPATH,
                                self.tableRows_xpath
                            )
                        ) > 0
                )
            )

            # =========================================================
            # SEARCH CURRENT PAGE
            # =========================================================

            restart_current_page = False

            try:

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                print(
                    f"Rows available on page {page_count}: "
                    f"{len(rows)}"
                )

                for row_index in range(len(rows)):

                    row_xpath = (
                        f"({self.tableRows_xpath})"
                        f"[{row_index + 1}]"
                    )

                    try:

                        row = self.driver.find_element(
                            By.XPATH,
                            row_xpath
                        )

                        cells = row.find_elements(
                            By.TAG_NAME,
                            "td"
                        )

                        if len(cells) < 3:
                            continue

                        actual_email = (
                            cells[1]
                            .text
                            .strip()
                        )

                        actual_name = (
                            cells[2]
                            .text
                            .strip()
                        )

                        print(
                            f"Row {row_index + 1}: "
                            f"{actual_email} | {actual_name}"
                        )

                        # =================================================
                        # CUSTOMER FOUND
                        # =================================================

                        if actual_email.lower() == email.lower():

                            print(
                                f"\nCustomer found: {email}"
                            )

                            print(
                                f"Customer row position: "
                                f"{row_index + 1}"
                            )

                            print(
                                f"Actual name  : {actual_name}"
                            )

                            print(
                                f"Expected name: {expected_name}"
                            )

                            # -------------------------------------------------
                            # VERIFY NAME
                            # -------------------------------------------------

                            if actual_name == expected_name:
                                print(
                                    "Customer name updated successfully."
                                )

                                return True

                            print(
                                "Customer found, but name "
                                "does not match expected value."
                            )

                            return False

                    except StaleElementReferenceException:

                        print(
                            f"Row {row_index + 1} became stale."
                        )

                        restart_current_page = True
                        break

            except StaleElementReferenceException:

                print(
                    "Customer table became stale "
                    "while verifying update."
                )

                restart_current_page = True

            # =========================================================
            # RESTART CURRENT PAGE
            # =========================================================

            if restart_current_page:
                print(
                    f"Retrying customer verification "
                    f"on page {page_count}..."
                )

                self.wait.until(
                    lambda driver: (
                            len(
                                driver.find_elements(
                                    By.XPATH,
                                    self.tableRows_xpath
                                )
                            ) > 0
                    )
                )

                continue

            # =========================================================
            # CUSTOMER NOT FOUND ON CURRENT PAGE
            # =========================================================

            print(
                f"Customer '{email}' was not found "
                f"on page {page_count}."
            )

            # =========================================================
            # FIND NEXT BUTTON
            # =========================================================

            next_button_xpaths = [

                # Standard nopCommerce/DataTables
                (
                    "//div[@id='customers-grid_wrapper']"
                    "//a[contains(@class,'paginate_button') "
                    "and normalize-space()='Next']"
                ),

                # Generic DataTables
                (
                    "//a[contains(@class,'paginate_button') "
                    "and normalize-space()='Next']"
                ),

                # DataTables <li class="next">
                (
                    "//li[contains(@class,'next')]"
                    "//a[normalize-space()='Next']"
                ),

                # Generic Next link
                (
                    "//a[normalize-space()='Next']"
                ),

                # Button fallback
                (
                    "//button[normalize-space()='Next']"
                )
            ]

            next_button = None
            next_button_xpath_used = None

            # =========================================================
            # FIND VISIBLE NEXT BUTTON
            # =========================================================

            for next_xpath in next_button_xpaths:

                try:

                    candidates = self.driver.find_elements(
                        By.XPATH,
                        next_xpath
                    )

                    for candidate in candidates:

                        try:

                            if candidate.is_displayed():
                                next_button = candidate
                                next_button_xpath_used = next_xpath

                                print(
                                    "Next button found using locator:"
                                )

                                print(
                                    next_xpath
                                )

                                break

                        except StaleElementReferenceException:

                            continue

                    if next_button is not None:
                        break

                except Exception:

                    continue

            # =========================================================
            # NEXT BUTTON NOT FOUND
            # =========================================================

            if next_button is None:

                print(
                    "Next button was not found."
                )

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                print(
                    "Current page:",
                    page_count
                )

                # -----------------------------------------------------
                # DEBUG PAGINATION
                # -----------------------------------------------------

                try:

                    pagination_elements = self.driver.find_elements(
                        By.XPATH,
                        """
                        //div[contains(@class,'dataTables_paginate')]
                        //*[
                            self::a
                            or self::button
                            or self::li
                        ]
                        """
                    )

                    print(
                        "Pagination elements found:",
                        len(pagination_elements)
                    )

                    for element in pagination_elements:

                        try:

                            print(
                                "Pagination text:",
                                repr(element.text),
                                "| class:",
                                element.get_attribute(
                                    "class"
                                ),
                                "| aria-disabled:",
                                element.get_attribute(
                                    "aria-disabled"
                                )
                            )

                        except StaleElementReferenceException:

                            continue

                except Exception as e:

                    print(
                        "Unable to inspect pagination:",
                        e
                    )

                raise AssertionError(
                    f"Customer '{email}' was not found "
                    f"after checking page {page_count}. "
                    f"'Next' button is not available."
                )

            # =========================================================
            # CHECK NEXT BUTTON STATUS
            # =========================================================

            classes = (
                    next_button.get_attribute("class")
                    or ""
            )

            aria_disabled = (
                    next_button.get_attribute("aria-disabled")
                    or ""
            )

            print(
                "Next button class:",
                classes
            )

            print(
                "Next aria-disabled:",
                aria_disabled
            )

            if (
                    "disabled" in classes.lower()
                    or
                    aria_disabled.lower() == "true"
            ):
                raise AssertionError(
                    f"Customer '{email}' was not found "
                    f"on any customer page."
                )

            # =========================================================
            # CAPTURE CURRENT FIRST ROW EMAIL
            # =========================================================

            old_first_email = ""

            try:

                first_row = self.driver.find_element(
                    By.XPATH,
                    f"({self.tableRows_xpath})[1]"
                )

                first_columns = first_row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                if len(first_columns) >= 2:
                    old_first_email = (
                        first_columns[1]
                        .text
                        .strip()
                    )

            except (
                    StaleElementReferenceException,
                    NoSuchElementException
            ):

                old_first_email = ""

            print(
                "Current first-row email:",
                old_first_email
            )

            # =========================================================
            # SCROLL TO NEXT
            # =========================================================

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'nearest'
                });
                """,
                next_button
            )

            # =========================================================
            # RELOCATE NEXT
            # =========================================================

            try:

                next_button = self.driver.find_element(
                    By.XPATH,
                    next_button_xpath_used
                )

            except (
                    NoSuchElementException,
                    StaleElementReferenceException
            ):

                next_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//a[normalize-space()='Next']"
                        )
                    )
                )

            # =========================================================
            # CLICK NEXT
            # =========================================================

            print(
                "Clicking Next..."
            )

            try:

                next_button.click()

            except StaleElementReferenceException:

                print(
                    "Next button became stale. "
                    "Re-locating..."
                )

                next_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            next_button_xpath_used
                        )
                    )
                )

                next_button.click()

            print(
                "Next button clicked."
            )

            # =========================================================
            # WAIT FOR DATATABLE PROCESSING
            # =========================================================

            for processing_xpath in processing_xpaths:

                try:

                    processing_element = self.driver.find_element(
                        By.XPATH,
                        processing_xpath
                    )

                    if processing_element.is_displayed():
                        print(
                            "Customer DataTable started processing."
                        )

                        self.wait.until(
                            EC.invisibility_of_element_located(
                                (
                                    By.XPATH,
                                    processing_xpath
                                )
                            )
                        )

                        print(
                            "Customer DataTable processing completed."
                        )

                        break

                except (
                        NoSuchElementException,
                        StaleElementReferenceException
                ):

                    continue

            # =========================================================
            # WAIT FOR ROWS
            # =========================================================

            self.wait.until(
                lambda driver: (
                        len(
                            driver.find_elements(
                                By.XPATH,
                                self.tableRows_xpath
                            )
                        ) > 0
                )
            )

            # =========================================================
            # WAIT FOR PAGE CONTENT TO CHANGE
            # =========================================================

            if old_first_email:

                try:

                    self.wait.until(
                        lambda driver: (
                                len(
                                    driver.find_elements(
                                        By.XPATH,
                                        self.tableRows_xpath
                                    )
                                ) > 0
                                and
                                len(
                                    driver.find_elements(
                                        By.XPATH,
                                        f"({self.tableRows_xpath})[1]//td"
                                    )
                                ) >= 2
                                and
                                driver.find_element(
                                    By.XPATH,
                                    f"({self.tableRows_xpath})[1]//td[2]"
                                ).text.strip()
                                != old_first_email
                        )
                    )

                    print(
                        "Customer table contents changed."
                    )

                except TimeoutException:

                    print(
                        "First row did not change within "
                        "the expected time."
                    )

                    print(
                        "Continuing with current table."
                    )

            # =========================================================
            # PAGE READY
            # =========================================================

            self.waitForCustomerRows()

            print(
                f"Page {page_count + 1} is ready."
            )

        # =========================================================
        # MAX PAGE LIMIT
        # =========================================================

        raise AssertionError(
            f"Unable to verify customer '{email}' "
            f"after checking {max_pages} pages."
        )

    def isCustomerDeleted(self, email):

        print(
            "\n========== VERIFY CUSTOMER DELETED =========="
        )

        print(
            "Searching for deleted email:",
            email
        )

        max_retries = 3

        for attempt in range(1, max_retries + 1):

            try:

                self.waitForTable()

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                print(
                    f"Attempt {attempt}: "
                    f"Found {len(rows)} customer rows"
                )

                for row_index, row in enumerate(
                        rows,
                        start=1
                ):

                    cells = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if len(cells) < 3:
                        continue

                    actual_email = (
                        cells[1].text.strip()
                    )

                    print(
                        f"Row {row_index}: "
                        f"{actual_email}"
                    )

                    if (
                            actual_email.lower()
                            == email.lower()
                    ):
                        print(
                            f"Customer still exists: {email}"
                        )

                        return False

                print(
                    f"Customer '{email}' "
                    f"is not present in the grid."
                )

                print(
                    "Customer deletion verified successfully."
                )

                return True

            except StaleElementReferenceException:

                print(
                    f"Attempt {attempt}: "
                    "Stale element detected. Retrying..."
                )

                if attempt < max_retries:
                    time.sleep(1)
                    continue

                return False

            except TimeoutException:

                print(
                    f"Attempt {attempt}: "
                    "Timeout while verifying deletion."
                )

                if attempt < max_retries:
                    time.sleep(1)
                    continue

                return False

            except Exception as e:

                print(
                    "Unexpected error while verifying "
                    f"customer deletion: {e}"
                )

                return False

        return False





