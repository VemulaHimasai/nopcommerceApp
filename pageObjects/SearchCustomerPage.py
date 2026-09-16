
import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
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

            # =================================================
            # WAIT FOR TABLE
            # =================================================

            self.waitForTable()

            # =================================================
            # WAIT FOR DATATABLES PROCESSING TO FINISH
            # =================================================

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

            # =================================================
            # WAIT FOR CUSTOMER ROWS
            # =================================================

            try:

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

            except TimeoutException:

                raise AssertionError(
                    f"No customer rows available on page "
                    f"{page_count} while searching for '{email}'."
                )

            # =================================================
            # WAIT FOR TABLE TO STABILIZE
            # =================================================

            try:

                previous_row_count = 0

                def rows_stable(driver):

                    nonlocal previous_row_count

                    current_rows = driver.find_elements(
                        By.XPATH,
                        self.tableRows_xpath
                    )

                    current_row_count = len(current_rows)

                    print(
                        f"Current customer row count: "
                        f"{current_row_count}"
                    )

                    if current_row_count == 0:
                        previous_row_count = 0
                        return False

                    if current_row_count == previous_row_count:
                        return True

                    previous_row_count = current_row_count
                    return False

                self.wait.until(rows_stable)

            except TimeoutException:

                print(
                    "Customer table did not stabilize within "
                    "the expected time. Continuing search..."
                )

            # =================================================
            # SEARCH CURRENT PAGE
            # =================================================

            restart_current_page = False

            try:

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                print(
                    f"Rows found on current page: {len(rows)}"
                )

                # =================================================
                # DEBUG CURRENT ROWS
                # =================================================

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

                # =================================================
                # SEARCH EACH ROW
                # =================================================

                for row_index in range(len(rows)):

                    row_xpath = (
                        f"({self.tableRows_xpath})"
                        f"[{row_index + 1}]"
                    )

                    try:

                        # -------------------------------------------------
                        # Re-locate exact row
                        # -------------------------------------------------

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

                        row_email = columns[1].text.strip()

                        print(
                            f"Row {row_index + 1} email: "
                            f"{row_email}"
                        )

                        # =================================================
                        # CUSTOMER FOUND
                        # =================================================

                        if row_email == email:
                            print(
                                f"\nCustomer found: '{email}'"
                            )

                            print(
                                f"Customer row position: "
                                f"{row_index + 1}"
                            )

                            # -------------------------------------------------
                            # Exact Edit button inside matching row
                            # -------------------------------------------------

                            edit_button_xpath = (
                                f"{row_xpath}"
                                f"//td[last()]//a"
                            )

                            # -------------------------------------------------
                            # Wait for Edit button
                            # -------------------------------------------------

                            self.wait.until(
                                EC.presence_of_element_located(
                                    (
                                        By.XPATH,
                                        edit_button_xpath
                                    )
                                )
                            )

                            # -------------------------------------------------
                            # Scroll to Edit button
                            # -------------------------------------------------

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

                            # -------------------------------------------------
                            # Wait until clickable
                            # -------------------------------------------------

                            self.wait.until(
                                EC.element_to_be_clickable(
                                    (
                                        By.XPATH,
                                        edit_button_xpath
                                    )
                                )
                            )

                            # -------------------------------------------------
                            # Final re-location
                            # -------------------------------------------------

                            edit_button = self.driver.find_element(
                                By.XPATH,
                                edit_button_xpath
                            )

                            print(
                                "Clicking Edit button..."
                            )

                            # -------------------------------------------------
                            # JavaScript click
                            # -------------------------------------------------

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
                            "of the CURRENT page..."
                        )

                        restart_current_page = True
                        break

            except StaleElementReferenceException:

                print(
                    "Customer table became stale while searching."
                )

                restart_current_page = True

            # =================================================
            # RESTART CURRENT PAGE AFTER STALE ELEMENT
            # =================================================

            if restart_current_page:

                time.sleep(0.5)

                try:

                    self.wait.until(
                        lambda driver: len(
                            driver.find_elements(
                                By.XPATH,
                                self.tableRows_xpath
                            )
                        ) > 0
                    )

                except TimeoutException:

                    raise AssertionError(
                        f"Customer table did not recover on "
                        f"page {page_count}."
                    )

                print(
                    f"Current page {page_count} refreshed. "
                    f"Searching again..."
                )

                continue

            # =================================================
            # CUSTOMER NOT FOUND ON CURRENT PAGE
            # =================================================

            print(
                f"Customer '{email}' not found on page "
                f"{page_count}."
            )

            # =================================================
            # NEXT BUTTON
            # =================================================

            next_button_xpath = (
                "//div[@id='customers-grid_wrapper']"
                "//a[contains(@class,'paginate_button') "
                "and normalize-space()='Next']"
            )

            try:

                next_button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            next_button_xpath
                        )
                    )
                )

            except TimeoutException:

                raise AssertionError(
                    f"Customer '{email}' was not found. "
                    f"'Next' button is not available."
                )

            # =================================================
            # CHECK NEXT BUTTON STATUS
            # =================================================

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
                    "disabled" in classes
                    or
                    aria_disabled.lower() == "true"
            ):
                raise AssertionError(
                    f"Customer '{email}' was not found "
                    f"on any customer page."
                )

            # =================================================
            # CAPTURE CURRENT FIRST ROW EMAIL
            # =================================================

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
                    TimeoutException
            ):

                old_first_email = ""

            print(
                "Current first-row email:",
                old_first_email
            )

            # =================================================
            # CLICK NEXT
            # =================================================

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'nearest'
                });
                """,
                next_button
            )

            # Re-locate Next
            next_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        next_button_xpath
                    )
                )
            )

            print(
                "Clicking Next..."
            )

            self.driver.execute_script(
                "arguments[0].click();",
                next_button
            )

            print(
                "Next button clicked."
            )

            # =================================================
            # WAIT FOR NEXT PAGE CONTENT
            # =================================================

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
                        "Checking the current table anyway..."
                    )

            # =================================================
            # WAIT FOR NEW PAGE ROWS
            # =================================================

            self.wait.until(
                lambda driver: len(
                    driver.find_elements(
                        By.XPATH,
                        self.tableRows_xpath
                    )
                ) > 0
            )

            print(
                f"Page {page_count + 1} is ready."
            )

        # =================================================
        # MAX PAGE LIMIT
        # =================================================

        raise AssertionError(
            f"Unable to find/edit customer with email: {email} "
            f"after checking {max_pages} pages."
        )