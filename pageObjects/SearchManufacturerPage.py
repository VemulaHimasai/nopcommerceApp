import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchManufacturer:
    txtManufacturername_xpath = "//input[@id='SearchManufacturerName']"
    drpPublished = (
        "//span[@id='select2-SearchPublishedId-container']"
    )
    lstPublished_All = (
        "//li[@role='option' and normalize-space()='All']"
    )
    lstPublished_Published = (
        "//li[@role='option' and normalize-space()='Published']"
    )
    lstPublished_Unpublished = (
        "//li[@role='option' and "
        "normalize-space()='Unpublished only']"
    )

    #btnSearch
    btnSearch = "//button[@id='search-manufacturers']"

    #Manufacturer Table
    tblmanufacturer = "//table[@id='manufacturers-grid']"

    #Manufacturer Checkboxes
    checkboxes_xpath = (
        "//table[@id='manufacturers-grid']"
        "//tbody/tr/td[1]"
        "//input[@type='checkbox']"
    )

    #constructor
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    #enter manufacturer name

    def enterManufacturerName(self,manufacturer):
        print("\n========== ENTER MANUFACTURER NAME ==========")
        print("Manufacturer:", manufacturer)
        for attempt in range(1, 4):
            try:
                manufacturer_name = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.txtManufacturername_xpath)
                    )
                )
                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                    block:'center',
                    inline:'nearest'
                    });
                    """,manufacturer_name
                )
                # Re-find the element after scrolling
                manufacturer_name = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.txtManufacturername_xpath)
                    )
                )
                manufacturer_name.click()
                manufacturer_name.clear()
                manufacturer_name.send_keys(manufacturer)
                actual_value = manufacturer_name.get_attribute("value")
                print("Manufacturer value entered:", repr(actual_value))
                if actual_value == manufacturer:
                    print("Manufacturer name entered successfully")
                    return True
                # Firefox can occasionally leave the field empty
                # after a normal send_keys operation.
                self.driver.execute_script(
                    """
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(
                        new Event('input', {bubbles: true})
                    );
                    arguments[0].dispatchEvent(
                        new Event('change', {bubbles: true})
                    );
                    """,
                    manufacturer_name,
                    manufacturer
                )
                actual_value = manufacturer_name.get_attribute("value")
                print(
                    "Manufacturer value after JS fallback:",
                    repr(actual_value)
                )
                if actual_value == manufacturer:
                    print("Manufacturer name entered successfully using JS fallback")
                    return True
                print(
                    f"Manufacturer value mismatch "
                    f"(attempt {attempt}/3)"
                )
            except (
                StaleElementReferenceException,
                TimeoutException
            ) as e:
                print(
                    f"Unable to enter category name "
                    f"(attempt {attempt}/3): "
                    f"{type(e).__name__}: {e}"
                )
                if attempt == 3:
                    raise
                time.sleep(3)
        raise AssertionError(
            f"Unable to enter manufacturer name: {manufacturer}"
        )
    # =========================================================
    # SELECT PUBLISHED FILTER
    # =========================================================

    def selectPublishedItem(self, published):

        print(
            "\n========== SELECT PUBLISHED =========="
        )

        print(
            "Selecting Published:",
            published
        )

        for attempt in range(1, 4):

            try:

                published_dropdown = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.drpPublished
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
                    published_dropdown
                )

                # Re-find after scrolling
                published_dropdown = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.drpPublished
                        )
                    )
                )

                published_dropdown.click()

                published_item_xpath = (
                    "//li[contains("
                    "@class,"
                    "'select2-results__option'"
                    ") "
                    "and normalize-space(.)="
                    f"'{published}' "
                    "and not(contains("
                    "@class,"
                    "'select2-results__message'"
                    "))]"
                )

                published_option = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            published_item_xpath
                        )
                    )
                )

                published_option.click()

                print(
                    "Published Item selected:",
                    published
                )

                return

            except (
                StaleElementReferenceException,
                TimeoutException
            ):

                print(
                    f"Published selection retry "
                    f"({attempt}/3)..."
                )

                if attempt == 3:
                    raise

                time.sleep(1)

        raise AssertionError(
            f"Unable to select Published: {published}"
        )
    # =========================================================
    # CLICK SEARCH
    # =========================================================

    def clickSearch(self):
        print(
            "\n========== CLICK SEARCH =========="
        )
        search_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.txtManufacturername_xpath)
        ))
        search_value_before = (
            search_field.get_attribute("value")
        )
        print("Manufacturer Name before Search: ",repr(search_value_before))
        #find search button
        search_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnSearch)
        ))
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            search_button
        )
        print(
            "Search button found."
        )

        print(
            "Search button text:",
            repr(search_button.text)
        )

        print(
            "Search button enabled:",
            search_button.is_enabled()
        )
        rows_xpath = (
            self.tblmanufacturer
            + "//tbody//tr"
        )
        before_rows = self.driver.find_elements(By.XPATH, rows_xpath)
        print("Rows Before Search: ",len(before_rows))
        search_button.click()
        print("Search button clicked using Selenium")
        self.wait.until(EC.presence_of_element_located(
            (
                By.XPATH,
                self.tblmanufacturer
            )
        ))
        print("Manufacturer table found after search")
        self.wait.until(EC.presence_of_element_located(
            (
                By.XPATH,
                self.tblmanufacturer
                + "//tbody"
            )
        ))
        time.sleep(0.5)
        processing_xpath = (
            self.tblmanufacturer
            + "//ancestor::div[contains("
            "@class,"
            "'dataTables_wrapper'"
            ")]"
            + "//div[contains("
            "@class,"
            "'dataTables_processing'"
            ")]"
        )
        try:
            processing_elements = (
                self.driver.find_elements(By.XPATH, processing_xpath)
            )
            processing_visible = any(
                element.is_displayed()
                for element in processing_elements
            )
            print("Datatables processing visible: ", processing_visible)
            if processing_visible:
                WebDriverWait(self.driver, 20).until(
                    EC.invisibility_of_element_located(
                        (
                            By.XPATH,
                            processing_xpath
                        )
                    )
                )
                print("Datatable Processing completed")
            else:
                print(
                    "DataTables processing already "
                    "completed or was too fast to observe."
                )
        except (TimeoutException, StaleElementReferenceException):
            print("Processing indicator could not be verified.")

        try:
            rows = self.driver.find_elements(
                By.XPATH,
                rows_xpath
            )

            print(
                "\n========== SEARCH RESULT TABLE =========="
            )

            print(
                "Number of table rows:",
                len(rows)
            )
            for index,row in enumerate(rows,start=1):
                try:
                    row_text = row.text.strip()

                    print(
                        f"Search Row {index}:",
                        row_text
                    )
                except StaleElementReferenceException:
                    print(f"Search Row {index}: STALE")
            print(
                "========== END SEARCH RESULT TABLE ==========\n"
            )
        except Exception as e:
            print(
                "Unable to inspect search result table:",
                type(e).__name__,
                str(e)
            )
            raise
        print(
            "Search results table loaded."
        )

    def isManufacturerPresent(self,manufacturer_name):
        rows_xpath = (
            "//table[@id='manufacturers-grid']"
        )
        expected_manufacturer_name = " ".join(
            manufacturer_name.split()
        ).strip().lower()

        print(
            "\n========== CHECK MANUFACTURER =========="
        )
        print("Checking manufacturer: ",manufacturer_name)
        print("Expected normalized name: ",expected_manufacturer_name)
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH,self.tblmanufacturer)
            ))
            rows = self.driver.find_elements(By.XPATH, rows_xpath)
            print("Rows found: ",len(rows))
            for index,row in enumerate(rows,start=1):
                try:
                    cells = row.find_elements(By.TAG_NAME,"td")
                    if len(cells) < 2:
                        continue

                    actual_manufacturer_name = (
                        cells[1].text.strip()
                    )
                    normalized_manufacturer_name = (
                        " ".join(
                            actual_manufacturer_name.split()
                        ).strip().lower()
                    )
                    print(f"Row {index}: "
                          f"{actual_manufacturer_name}")
                    if normalized_manufacturer_name == expected_manufacturer_name:
                        print(f"Manufacturer found: "f"{actual_manufacturer_name}")
                        return True
                except StaleElementReferenceException:
                    print(
                        f"Row {index} became stale. "
                        f"Skipping..."
                    )

                    continue
            print(f"Manufacturer Not found: "f"{manufacturer_name}")
            return False
        except TimeoutException:
            print("Manufacturer table was not found")
            print("Current URL: ",self.driver.current_url)
            print("Page Title: ",self.driver.title)
            return False


    def isNoDataAvailable(self):
        print("\n========== CHECK NO DATA ==========")
        no_data_xpaths = [
            (
                    self.tblmanufacturer
                    + "//tbody//td[contains("
                      "@class,"
                      "'dt-empty'"
                      ")]"
            ),
            (
                    self.tblmanufacturer
                    + "//tbody//td[contains("
                      "normalize-space(.),"
                      "'No data available in table'"
                      ")]"
            )
        ]
        for xpath in no_data_xpaths:
            try:
                no_data = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, xpath)
                    ))
                actual_text = (no_data.text.strip())
                print("Search result message: ",actual_text)
                if actual_text == "No data available in table":
                    print("NO DATA confirmed")
                    return True
            except TimeoutException:
                continue

        print(
            "No 'No data available in table' "
            "message found"
        )
        return False

    def isNoRecordsDisplayed(self):
        print("\n========== CHECK NO RECORDS ==========")
        records_xpaths = [
            "//div[contains(@class,'dt-info')]",

            "//div[contains("
            "@class,"
            "'dataTables_info'"
            ")]",

            (
                "//div[contains("
                "@class,"
                "'dataTables_wrapper'"
                ")]"
                "//div[contains("
                "@class,"
                "'dt-info'"
                ")]"
            ),

            (
                "//div[contains("
                "@class,"
                "'dataTables_wrapper'"
                ")]"
                "//div[contains("
                "@class,"
                "'dataTables_info'"
                ")]"
            )
        ]
        for xpath in records_xpaths:
            try:
                records = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, xpath)
                    )
                )
                actual_text = (
                    records.text.strip()
                )
                print("Records information: ",actual_text)
                if actual_text == "No records":
                    print("NO RECORDS found")
                    return True
                if "No records" in actual_text:
                    print("NO RECORDS text confirmed")
                    return True
            except TimeoutException:
                continue

        print("No 'No records' text found")
        return False

    def printSearchResults(self):
        rows = self.driver.find_elements(By.XPATH,self.tblmanufacturer + "//tbody//tr")
        print(f"Total rows: {len(rows)}")
        for index,row in enumerate(rows,start=1):
            try:
                print(f"Search Row: {index}: "
                      f"{row.text.strip()}")
            except StaleElementReferenceException:
                print(f"Search Row {index}: STALE")


    def getFirstManufacturerName(self):
        print("\n========== GET FIRST MANUFACTURER NAME ==========")
        rows_xpath = (
            "//table[@id='manufacturers-grid']"
            "//tbody//tr"
        )
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH,self.tblmanufacturer)
                )
            )
            time.sleep(1)
            rows = self.driver.find_elements(By.XPATH,rows_xpath)
            print("Total rows found: ", len(rows))
            for index,row in enumerate(rows,start=1):
                try:
                    cells = row.find_elements(By.TAG_NAME,"td")
                    if len(cells) < 2:
                        continue

                    manufacturer_name = cells[1].text.strip()
                    if not manufacturer_name:
                        continue

                    if "No data available in table" in manufacturer_name:
                        continue
                    print(
                        "First Manufacturer found:",
                        repr(manufacturer_name)
                    )
                    return manufacturer_name
                except StaleElementReferenceException:
                    print(
                        f"Row {index} became stale. Skipping..."
                    )
                    continue

            print("No category found in the table.")
            return None
        except TimeoutException:
            print("Category table was not found.")
            print("Current URL:", self.driver.current_url)
            print("Page title:", self.driver.title)
            return None

    def getManufacturerRowCount(self):
        rows_xpath = (
            "//table[@id='manufacturers-grid']"
            "//tbody//tr"
        )
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH,self.tblmanufacturer)
                )
            )
            rows = self.driver.find_elements(By.XPATH,rows_xpath)
            valid_row_count = 0
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME,"td")
                    if len(cells) < 2:
                        continue
                    manufacturer_name = cells[1].text.strip()
                    if not manufacturer_name:
                        continue
                    if "No data avaiable in table" in manufacturer_name:
                        continue
                    valid_row_count += 1

                except StaleElementReferenceException:
                    continue

            print("Valid manufacturer rows found: ",valid_row_count)
            return valid_row_count
        except TimeoutException:
            print("Manufacturer table was not found.")
            return 0
    



