import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DeleteCategory:

    # -------------------------------------------------
    # Delete buttons
    # -------------------------------------------------

    btnDeleteSelected = (
        "//button[@id='delete-selected']"
    )

    btnDeleteConfirm = (
        "//button[@id='delete-selected-action-confirmation-submit-button']"
    )

    # -------------------------------------------------
    # Categories table
    # -------------------------------------------------

    categories_table_xpath = (
        "//table[@id='categories-grid']"
    )

    category_rows_xpath = (
        "//table[@id='categories-grid']//tbody/tr"
    )

    previous_xpath = "//a[normalize-space()='Previous']"
    next_xpath = "//a[normalize-space()='Next']"


    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # -------------------------------------------------
    # Find category row
    # -------------------------------------------------

    def getCategoryRow(self, category_name):

        expected_name = " ".join(
            category_name.split()
        ).strip().lower()

        print("\n========== FIND CATEGORY ==========")
        print(
            f"Searching for category: "
            f"{category_name}"
        )

        max_pages = 20

        for page in range(1, max_pages + 1):

            print(
                f"\nChecking category table "
                f"page {page}..."
            )

            # -------------------------------------------------
            # Wait for category table
            # -------------------------------------------------

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.categories_table_xpath
                    )
                )
            )

            # -------------------------------------------------
            # Wait until real category rows are loaded
            # -------------------------------------------------

            try:

                self.wait.until(
                    lambda driver: any(
                        (
                                "loading..." not in
                                " ".join(row.text.split()).lower()
                                and
                                row.text.strip()
                        )
                        for row in driver.find_elements(
                            By.XPATH,
                            self.category_rows_xpath
                        )
                    )
                )

            except TimeoutException:

                print(
                    "Category rows did not load "
                    "within the expected time."
                )

                # Try refreshing the current Categories page
                # before giving up on this page.

                self.driver.refresh()

                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.categories_table_xpath
                        )
                    )
                )

                try:

                    self.wait.until(
                        lambda driver: any(
                            (
                                    "loading..." not in
                                    " ".join(row.text.split()).lower()
                                    and
                                    row.text.strip()
                            )
                            for row in driver.find_elements(
                                By.XPATH,
                                self.category_rows_xpath
                            )
                        )
                    )

                except TimeoutException:

                    print(
                        "Category rows still not loaded "
                        "after refresh."
                    )

                    continue

            # -------------------------------------------------
            # Get current page rows
            # -------------------------------------------------

            rows = self.driver.find_elements(
                By.XPATH,
                self.category_rows_xpath
            )

            print(
                f"Rows found on page {page}: "
                f"{len(rows)}"
            )

            # -------------------------------------------------
            # Search current page
            # -------------------------------------------------

            for index, row in enumerate(
                    rows,
                    start=1
            ):

                try:

                    row_text = " ".join(
                        row.text.split()
                    ).strip()

                    print(
                        f"ROW {index}: "
                        f"{row_text!r}"
                    )

                    if not row_text:
                        continue

                    if row_text.lower() == "loading...":
                        continue

                    if expected_name in row_text.lower():
                        print(
                            f"Category found on "
                            f"page {page}: "
                            f"{category_name}"
                        )

                        return row

                except StaleElementReferenceException:

                    print(
                        f"ROW {index}: "
                        f"stale element"
                    )

                    continue

            print(
                f"Category not found on "
                f"page {page}."
            )

            # -------------------------------------------------
            # Check Next button
            # -------------------------------------------------

            next_buttons = self.driver.find_elements(
                By.XPATH,
                self.next_xpath
            )

            if not next_buttons:
                print(
                    "Next button does not exist. "
                    "No more pages."
                )

                break

            try:

                next_button = next_buttons[0]

                next_class = (
                        next_button.get_attribute("class")
                        or ""
                )

                print(
                    f"Next button class: "
                    f"{next_class!r}"
                )

                if "disabled" in next_class.lower():
                    print(
                        "Next button is disabled. "
                        "Last page reached."
                    )

                    break

                # Save current row text so we can detect
                # that DataTables actually changed pages.

                old_first_row_text = ""

                if rows:

                    try:
                        old_first_row_text = " ".join(
                            rows[0].text.split()
                        ).strip()

                    except StaleElementReferenceException:
                        pass

            except StaleElementReferenceException:

                print(
                    "Next button became stale."
                )

                continue

            # -------------------------------------------------
            # Click Next
            # -------------------------------------------------

            self.clickNextPage()

            # -------------------------------------------------
            # Wait for DataTables to refresh
            # -------------------------------------------------

            try:

                self.wait.until(
                    lambda driver: (
                        any(
                            (
                                    "loading..." not in
                                    " ".join(row.text.split()).lower()
                                    and
                                    row.text.strip()
                            )
                            for row in driver.find_elements(
                                By.XPATH,
                                self.category_rows_xpath
                            )
                        )
                    )
                )

            except TimeoutException:

                print(
                    "New category page did not finish "
                    "loading within the expected time."
                )

                continue

            time.sleep(0.5)

        raise AssertionError(
            f"Category not found after searching "
            f"{max_pages} pages: "
            f"{category_name}"
        )
    # -------------------------------------------------
    # Select category
    # -------------------------------------------------

    def selectCategory(self, category_name):

        for attempt in range(1, 4):

            try:

                print(
                    f"Selecting category "
                    f"(attempt {attempt}/3): "
                    f"{category_name}"
                )

                row = self.getCategoryRow(
                    category_name
                )

                checkbox = row.find_element(
                    By.XPATH,
                    ".//input[@type='checkbox']"
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

                time.sleep(0.5)

                if not checkbox.is_selected():

                    self.driver.execute_script(
                        "arguments[0].click();",
                        checkbox
                    )

                if checkbox.is_selected():

                    print(
                        "Category selected successfully."
                    )

                    return True

            except (
                StaleElementReferenceException,
                TimeoutException,
                ElementClickInterceptedException
            ) as exc:

                print(
                    f"Unable to select category "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            f"Unable to select category: "
            f"{category_name}"
        )

    # -------------------------------------------------
    # Delete selected category
    # -------------------------------------------------

    def clickDeleteSelected(self):

        for attempt in range(1, 4):

            try:

                print(
                    f"Clicking Delete Selected "
                    f"(attempt {attempt}/3)..."
                )

                button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.btnDeleteSelected
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

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                print(
                    "Delete Selected clicked successfully."
                )

                return True

            except (
                StaleElementReferenceException,
                TimeoutException,
                ElementClickInterceptedException
            ) as exc:

                print(
                    f"Unable to click Delete Selected "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            "Unable to click Delete Selected."
        )

    # -------------------------------------------------
    # Confirm deletion
    # -------------------------------------------------

    def confirmDelete(self):

        for attempt in range(1, 4):

            try:

                print(
                    f"Confirming category deletion "
                    f"(attempt {attempt}/3)..."
                )

                button = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.btnDeleteConfirm
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

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                print(
                    "Category deletion confirmed."
                )

                return True

            except (
                StaleElementReferenceException,
                TimeoutException,
                ElementClickInterceptedException
            ) as exc:

                print(
                    f"Unable to confirm deletion "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            "Unable to confirm category deletion."
        )

    def isCategoryPresent(self, category_name):

        expected_category_name = " ".join(
            category_name.split()
        ).strip().lower()

        for attempt in range(1, 4):

            try:

                print(
                    f"Checking category presence "
                    f"(attempt {attempt}/3): "
                    f"{category_name}"
                )

                # Wait for the category table
                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.categories_table_xpath
                        )
                    )
                )

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.category_rows_xpath
                )

                print(
                    f"Category rows found: {len(rows)}"
                )

                for row in rows:

                    try:

                        row_text = " ".join(
                            row.text.split()
                        ).strip().lower()

                        print(
                            f"Checking category row: "
                            f"{row_text}"
                        )

                        if expected_category_name in row_text:
                            print(
                                f"Category found: "
                                f"{category_name}"
                            )

                            return True

                    except StaleElementReferenceException:

                        continue

                print(
                    f"Category not found: "
                    f"{category_name}"
                )

                return False

            except (
                    StaleElementReferenceException,
                    TimeoutException
            ) as exc:

                print(
                    f"Unable to check category presence "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            f"Unable to verify category presence: "
            f"{category_name}"
        )

    def clickNextPage(self):

        print("\n========== CLICK NEXT PAGE ==========")

        for attempt in range(1, 4):

            try:

                next_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.next_xpath)
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    next_button
                )

                time.sleep(0.5)

                print(
                    f"Next button text: "
                    f"{next_button.text!r}"
                )

                print(
                    f"Next button class: "
                    f"{next_button.get_attribute('class')!r}"
                )

                print(
                    f"Next button aria-disabled: "
                    f"{next_button.get_attribute('aria-disabled')!r}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    next_button
                )

                print("Next button clicked.")

                time.sleep(1)

                return True

            except (
                    StaleElementReferenceException,
                    TimeoutException,
                    ElementClickInterceptedException
            ) as exc:

                print(
                    f"Unable to click Next "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            "Unable to click Next page."
        )

    def clickPreviousPage(self):

        print("\n========== CLICK PREVIOUS PAGE ==========")

        for attempt in range(1, 4):

            try:

                previous_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.previous_xpath)
                    )
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    previous_button
                )

                time.sleep(0.5)

                print(
                    f"Previous button text: "
                    f"{previous_button.text!r}"
                )

                print(
                    f"Previous button class: "
                    f"{previous_button.get_attribute('class')!r}"
                )

                print(
                    f"Previous button aria-disabled: "
                    f"{previous_button.get_attribute('aria-disabled')!r}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    previous_button
                )

                print("Previous button clicked.")

                time.sleep(1)

                return True

            except (
                    StaleElementReferenceException,
                    TimeoutException,
                    ElementClickInterceptedException
            ) as exc:

                print(
                    f"Unable to click Previous "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            "Unable to click Previous page."
        )