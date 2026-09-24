import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchCategory:

    # =========================================================
    # LOCATORS
    # =========================================================

    # Category name search field
    txtcategoryname_xpath = "//input[@id='SearchCategoryName']"

    # Published dropdown
    drpPublished = (
        "//span[@id='select2-SearchPublishedId-container']"
    )

    lstPublished_All = (
        "//li[@role='option' and normalize-space()='All']"
    )

    lstPublished_Published = (
        "//li[@role='option' and "
        "normalize-space()='Published only']"
    )

    lstPublished_Unpublished = (
        "//li[@role='option' and "
        "normalize-space()='Unpublished only']"
    )

    # Search button
    btnSearch = "//button[@id='search-categories']"

    # Category table
    tblcategory = "//table[@id='categories-grid']"

    # Category checkboxes
    checkboxes_xpath = (
        "//table[@id='categories-grid']"
        "//tbody/tr/td[1]"
        "//input[@type='checkbox']"
    )

    # =========================================================
    # CONSTRUCTOR
    # =========================================================

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # =========================================================
    # ENTER CATEGORY NAME
    # =========================================================

    def enterCategoryName(self, category):

        print(
            "\n========== ENTER CATEGORY NAME =========="
        )

        print(
            "Category:",
            category
        )

        category_name = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.txtcategoryname_xpath
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
            category_name
        )

        category_name.clear()
        category_name.send_keys(category)

        print(
            "Category name entered successfully."
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

        # -----------------------------------------------------
        # Verify search field value
        # -----------------------------------------------------

        search_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.txtcategoryname_xpath
                )
            )
        )

        search_value_before = (
            search_field.get_attribute("value")
        )

        print(
            "Category Name before Search:",
            repr(search_value_before)
        )

        # -----------------------------------------------------
        # Find Search button
        # -----------------------------------------------------

        search_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.btnSearch
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

        # -----------------------------------------------------
        # Capture current rows before search
        # -----------------------------------------------------

        rows_xpath = (
            self.tblcategory
            + "//tbody//tr"
        )

        before_rows = self.driver.find_elements(
            By.XPATH,
            rows_xpath
        )

        print(
            "Rows before Search:",
            len(before_rows)
        )

        # -----------------------------------------------------
        # Selenium click
        # -----------------------------------------------------

        search_button.click()

        print(
            "Search button clicked using Selenium."
        )

        # -----------------------------------------------------
        # Wait for table
        # -----------------------------------------------------

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.tblcategory
                )
            )
        )

        print(
            "Category table found after Search."
        )

        # -----------------------------------------------------
        # Wait for tbody
        # -----------------------------------------------------

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.tblcategory
                    + "//tbody"
                )
            )
        )

        # -----------------------------------------------------
        # Allow DataTables request to start
        # -----------------------------------------------------

        time.sleep(0.5)

        # -----------------------------------------------------
        # Check processing indicator
        # -----------------------------------------------------

        processing_xpath = (
            self.tblcategory
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
                self.driver.find_elements(
                    By.XPATH,
                    processing_xpath
                )
            )

            processing_visible = any(
                element.is_displayed()
                for element in processing_elements
            )

            print(
                "DataTables processing visible:",
                processing_visible
            )

            if processing_visible:

                WebDriverWait(
                    self.driver,
                    20
                ).until(
                    EC.invisibility_of_element_located(
                        (
                            By.XPATH,
                            processing_xpath
                        )
                    )
                )

                print(
                    "DataTables processing completed."
                )

            else:

                print(
                    "DataTables processing already "
                    "completed or was too fast to observe."
                )

        except (
            TimeoutException,
            StaleElementReferenceException
        ):

            print(
                "Processing indicator could not be verified."
            )

        # -----------------------------------------------------
        # Read final search result table
        # -----------------------------------------------------

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

            for index, row in enumerate(
                rows,
                start=1
            ):

                try:

                    row_text = row.text.strip()

                    print(
                        f"Search Row {index}:",
                        row_text
                    )

                except StaleElementReferenceException:

                    print(
                        f"Search Row {index}: STALE"
                    )

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

    # =========================================================
    # SELECT CATEGORY
    # =========================================================

    def selectCategory(self, category):

        print(
            "\n========== SELECT CATEGORY =========="
        )

        print(
            "Selecting category:",
            category
        )

        try:

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.tblcategory
                    )
                )
            )

            # Exact category-name match
            row_xpath = (
                f"//table[@id='categories-grid']"
                f"//tbody/tr["
                f"td[2][normalize-space()="
                f"'{category}']"
                f"]"
            )

            row = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        row_xpath
                    )
                )
            )

            print(
                "Category row found."
            )

            checkbox = row.find_element(
                By.XPATH,
                ".//td[1]//input[@type='checkbox']"
            )

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

                try:

                    checkbox.click()

                except Exception:

                    self.driver.execute_script(
                        "arguments[0].click();",
                        checkbox
                    )

            print(
                f"Category '{category}' "
                f"selected successfully."
            )

            return True

        except TimeoutException:

            print(
                f"Category '{category}' was not found."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Page title:",
                self.driver.title
            )

            raise

    # =========================================================
    # CHECK CATEGORY EXISTS
    # =========================================================

    def isCategoryPresent(self, category_name):

        rows_xpath = (
            "//table[@id='categories-grid']"
            "//tbody//tr"
        )

        expected_category_name = " ".join(
            category_name.split()
        ).strip().lower()

        print(
            "\n========== CHECK CATEGORY =========="
        )

        print(
            "Checking category:",
            category_name
        )

        print(
            "Expected normalized name:",
            expected_category_name
        )

        try:

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.tblcategory
                    )
                )
            )

            rows = self.driver.find_elements(
                By.XPATH,
                rows_xpath
            )

            print(
                "Rows found:",
                len(rows)
            )

            for index, row in enumerate(
                rows,
                start=1
            ):

                try:

                    cells = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if len(cells) < 2:
                        continue

                    # Category name is normally column 2
                    actual_category_name = (
                        cells[1].text.strip()
                    )

                    normalized_actual_name = (
                        " ".join(
                            actual_category_name.split()
                        )
                        .strip()
                        .lower()
                    )

                    print(
                        f"Row {index}: "
                        f"{actual_category_name!r}"
                    )

                    if (
                        normalized_actual_name
                        == expected_category_name
                    ):

                        print(
                            f"Category found: "
                            f"{actual_category_name}"
                        )

                        return True

                except StaleElementReferenceException:

                    print(
                        f"Row {index} became stale. "
                        f"Skipping..."
                    )

                    continue

            print(
                f"Category not found: "
                f"{category_name}"
            )

            return False

        except TimeoutException:

            print(
                "Category table was not found."
            )

            print(
                "Current URL:",
                self.driver.current_url
            )

            print(
                "Page title:",
                self.driver.title
            )

            return False

    # =========================================================
    # CHECK NO DATA AVAILABLE
    # =========================================================

    def isNoDataAvailable(self):

        print(
            "\n========== CHECK NO DATA =========="
        )

        no_data_xpaths = [

            (
                self.tblcategory
                + "//tbody//td[contains("
                "@class,"
                "'dt-empty'"
                ")]"
            ),

            (
                self.tblcategory
                + "//tbody//td[contains("
                "normalize-space(.),"
                "'No data available in table'"
                ")]"
            )
        ]

        for xpath in no_data_xpaths:

            try:

                no_data = WebDriverWait(
                    self.driver,
                    5
                ).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            xpath
                        )
                    )
                )

                actual_text = (
                    no_data.text.strip()
                )

                print(
                    "Search result message:",
                    actual_text
                )

                if (
                    actual_text
                    == "No data available in table"
                ):

                    print(
                        "NO DATA confirmed"
                    )

                    return True

            except TimeoutException:

                continue

        print(
            "No 'No data available in table' "
            "message found"
        )

        return False

    # =========================================================
    # CHECK NO RECORDS
    # =========================================================

    def isNoRecordsDisplayed(self):

        print(
            "\n========== CHECK NO RECORDS =========="
        )

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

                records = WebDriverWait(
                    self.driver,
                    5
                ).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            xpath
                        )
                    )
                )

                actual_text = (
                    records.text.strip()
                )

                print(
                    "Records information:",
                    actual_text
                )

                if actual_text == "No records":

                    print(
                        "NO RECORDS confirmed"
                    )

                    return True

                if "No records" in actual_text:

                    print(
                        "NO RECORDS text confirmed"
                    )

                    return True

            except TimeoutException:

                continue

        print(
            "No 'No records' text found"
        )

        return False

    # =========================================================
    # PRINT SEARCH RESULTS
    # =========================================================

    def printSearchResults(self):

        rows = self.driver.find_elements(
            By.XPATH,
            self.tblcategory
            + "//tbody//tr"
        )

        print(
            f"Total rows: {len(rows)}"
        )

        for index, row in enumerate(
            rows,
            start=1
        ):

            try:

                print(
                    f"Search Row {index}: "
                    f"{row.text.strip()}"
                )

            except StaleElementReferenceException:

                print(
                    f"Search Row {index}: STALE"
                )

    def getFirstCategoryName(self):

        print("\n========== GET FIRST CATEGORY NAME ==========")

        rows_xpath = (
            "//table[@id='categories-grid']"
            "//tbody//tr"
        )

        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.tblcategory)
                )
            )

            time.sleep(1)

            rows = self.driver.find_elements(
                By.XPATH,
                rows_xpath
            )

            print("Total rows found:", len(rows))

            for index, row in enumerate(rows, start=1):
                try:
                    cells = row.find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if len(cells) < 2:
                        continue

                    category_name = cells[1].text.strip()

                    if not category_name:
                        continue

                    if "No data available in table" in category_name:
                        continue

                    print(
                        "First category found:",
                        repr(category_name)
                    )

                    return category_name

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