
import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException
)
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

    # Search Button
    btnSearch_id = "search-customers"

    # Customer Table
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

    # Checkboxes
    checkboxes_xpath = (
        "//table[@id='customers-grid']//tbody/tr/td[1]"
        "//input[@type='checkbox']"
    )

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    # Export dropdown button
    btnExport_drp_xpath = (
        "//button[contains(@class,'btn-success') "
        "and contains(@class,'dropdown-toggle')]"
    )

    # Export Selected XML
    exportSelected_xml_xpath = (
        "//button[@id='exportxml-selected']"
    )

    # Export All XML
    exportAll_xml_xpath = (
        "//button[@type='submit' "
        "and @name='exportxml-all' "
        "and @formaction='/Admin/Customer/ExportXML']"
    )

    # Export Selected Excel
    exportSelected_excel_xpath = (
        "//button[@id='exportexcel-selected']"
    )

    # Export All Excel
    exportAll_excel_xpath = (
        "//button[@type='submit' "
        "and @name='exportexcel-all' "
        "and @formaction='/Admin/Customer/ExportExcel']"
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
    # EMAIL
    # =================================================
    def setEmail(self, email):

        email = str(email).strip()

        if not email:
            raise ValueError(
                "Customer email cannot be empty."
            )

        print(
            f"Setting customer email: {email}"
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Setting customer email "
                    f"(attempt {attempt}/3): {email}"
                )

                # -------------------------------------------------
                # Wait for Email field
                # -------------------------------------------------

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.txtEmail_id
                        )
                    )
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
                    element
                )

                # -------------------------------------------------
                # Re-locate after scrolling
                # -------------------------------------------------

                element = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            self.txtEmail_id
                        )
                    )
                )

                # -------------------------------------------------
                # Clear and enter email
                # -------------------------------------------------

                element.click()
                element.clear()
                element.send_keys(email)

                # -------------------------------------------------
                # Verify value using explicit wait
                #
                # IMPORTANT:
                # Do not use immediate find_element() here.
                # The page can re-render the search form.
                # -------------------------------------------------

                def email_value_matches(driver):

                    try:

                        elements = driver.find_elements(
                            By.ID,
                            self.txtEmail_id
                        )

                        for field in elements:

                            try:

                                if not field.is_displayed():
                                    continue

                                value = (
                                        field.get_attribute("value")
                                        or ""
                                ).strip()

                                if value == email:
                                    return True

                            except StaleElementReferenceException:
                                continue

                        return False

                    except (
                            StaleElementReferenceException,
                            NoSuchElementException
                    ):

                        return False

                self.wait.until(
                    email_value_matches
                )

                # -------------------------------------------------
                # Get the final value after the wait
                # -------------------------------------------------

                actual_value = self.wait.until(
                    lambda driver: (
                            (
                                    driver.find_element(
                                        By.ID,
                                        self.txtEmail_id
                                    ).get_attribute("value")
                                    or ""
                            ).strip()
                            or False
                    )
                )

                print(
                    "Expected Email:",
                    repr(email)
                )

                print(
                    "Actual Email  :",
                    repr(actual_value)
                )

                if actual_value == email:
                    print(
                        "Customer email entered successfully."
                    )

                    return

                print(
                    "Email value did not match expected value."
                )

            except (
                    StaleElementReferenceException,
                    TimeoutException,
                    NoSuchElementException
            ) as exc:

                print(
                    f"Unable to set customer email "
                    f"on attempt {attempt}/3: {exc}"
                )

                if attempt < 3:
                    time.sleep(0.5)
                    continue

                # -------------------------------------------------
                # Diagnostics
                # -------------------------------------------------

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                print(
                    "Current Title:",
                    self.driver.title
                )

                try:

                    count = self.driver.execute_script(
                        """
                        return document.querySelectorAll(
                            '#SearchEmail'
                        ).length;
                        """
                    )

                    print(
                        "SearchEmail element count:",
                        count
                    )

                except Exception as debug_error:

                    print(
                        "Unable to check SearchEmail:",
                        debug_error
                    )

                raise

        raise AssertionError(
            f"Unable to enter customer email: {email}"
        )

    # =================================================
    # FIRST NAME
    # =================================================
    def setFirstName(self, first_name):

        for attempt in range(1, 4):

            try:

                print(
                    f"Setting first name "
                    f"(attempt {attempt}/3): {first_name}"
                )

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.txtFirstName_id
                        )
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    element
                )

                self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            self.txtFirstName_id
                        )
                    )
                )

                element = self.driver.find_element(
                    By.ID,
                    self.txtFirstName_id
                )

                element.clear()
                element.send_keys(first_name)

                actual_value = element.get_attribute(
                    "value"
                )

                if actual_value == first_name:

                    print(
                        "First name entered successfully."
                    )

                    return

                print(
                    "First name verification failed."
                )

            except (
                StaleElementReferenceException,
                TimeoutException
            ) as exc:

                print(
                    f"Unable to set first name on attempt "
                    f"{attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            f"Unable to set first name: {first_name}"
        )

    # =================================================
    # CLEAR FIRST NAME
    # =================================================
    def clearFirstName(self):

        for attempt in range(1, 4):

            try:

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.txtFirstName_id
                        )
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    element
                )

                element = self.driver.find_element(
                    By.ID,
                    self.txtFirstName_id
                )

                element.clear()

                print(
                    "First name field cleared."
                )

                return

            except (
                StaleElementReferenceException,
                TimeoutException
            ) as exc:

                print(
                    f"Unable to clear first name "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            "Unable to clear first name field."
        )

    # =================================================
    # LAST NAME
    # =================================================
    def setLastName(self, last_name):

        for attempt in range(1, 4):

            try:

                print(
                    f"Setting last name "
                    f"(attempt {attempt}/3): {last_name}"
                )

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.txtLastName_id
                        )
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    element
                )

                self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            self.txtLastName_id
                        )
                    )
                )

                element = self.driver.find_element(
                    By.ID,
                    self.txtLastName_id
                )

                element.clear()
                element.send_keys(last_name)

                actual_value = element.get_attribute(
                    "value"
                )

                if actual_value == last_name:

                    print(
                        "Last name entered successfully."
                    )

                    return

                print(
                    "Last name verification failed."
                )

            except (
                StaleElementReferenceException,
                TimeoutException
            ) as exc:

                print(
                    f"Unable to set last name on attempt "
                    f"{attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            f"Unable to set last name: {last_name}"
        )

    # =================================================
    # SEARCH
    # =================================================
    def clickSearch(self):

        for attempt in range(1, 4):

            try:

                print(
                    f"Clicking Search button "
                    f"(attempt {attempt}/3)"
                )

                button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.ID,
                            self.btnSearch_id
                        )
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    button
                )

                button = self.driver.find_element(
                    By.ID,
                    self.btnSearch_id
                )

                try:

                    button.click()

                except StaleElementReferenceException:

                    button = self.wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.ID,
                                self.btnSearch_id
                            )
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        button
                    )

                self.waitForTable()

                print(
                    "Search button clicked successfully."
                )

                return

            except (
                StaleElementReferenceException,
                TimeoutException
            ) as exc:

                print(
                    f"Search click failed on attempt "
                    f"{attempt}: {exc}"
                )

                if attempt < 3:
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
                (
                    By.XPATH,
                    self.table_xpath
                )
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            table
        )

    # =================================================
    # WAIT FOR TABLE
    # =================================================
    def waitForTable(self):

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.table_xpath
                )
            )
        )

    # =================================================
    # WAIT FOR CUSTOMER ROWS
    # =================================================
    def waitForCustomerRows(self):

        def rows_available(driver):

            try:

                rows = driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                if not rows:
                    return False

                for row in rows:

                    try:

                        columns = row.find_elements(
                            By.TAG_NAME,
                            "td"
                        )

                        if len(columns) < 2:
                            continue

                        email = (
                            columns[1]
                            .text
                            .strip()
                        )

                        if not email:
                            continue

                        if email.lower() == "loading...":
                            continue

                        return True

                    except StaleElementReferenceException:

                        continue

                return False

            except StaleElementReferenceException:

                return False

        self.wait.until(rows_available)

    # =================================================
    # GET ROW COUNT
    # =================================================
    def getNoOfRows(self):

        return len(
            self.driver.find_elements(
                By.XPATH,
                self.tableRows_xpath
            )
        )

    # =================================================
    # GET COLUMN COUNT
    # =================================================
    def getNoOfColumns(self):

        rows = self.driver.find_elements(
            By.XPATH,
            self.tableRows_xpath
        )

        if not rows:
            return 0

        return len(
            rows[0].find_elements(
                By.TAG_NAME,
                "td"
            )
        )

    # =================================================
    # GET TABLE DATA
    # =================================================
    def getTableData(self):

        data = []

        rows = self.driver.find_elements(
            By.XPATH,
            self.tableRows_xpath
        )

        for row in rows:

            try:

                columns = row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                row_data = [
                    column.text.strip()
                    for column in columns
                ]

                if (
                    len(row_data) >= 2
                    and row_data[1].strip().lower()
                    == "loading..."
                ):
                    continue

                data.append(row_data)

            except StaleElementReferenceException:

                continue

        return data

    # =================================================
    # GET CUSTOMER NAMES
    # =================================================
    def getCustomerNames(self):

        names = []

        rows = self.driver.find_elements(
            By.XPATH,
            self.tableRows_xpath
        )

        for row in rows:

            try:

                columns = row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                if len(columns) >= 4:

                    email = (
                        columns[1]
                        .text
                        .strip()
                    )

                    if (
                        not email
                        or email.lower() == "loading..."
                    ):
                        continue

                    names.append(
                        columns[2].text.strip()
                    )

            except StaleElementReferenceException:

                continue

        return names

    # =================================================
    # SEARCH CUSTOMER BY EMAIL
    # =================================================
    def searchCustomerByEmail(self, email):

        print(
            f"Checking search results for customer email: {email}"
        )

        customer_rows_xpath = (
            "//table[@id='customers-grid']//tbody/tr"
        )

        try:

            self.waitForCustomerRows()

            rows = self.driver.find_elements(
                By.XPATH,
                customer_rows_xpath
            )

            print(
                f"Customer rows found: {len(rows)}"
            )

            for row in rows:

                try:

                    row_text = row.text.strip()

                    print(
                        "Checking customer row:",
                        repr(row_text)
                    )

                    if email.lower() in row_text.lower():
                        print(
                            f"Customer found with email: {email}"
                        )

                        return True

                except StaleElementReferenceException:

                    print(
                        "Customer row became stale. "
                        "Skipping row..."
                    )

                    continue

            print(
                f"Customer with email '{email}' "
                "was not found in the current results."
            )

            return False

        except TimeoutException:

            print(
                "Customer search results did not load "
                "within the expected time."
            )

            return False
    # =================================================
    # SEARCH CUSTOMER BY NAME
    # =================================================
    def searchCustomerByName(self, full_name):

        print(
            f"Checking search results for customer name: {full_name}"
        )

        customer_rows_xpath = (
            "//table[@id='customers-grid']//tbody/tr"
        )

        try:

            self.waitForCustomerRows()

            rows = self.driver.find_elements(
                By.XPATH,
                customer_rows_xpath
            )

            print(
                f"Customer rows found: {len(rows)}"
            )

            for row in rows:

                try:

                    row_text = row.text.strip()

                    print(
                        "Checking customer row:",
                        repr(row_text)
                    )

                    if full_name.lower() in row_text.lower():
                        print(
                            f"Customer found with name: {full_name}"
                        )

                        return True

                except StaleElementReferenceException:

                    print(
                        "Customer row became stale. "
                        "Skipping row..."
                    )

                    continue

            print(
                f"Customer with name '{full_name}' "
                "was not found in the current results."
            )

            return False

        except TimeoutException:

            print(
                "Customer search results did not load "
                "within the expected time."
            )

            return False
    # =================================================
    # GET CHECKBOXES
    # =================================================
    def getCustomerCheckBoxes(self):

        return self.driver.find_elements(
            By.XPATH,
            self.checkboxes_xpath
        )

    # =================================================
    # SELECT CHECKBOX
    # =================================================
    def selectCustomerCheckBox(self, index):

        checkboxes = self.getCustomerCheckBoxes()

        if index < 0 or index >= len(checkboxes):

            raise IndexError(
                f"Customer checkbox index {index} "
                f"is out of range."
            )

        checkbox = checkboxes[index]

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            checkbox
        )

        if not checkbox.is_selected():

            self.driver.execute_script(
                "arguments[0].click();",
                checkbox
            )

    # =================================================
    # CLICK EXPORT DROPDOWN
    # =================================================
    def clickExport(self):

        """
        Opens the Export dropdown.

        The actual export option is selected by:
            clickExportAll_Excel()
            clickExportAll_XML()
            clickExportSelected_Excel()
            clickExportSelected_XML()
        """

        for attempt in range(1, 4):

            try:

                print(
                    f"Opening Export dropdown "
                    f"(attempt {attempt}/3)..."
                )

                dropdown = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.btnExport_drp_xpath
                        )
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    dropdown
                )

                dropdown = self.driver.find_element(
                    By.XPATH,
                    self.btnExport_drp_xpath
                )

                try:

                    dropdown.click()

                except StaleElementReferenceException:

                    dropdown = self.wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                self.btnExport_drp_xpath
                            )
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        dropdown
                    )

                print(
                    "Export dropdown opened successfully."
                )

                return

            except (
                StaleElementReferenceException,
                TimeoutException
            ) as exc:

                print(
                    f"Export dropdown attempt "
                    f"{attempt} failed: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            "Unable to open Export dropdown "
            "after 3 attempts."
        )

    # =================================================
    # EXPORT WRAPPERS
    # =================================================
    def clickExportSelected_XML(self):

        print(
            "Clicking Export Selected XML..."
        )

        self.exportSelectedXML()

        print(
            "Export Selected XML clicked successfully."
        )

    def clickExportAll_XML(self):

        print(
            "Clicking Export All XML..."
        )

        self.exportAllXML()

        print(
            "Export All XML clicked successfully."
        )

    def clickExportSelected_Excel(self):

        print(
            "Clicking Export Selected Excel..."
        )

        self.exportSelectedExcel()

        print(
            "Export Selected Excel clicked successfully."
        )

    def clickExportAll_Excel(self):

        print(
            "Clicking Export All Excel..."
        )

        self.exportAllExcel()

        print(
            "Export All Excel clicked successfully."
        )

    # =================================================
    # EXPORT SELECTED XML
    # =================================================
    def exportSelectedXML(self):

        print(
            "Clicking Export Selected XML..."
        )

        export_xpath = (
            "//button[@id='exportxml-selected']"
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Export Selected XML click attempt "
                    f"{attempt}/3..."
                )

                button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            export_xpath
                        )
                    )
                )

                print(
                    "Export Selected XML button found."
                )

                print(
                    "Displayed:",
                    button.is_displayed()
                )

                print(
                    "Enabled:",
                    button.is_enabled()
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                print(
                    "Export Selected XML clicked successfully."
                )

                return

            except StaleElementReferenceException:

                print(
                    "Export Selected XML button became "
                    "stale. Retrying..."
                )

                continue

            except TimeoutException:

                print(
                    "Export Selected XML button was not "
                    "found within the wait time."
                )

                raise

        raise TimeoutException(
            "Unable to click Export Selected XML "
            "after 3 attempts."
        )

    # =================================================
    # EXPORT ALL XML
    # =================================================
    def exportAllXML(self):

        print(
            "Clicking Export All XML..."
        )

        export_xpath = (
            "//button[@type='submit' "
            "and @name='exportxml-all' "
            "and @formaction='/Admin/Customer/ExportXML']"
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Export All XML click attempt "
                    f"{attempt}/3..."
                )

                button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            export_xpath
                        )
                    )
                )

                print(
                    "Export All XML button found."
                )

                print(
                    "Displayed:",
                    button.is_displayed()
                )

                print(
                    "Enabled:",
                    button.is_enabled()
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                print(
                    "Export All XML clicked successfully."
                )

                return

            except StaleElementReferenceException:

                print(
                    "Export All XML button became stale. "
                    "Retrying..."
                )

                continue

            except TimeoutException:

                print(
                    "Export All XML button was not found "
                    "within the wait time."
                )

                raise

        raise TimeoutException(
            "Unable to click Export All XML "
            "after 3 attempts."
        )

    # =================================================
    # EXPORT SELECTED EXCEL
    # =================================================
    def exportSelectedExcel(self):

        print(
            "Clicking Export Selected Excel..."
        )

        export_xpath = (
            "//button[@id='exportexcel-selected']"
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Export Selected Excel click attempt "
                    f"{attempt}/3..."
                )

                button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            export_xpath
                        )
                    )
                )

                print(
                    "Export Selected Excel button found."
                )

                print(
                    "Displayed:",
                    button.is_displayed()
                )

                print(
                    "Enabled:",
                    button.is_enabled()
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                print(
                    "Export Selected Excel clicked successfully."
                )

                return

            except StaleElementReferenceException:

                print(
                    "Export Selected Excel button became "
                    "stale. Retrying..."
                )

                continue

            except TimeoutException:

                print(
                    "Export Selected Excel button was not "
                    "found within the wait time."
                )

                raise

        raise TimeoutException(
            "Unable to click Export Selected Excel "
            "after 3 attempts."
        )

    # =================================================
    # EXPORT ALL EXCEL
    # =================================================
    def exportAllExcel(self):

        print(
            "Clicking Export All Excel..."
        )

        export_xpath = (
            "//button[@type='submit' "
            "and @name='exportexcel-all' "
            "and @formaction='/Admin/Customer/ExportExcel']"
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Export All Excel click attempt "
                    f"{attempt}/3..."
                )

                button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            export_xpath
                        )
                    )
                )

                print(
                    "Export All Excel button found."
                )

                print(
                    "Displayed:",
                    button.is_displayed()
                )

                print(
                    "Enabled:",
                    button.is_enabled()
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });
                    """,
                    button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                print(
                    "Export All Excel clicked successfully."
                )

                return

            except StaleElementReferenceException:

                print(
                    "Export All Excel button became "
                    "stale. Retrying..."
                )

                continue

            except TimeoutException:

                print(
                    "Export All Excel button was not "
                    "found within the wait time."
                )

                raise

        raise TimeoutException(
            "Unable to click Export All Excel "
            "after 3 attempts."
        )

    # =================================================
    # EDIT CUSTOMER BY INDEX
    # =================================================
    def clickEditCustomer(self, index):

        rows = self.driver.find_elements(
            By.XPATH,
            self.tableRows_xpath
        )

        if index < 0 or index >= len(rows):

            raise IndexError(
                f"Customer row index {index} "
                f"is out of range."
            )

        row_xpath = (
            f"({self.tableRows_xpath})"
            f"[{index + 1}]"
        )

        edit_button_xpath = (
            f"{row_xpath}//td[last()]//a"
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
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            edit_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            edit_button
        )

    # =================================================
    # GET NEXT PAGINATION BUTTON
    # =================================================
    def _getNextPaginationButton(self):

        next_locators = [

            (
                By.CSS_SELECTOR,
                "#customers-grid_wrapper "
                "li.paginate_button.next a"
            ),

            (
                By.CSS_SELECTOR,
                "#customers-grid_wrapper "
                ".paginate_button.next"
            ),

            (
                By.CSS_SELECTOR,
                ".dataTables_paginate "
                "li.paginate_button.next a"
            ),

            (
                By.CSS_SELECTOR,
                ".dataTables_paginate "
                ".paginate_button.next"
            ),

            (
                By.XPATH,
                "//*[@aria-label='Next']"
            ),

            (
                By.XPATH,
                "//*[@title='Next']"
            ),

            (
                By.XPATH,
                "//a[contains(@class,'paginate_button') "
                "and normalize-space()='Next']"
            ),

            (
                By.XPATH,
                "//button[contains(@class,'paginate_button') "
                "and normalize-space()='Next']"
            ),

            (
                By.XPATH,
                "//*[contains(@class,'pagination')]"
                "//*[self::a or self::button]"
                "[normalize-space()='Next']"
            )
        ]

        for by, locator in next_locators:

            try:

                elements = self.driver.find_elements(
                    by,
                    locator
                )

                for element in elements:

                    try:

                        if not element.is_displayed():
                            continue

                        tag_name = (
                            element.tag_name.lower()
                        )

                        if tag_name == "li":

                            links = element.find_elements(
                                By.TAG_NAME,
                                "a"
                            )

                            for link in links:

                                try:

                                    if link.is_displayed():

                                        return (
                                            link,
                                            by,
                                            locator
                                        )

                                except StaleElementReferenceException:

                                    continue

                        return (
                            element,
                            by,
                            locator
                        )

                    except StaleElementReferenceException:

                        continue

            except (
                NoSuchElementException,
                StaleElementReferenceException
            ):

                continue

        return None, None, None

    # =================================================
    # CHECK NEXT BUTTON DISABLED
    # =================================================
    def _isNextPaginationDisabled(self, element):

        if element is None:
            return True

        try:

            result = self.driver.execute_script(
                """
                const element = arguments[0];

                if (!element) {
                    return true;
                }

                let current = element;

                for (
                    let i = 0;
                    i < 4 && current;
                    i++,
                    current = current.parentElement
                ) {

                    const className =
                        String(current.className || '');

                    const ariaDisabled =
                        current.getAttribute(
                            'aria-disabled'
                        );

                    const disabled =
                        current.getAttribute(
                            'disabled'
                        );

                    const classes =
                        className.split(/\\s+/);

                    if (
                        classes.includes('disabled') ||
                        ariaDisabled === 'true' ||
                        disabled !== null
                    ) {
                        return true;
                    }
                }

                return false;
                """,
                element
            )

            return bool(result)

        except StaleElementReferenceException:

            return True

        except Exception as exc:

            print(
                "Unable to determine Next button "
                f"disabled state: {exc}"
            )

            return False

    # =================================================
    # DEBUG PAGINATION
    # =================================================
    def _debugPagination(self):

        print(
            "\n========== PAGINATION DEBUG =========="
        )

        containers = [

            (
                "customers wrapper pagination",
                By.CSS_SELECTOR,
                "#customers-grid_wrapper .dataTables_paginate"
            ),

            (
                "global DataTables pagination",
                By.CSS_SELECTOR,
                ".dataTables_paginate"
            ),

            (
                "pagination class",
                By.CSS_SELECTOR,
                ".pagination"
            ),

            (
                "paginate button",
                By.CSS_SELECTOR,
                ".paginate_button"
            )
        ]

        total_found = 0

        for name, by, locator in containers:

            try:

                elements = self.driver.find_elements(
                    by,
                    locator
                )

                print(
                    f"{name}: {len(elements)}"
                )

                total_found += len(elements)

                for index, element in enumerate(
                    elements[:10],
                    start=1
                ):

                    try:

                        print(
                            f"  {index}. "
                            f"tag={element.tag_name}, "
                            f"text={element.text.strip()!r}, "
                            f"class={element.get_attribute('class')!r}"
                        )

                    except StaleElementReferenceException:

                        print(
                            f"  {index}. stale"
                        )

            except Exception as exc:

                print(
                    f"{name}: ERROR - {exc}"
                )

        print(
            f"Total pagination-related elements found: "
            f"{total_found}"
        )

        try:

            pagination_debug = self.driver.execute_script(
                """
                return {
                    url: window.location.href,

                    tables:
                        Array.from(
                            document.querySelectorAll('table')
                        ).map(function(table) {
                            return {
                                id: table.id,
                                classes: table.className
                            };
                        }),

                    pagination:
                        Array.from(
                            document.querySelectorAll(
                                '.dataTables_paginate, '
                                '.paginate_button, '
                                '.pagination'
                            )
                        ).map(function(element) {
                            return {
                                tag: element.tagName,
                                text: (
                                    element.innerText || ''
                                ).trim(),
                                id: element.id,
                                classes: element.className,
                                ariaDisabled:
                                    element.getAttribute(
                                        'aria-disabled'
                                    ),
                                title:
                                    element.getAttribute(
                                        'title'
                                    ),
                                ariaLabel:
                                    element.getAttribute(
                                        'aria-label'
                                    )
                            };
                        })
                };
                """
            )

            print(
                "JavaScript pagination debug:"
            )

            print(
                pagination_debug
            )

        except Exception as exc:

            print(
                "JavaScript pagination debug failed:",
                exc
            )

        print(
            "========================================"
        )

    # =================================================
    # GET CURRENT PAGE NUMBER
    # =================================================
    def _getCurrentPageNumber(self):

        locators = [

            (
                By.CSS_SELECTOR,
                "#customers-grid_wrapper "
                ".dataTables_paginate "
                ".paginate_button.current"
            ),

            (
                By.CSS_SELECTOR,
                ".dataTables_paginate "
                ".paginate_button.current"
            )
        ]

        for by, locator in locators:

            try:

                elements = self.driver.find_elements(
                    by,
                    locator
                )

                for element in elements:

                    try:

                        if element.is_displayed():

                            value = (
                                element.text
                                .strip()
                            )

                            if value:
                                return value

                    except StaleElementReferenceException:

                        continue

            except Exception:

                continue

        return ""

    # =================================================
    # CLICK NEXT PAGE
    # =================================================
    def _clickNextPage(self):

        next_button, next_by, next_locator = (
            self._getNextPaginationButton()
        )

        if next_button is None:

            print(
                "\nNext pagination control was not found."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            self._debugPagination()

            return False

        if self._isNextPaginationDisabled(
            next_button
        ):

            print(
                "Next pagination control is disabled."
            )

            return False

        old_page_number = (
            self._getCurrentPageNumber()
        )

        old_first_email = ""

        try:

            first_row = self.driver.find_element(
                By.XPATH,
                f"({self.tableRows_xpath})[1]"
            )

            columns = first_row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(columns) >= 2:

                old_first_email = (
                    columns[1]
                    .text
                    .strip()
                )

        except (
            NoSuchElementException,
            StaleElementReferenceException
        ):

            pass

        print(
            "Current page:",
            old_page_number or "unknown"
        )

        print(
            "Current first-row email:",
            old_first_email or "unknown"
        )

        try:

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'nearest'
                });
                """,
                next_button
            )

        except StaleElementReferenceException:

            print(
                "Next button became stale before click. "
                "Re-locating..."
            )

            next_button, next_by, next_locator = (
                self._getNextPaginationButton()
            )

            if next_button is None:
                return False

        try:

            next_button = self.driver.find_element(
                next_by,
                next_locator
            )

        except (
            NoSuchElementException,
            StaleElementReferenceException
        ):

            next_button, next_by, next_locator = (
                self._getNextPaginationButton()
            )

            if next_button is None:

                print(
                    "Unable to re-locate Next button."
                )

                return False

        print(
            "Clicking Next pagination button..."
        )

        try:

            next_button.click()

        except (
            StaleElementReferenceException,
            TimeoutException
        ):

            print(
                "Normal Next click failed. "
                "Using JavaScript click..."
            )

            next_button, next_by, next_locator = (
                self._getNextPaginationButton()
            )

            if next_button is None:
                return False

            self.driver.execute_script(
                "arguments[0].click();",
                next_button
            )

        processing_locators = [

            (
                By.ID,
                "customers-grid_processing"
            ),

            (
                By.CSS_SELECTOR,
                "#customers-grid_wrapper "
                ".dataTables_processing"
            ),

            (
                By.CSS_SELECTOR,
                ".dataTables_processing"
            )
        ]

        for by, locator in processing_locators:

            try:

                elements = self.driver.find_elements(
                    by,
                    locator
                )

                if not elements:
                    continue

                processing_element = elements[0]

                if processing_element.is_displayed():

                    print(
                        "Waiting for customer DataTable "
                        "processing to complete..."
                    )

                    try:

                        self.wait.until(
                            EC.invisibility_of_element_located(
                                (
                                    by,
                                    locator
                                )
                            )
                        )

                    except TimeoutException:

                        print(
                            "Processing indicator remained "
                            "visible."
                        )

                break

            except (
                NoSuchElementException,
                StaleElementReferenceException
            ):

                continue

        try:

            self.waitForCustomerRows()

        except TimeoutException:

            print(
                "Real customer rows were not available "
                "after clicking Next."
            )

            return False

        def page_changed(driver):

            try:

                new_page_number = (
                    self._getCurrentPageNumber()
                )

                if (
                    old_page_number
                    and new_page_number
                    and new_page_number != old_page_number
                ):

                    return True

                if old_first_email:

                    first_row = driver.find_element(
                        By.XPATH,
                        f"({self.tableRows_xpath})[1]"
                    )

                    columns = first_row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if len(columns) >= 2:

                        new_first_email = (
                            columns[1]
                            .text
                            .strip()
                        )

                        if (
                            new_first_email
                            and
                            new_first_email != old_first_email
                        ):

                            return True

                return False

            except (
                NoSuchElementException,
                StaleElementReferenceException
            ):

                return False

        try:

            self.wait.until(page_changed)

        except TimeoutException:

            print(
                "Page-change verification timed out. "
                "Continuing because customer rows "
                "are present."
            )

        print(
            "Next page loaded successfully."
        )

        return True

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
                f"\n========== CHECKING CUSTOMER PAGE "
                f"{page_count} =========="
            )

            self.waitForTable()

            processing_locators = [

                (
                    By.ID,
                    "customers-grid_processing"
                ),

                (
                    By.CSS_SELECTOR,
                    "#customers-grid_wrapper "
                    ".dataTables_processing"
                ),

                (
                    By.CSS_SELECTOR,
                    ".dataTables_processing"
                )
            ]

            for by, locator in processing_locators:

                try:

                    elements = self.driver.find_elements(
                        by,
                        locator
                    )

                    if not elements:
                        continue

                    processing_element = elements[0]

                    if processing_element.is_displayed():

                        print(
                            "Customer DataTable is processing..."
                        )

                        self.wait.until(
                            EC.invisibility_of_element_located(
                                (
                                    by,
                                    locator
                                )
                            )
                        )

                        print(
                            "Customer DataTable processing "
                            "completed."
                        )

                    break

                except (
                    NoSuchElementException,
                    StaleElementReferenceException
                ):

                    continue

                except TimeoutException:

                    print(
                        "DataTable processing indicator "
                        "did not disappear within the "
                        "expected time."
                    )

                    break

            try:

                self.waitForCustomerRows()

            except TimeoutException:

                print(
                    "No loaded customer rows found. "
                    "Retrying current page..."
                )

                continue

            restart_current_page = False

            try:

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.tableRows_xpath
                )

                print(
                    f"Rows found on current page: "
                    f"{len(rows)}"
                )

                for row_number, row in enumerate(
                    rows,
                    start=1
                ):

                    try:

                        row_text = (
                            row.text
                            .strip()
                        )

                        print(
                            f"Row {row_number}: "
                            f"{row_text[:200]}"
                        )

                    except StaleElementReferenceException:

                        print(
                            f"Row {row_number} became stale "
                            f"during debug."
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

                        if (
                            not row_email
                            or row_email.lower()
                            == "loading..."
                        ):
                            continue

                        print(
                            f"Row {row_index + 1} email: "
                            f"{row_email}"
                        )

                        if (
                            row_email.lower()
                            == email.lower()
                        ):

                            print(
                                f"\nCustomer found: "
                                f"'{email}'"
                            )

                            print(
                                f"Customer row position: "
                                f"{row_index + 1}"
                            )

                            edit_button_xpath = (
                                f"{row_xpath}"
                                f"//td[last()]//a"
                            )

                            edit_button = self.wait.until(
                                EC.presence_of_element_located(
                                    (
                                        By.XPATH,
                                        edit_button_xpath
                                    )
                                )
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

                            edit_button = self.wait.until(
                                EC.element_to_be_clickable(
                                    (
                                        By.XPATH,
                                        edit_button_xpath
                                    )
                                )
                            )

                            print(
                                "Clicking Edit button..."
                            )

                            try:

                                edit_button.click()

                            except StaleElementReferenceException:

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

                        restart_current_page = True
                        break

            except StaleElementReferenceException:

                print(
                    "Customer table became stale "
                    "while searching."
                )

                restart_current_page = True

            if restart_current_page:

                print(
                    f"Refreshing search state for page "
                    f"{page_count}..."
                )

                continue

            print(
                f"Customer '{email}' not found on page "
                f"{page_count}."
            )

            if not self._clickNextPage():

                raise AssertionError(
                    f"Customer '{email}' was not found "
                    f"after checking page {page_count}. "
                    f"Next pagination control is not available."
                )

        raise AssertionError(
            f"Customer '{email}' was not found "
            f"within {max_pages} pages."
        )

    # =================================================
    # CHECK FIRST NAME UPDATED
    # =================================================
    def isCustomerFirstNameUpdated(
        self,
        email,
        expected_first_name
    ):

        email = email.strip()
        expected_first_name = expected_first_name.strip()

        max_pages = 100
        page_count = 0

        while page_count < max_pages:

            page_count += 1

            print(
                f"\n========== VERIFYING FIRST NAME "
                f"PAGE {page_count} =========="
            )

            self.waitForTable()

            try:

                self.waitForCustomerRows()

            except TimeoutException:

                print(
                    "Real customer rows not available. "
                    "Retrying current page..."
                )

                continue

            rows = self.driver.find_elements(
                By.XPATH,
                self.tableRows_xpath
            )

            print(
                f"Rows found on current page: "
                f"{len(rows)}"
            )

            restart_current_page = False

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

                    if len(columns) < 4:
                        continue

                    row_email = (
                        columns[1]
                        .text
                        .strip()
                    )

                    if (
                        not row_email
                        or row_email.lower()
                        == "loading..."
                    ):
                        continue

                    print(
                        f"Row {row_index + 1} email: "
                        f"{row_email}"
                    )

                    if (
                        row_email.lower()
                        == email.lower()
                    ):

                        customer_name = (
                            columns[2]
                            .text
                            .strip()
                        )

                        print(
                            "Expected first name:",
                            expected_first_name
                        )

                        print(
                            "Actual customer name:",
                            customer_name
                        )

                        if (
                            expected_first_name.lower()
                            in customer_name.lower()
                        ):

                            print(
                                "Customer first name "
                                "updated successfully."
                            )

                            return True

                        print(
                            "Customer found, but first name "
                            "does not match expected value."
                        )

                        return False

                except StaleElementReferenceException:

                    print(
                        f"Row {row_index + 1} became stale."
                    )

                    restart_current_page = True
                    break

            if restart_current_page:

                print(
                    "Restarting current page verification..."
                )

                continue

            print(
                f"Customer '{email}' not found on "
                f"page {page_count}."
            )

            if not self._clickNextPage():

                raise AssertionError(
                    f"Customer '{email}' was not found "
                    f"after checking page {page_count}."
                )

        raise AssertionError(
            f"Customer '{email}' was not found "
            f"within {max_pages} pages."
        )

    # =================================================
    # CHECK CUSTOMER NAME UPDATED
    # =================================================
    def isCustomerNameUpdated(
        self,
        email,
        expected_name
    ):

        email = email.strip()
        expected_name = expected_name.strip()

        max_pages = 100
        page_count = 0

        while page_count < max_pages:

            page_count += 1

            print(
                f"\n========== VERIFYING CUSTOMER PAGE "
                f"{page_count} =========="
            )

            self.waitForTable()

            try:

                self.waitForCustomerRows()

            except TimeoutException:

                print(
                    "Real customer rows not available. "
                    "Retrying current page..."
                )

                continue

            rows = self.driver.find_elements(
                By.XPATH,
                self.tableRows_xpath
            )

            print(
                f"Rows found on current page: "
                f"{len(rows)}"
            )

            restart_current_page = False

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

                    if len(columns) < 4:
                        continue

                    row_email = (
                        columns[1]
                        .text
                        .strip()
                    )

                    if (
                        not row_email
                        or row_email.lower()
                        == "loading..."
                    ):
                        continue

                    print(
                        f"Row {row_index + 1} email: "
                        f"{row_email}"
                    )

                    if (
                        row_email.lower()
                        == email.lower()
                    ):

                        actual_name = (
                            columns[2]
                            .text
                            .strip()
                        )

                        print(
                            "Expected customer name:",
                            expected_name
                        )

                        print(
                            "Actual customer name:",
                            actual_name
                        )

                        if (
                            actual_name.lower()
                            == expected_name.lower()
                        ):

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

            if restart_current_page:

                print(
                    "Restarting current page verification..."
                )

                continue

            print(
                f"Customer '{email}' not found on "
                f"page {page_count}."
            )

            if not self._clickNextPage():

                raise AssertionError(
                    f"Customer '{email}' was not found "
                    f"after checking page {page_count}."
                )

        raise AssertionError(
            f"Customer '{email}' was not found "
            f"within {max_pages} pages."
        )

    # =================================================
    # CHECK CUSTOMER DELETED
    # =================================================
    def isCustomerDeleted(self, email):

        email = email.strip()

        self.waitForTable()

        try:

            self.waitForCustomerRows()

        except TimeoutException:

            print(
                "No real customer rows available. "
                "Customer may already be deleted."
            )

            return True

        rows = self.driver.find_elements(
            By.XPATH,
            self.tableRows_xpath
        )

        for row in rows:

            try:

                columns = row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                if len(columns) >= 2:

                    row_email = (
                        columns[1]
                        .text
                        .strip()
                    )

                    if (
                        not row_email
                        or row_email.lower()
                        == "loading..."
                    ):
                        continue

                    if (
                        row_email.lower()
                        == email.lower()
                    ):

                        print(
                            f"Customer '{email}' "
                            f"still exists."
                        )

                        return False

            except StaleElementReferenceException:

                continue

        print(
            f"Customer '{email}' was not found "
            f"on the current page."
        )

        return True

