import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DeleteManufacturer:

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
    # Manufacturers table
    # -------------------------------------------------

    manufacturers_table_xpath = (
        "//table[@id='manufacturers-grid']"
    )

    manufacturer_rows_xpath = (
        "//table[@id='manufacturers-grid']//tbody//tr"
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

    def getManufacturerRow(self, manufacturer_name):

        expected_name = " ".join(
            manufacturer_name.split()
        ).strip().lower()

        print("\n========== FIND MANUFACTURER ==========")
        print(
            f"Searching for category: "
            f"{manufacturer_name}"
        )

        max_pages = 20

        for page in range(1, max_pages + 1):

            print(
                f"\nChecking category table "
                f"page {page}..."
            )

            # -------------------------------------------------
            # Wait for manufacturer table
            # -------------------------------------------------

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self.manufacturers_table_xpath
                    )
                )
            )

            # -------------------------------------------------
            # Wait until real manufacturer rows are loaded
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
                            self.manufacturer_rows_xpath
                        )
                    )
                )

            except TimeoutException:

                print(
                    "Manufacturer rows did not load "
                    "within the expected time."
                )

                # Try refreshing the current Categories page
                # before giving up on this page.

                self.driver.refresh()

                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.manufacturers_table_xpath
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
                                self.manufacturer_rows_xpath
                            )
                        )
                    )

                except TimeoutException:

                    print(
                        "Manufacturer rows still not loaded "
                        "after refresh."
                    )

                    continue

            # -------------------------------------------------
            # Get current page rows
            # -------------------------------------------------

            rows = self.driver.find_elements(
                By.XPATH,
                self.manufacturer_rows_xpath
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
                            f"Manufacturer found on "
                            f"page {page}: "
                            f"{manufacturer_name}"
                        )

                        return row

                except StaleElementReferenceException:

                    print(
                        f"ROW {index}: "
                        f"stale element"
                    )

                    continue

            print(
                f"Manufacturer not found on "
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
                                self.manufacturer_rows_xpath
                            )
                        )
                    )
                )

            except TimeoutException:

                print(
                    "New manufacturer page did not finish "
                    "loading within the expected time."
                )

                continue

            time.sleep(0.5)

        raise AssertionError(
            f"Manufacturer not found after searching "
            f"{max_pages} pages: "
            f"{manufacturer_name}"
        )
    # -------------------------------------------------
    # Select category
    # -------------------------------------------------

    def selectManufacturer(self, manufacturer_name):

        for attempt in range(1, 4):

            try:

                print(
                    f"Selecting category "
                    f"(attempt {attempt}/3): "
                    f"{manufacturer_name}"
                )

                row = self.getManufacturerRow(
                    manufacturer_name
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
                        "Manufacturer selected successfully."
                    )

                    return True

            except (
                StaleElementReferenceException,
                TimeoutException,
                ElementClickInterceptedException
            ) as exc:

                print(
                    f"Unable to select manufacturer "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            f"Unable to select manufacturer: "
            f"{manufacturer_name}"
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



    def confirmDelete(self, manufacturer_name=None):

        for attempt in range(1, 4):

            try:

                print(
                    f"Confirming manufacturer deletion "
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

                time.sleep(0.5)

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                print(
                    "Manufacturer deletion confirmation clicked."
                )

                # -------------------------------------------------
                # Wait for confirmation modal to disappear
                # -------------------------------------------------

                try:

                    self.wait.until(
                        EC.invisibility_of_element_located(
                            (
                                By.XPATH,
                                self.btnDeleteConfirm
                            )
                        )
                    )

                    print(
                        "Delete confirmation dialog closed."
                    )

                except TimeoutException:

                    print(
                        "Delete confirmation dialog did not "
                        "disappear within the expected time."
                    )

                # -------------------------------------------------
                # Give DataTables/AJAX time to process deletion
                # -------------------------------------------------

                time.sleep(1)

                # -------------------------------------------------
                # If category name was supplied, wait until the
                # deleted category disappears from the current
                # category grid.
                # -------------------------------------------------

                if manufacturer_name:

                    expected_name = " ".join(
                        manufacturer_name.split()
                    ).strip().lower()

                    def manufacturer_removed(driver):

                        rows = driver.find_elements(
                            By.XPATH,
                            self.manufacturer_rows_xpath
                        )

                        for row in rows:

                            try:

                                row_text = " ".join(
                                    row.text.split()
                                ).strip().lower()

                                if expected_name in row_text:
                                    print(
                                        "Deleted manufacturer is still "
                                        "present in the grid."
                                    )

                                    return False

                            except StaleElementReferenceException:

                                # DataTables is refreshing.
                                return False

                        return True

                    try:

                        self.wait.until(
                            manufacturer_removed
                        )

                        print(
                            f"Category removed from grid: "
                            f"{manufacturer_name}"
                        )

                    except TimeoutException:

                        print(
                            f"Manufacturer still appears in grid "
                            f"after deletion wait: "
                            f"{manufacturer_name}"
                        )

                print(
                    "Manufacturer deletion completed."
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
            "Unable to confirm manufacturer deletion."
        )



    def isManufacturerPresent(self, manufacturer_name):

        expected_category_name = " ".join(
            manufacturer_name.split()
        ).strip().lower()

        for attempt in range(1, 4):

            try:

                print(
                    f"Checking manufacturer presence "
                    f"(attempt {attempt}/3): "
                    f"{manufacturer_name}"
                )

                # Wait for the category table
                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            self.manufacturers_table_xpath
                        )
                    )
                )

                rows = self.driver.find_elements(
                    By.XPATH,
                    self.manufacturer_rows_xpath
                )

                print(
                    f"Manufacturer rows found: {len(rows)}"
                )

                for row in rows:

                    try:

                        row_text = " ".join(
                            row.text.split()
                        ).strip().lower()

                        print(
                            f"Checking manufacturer row: "
                            f"{row_text}"
                        )

                        if expected_category_name in row_text:
                            print(
                                f"Manufacturer found: "
                                f"{manufacturer_name}"
                            )

                            return True

                    except StaleElementReferenceException:

                        continue

                print(
                    f"Manufacturer not found: "
                    f"{manufacturer_name}"
                )

                return False

            except (
                    StaleElementReferenceException,
                    TimeoutException
            ) as exc:

                print(
                    f"Unable to check manufacturer presence "
                    f"on attempt {attempt}: {exc}"
                )

                if attempt < 3:
                    time.sleep(1)

        raise AssertionError(
            f"Unable to verify manufacturer presence: "
            f"{manufacturer_name}"
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