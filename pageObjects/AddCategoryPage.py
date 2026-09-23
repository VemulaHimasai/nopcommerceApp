import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException
)


class AddCategory:

    # -------------------------------------------------
    # Catalog / Categories menu
    # -------------------------------------------------

    lnkCatalog_menu_xpath = (
        "//a[@href='#']//p[contains(text(),'Catalog')]"
    )

    lnkCategories_menuitem_xpath = (
        "//a[@href='/Admin/Category/List']"
    )

    # -------------------------------------------------
    # Category page
    # -------------------------------------------------

    btnAddNew_Category = (
        "//a[normalize-space()='Add new']"
    )

    txtCategoryName = (
        "//input[@id='Name']"
    )

    txtCategoryDesc = "//div[@role='textbox']"

    btnSave = (
        "//button[@name='save']"
    )

    success_msg = (
        "//div[contains(@class,'alert-success')]"
    )

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # -------------------------------------------------
    # Click Catalog menu
    # -------------------------------------------------

    def clickonCatalogmenu(self):

        print("\n========== OPEN CATALOG MENU ==========")

        for attempt in range(1, 4):

            try:

                print(
                    f"Opening Catalog menu "
                    f"(attempt {attempt}/3)"
                )

                catalog_menu = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.lnkCatalog_menu_xpath
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    catalog_menu
                )

                try:
                    catalog_menu.click()

                except ElementClickInterceptedException:

                    print(
                        "Catalog menu click intercepted. "
                        "Using JavaScript click..."
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        catalog_menu
                    )

                print("Catalog menu opened")
                return True

            except StaleElementReferenceException:

                print(
                    "Catalog menu became stale. Retrying..."
                )

                time.sleep(1)

            except TimeoutException:

                print(
                    "Timed out waiting for Catalog menu"
                )

                if attempt == 3:
                    raise

                time.sleep(1)

        return False

    # -------------------------------------------------
    # Click Categories submenu
    # -------------------------------------------------

    def clickonCategoriesmenuItem(self):

        print("\n========== OPEN CATEGORIES MENU ITEM ==========")

        for attempt in range(1, 4):

            try:

                print(
                    f"Opening Categories Menu Item "
                    f"(attempt {attempt}/3)"
                )

                categories_menu = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.lnkCategories_menuitem_xpath
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    categories_menu
                )

                try:
                    categories_menu.click()

                except ElementClickInterceptedException:

                    print(
                        "Categories menu click intercepted. "
                        "Using JavaScript click..."
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        categories_menu
                    )

                print("Categories menu item opened")

                # Verify navigation
                self.wait.until(
                    EC.url_contains("/Admin/Category/List")
                )

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                return True

            except StaleElementReferenceException:

                print(
                    "Categories menu item became stale. "
                    "Retrying..."
                )

                time.sleep(1)

            except TimeoutException:

                print(
                    "Timed out waiting for Categories menu item"
                )

                if attempt == 3:
                    raise

                time.sleep(1)

        return False

    # -------------------------------------------------
    # Click Add New
    # -------------------------------------------------



    def clickAddNew(self):

        print(
            "\n========== CLICK ADD NEW CATEGORY =========="
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Opening Category Create page "
                    f"(attempt {attempt}/3)"
                )

                # -------------------------------------------------
                # Locate exact Category Add New link
                # -------------------------------------------------

                add_new = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//a[@href='/Admin/Category/Create'"
                            " and normalize-space()='Add new']"
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    add_new
                )

                # -------------------------------------------------
                # Verify href before clicking
                # -------------------------------------------------

                href = add_new.get_attribute("href")

                print(
                    "Add new href:",
                    href
                )

                # -------------------------------------------------
                # Try normal Selenium click first
                # -------------------------------------------------

                try:

                    self.wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "//a[@href='/Admin/Category/Create'"
                                " and normalize-space()='Add new']"
                            )
                        )
                    )

                    add_new.click()

                    print(
                        "Normal Selenium click executed"
                    )

                except (
                        ElementClickInterceptedException,
                        StaleElementReferenceException
                ):

                    print(
                        "Normal click failed. "
                        "Using JavaScript click..."
                    )

                    add_new = self.driver.find_element(
                        By.XPATH,
                        "//a[@href='/Admin/Category/Create'"
                        " and normalize-space()='Add new']"
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        add_new
                    )

                    print(
                        "JavaScript click executed"
                    )

                # -------------------------------------------------
                # Wait for navigation
                # -------------------------------------------------

                self.wait.until(
                    EC.url_contains("/Admin/Category/Create")
                )

                print(
                    "Category Create page opened successfully"
                )

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                # -------------------------------------------------
                # Wait for Category Name field
                # -------------------------------------------------

                self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            "Name"
                        )
                    )
                )

                print(
                    "Category Name field is visible"
                )

                return True

            except TimeoutException:

                print(
                    "Category Create page did not open."
                )

                print(
                    "Current URL:",
                    self.driver.current_url
                )

                print(
                    "Page title:",
                    self.driver.title
                )

                if attempt == 3:
                    raise

                time.sleep(1)

            except StaleElementReferenceException:

                print(
                    "Add New element became stale. Retrying..."
                )

                if attempt == 3:
                    raise

                time.sleep(1)

        return False



    # -------------------------------------------------
    # Enter Category Name
    # -------------------------------------------------

    def setCategoryName(self, category_name):

        print(f"Entering category name: {category_name}")

        for attempt in range(1, 4):

            try:

                print(f"Category name entry attempt {attempt}/3")

                category_name_field = self.wait.until(
                    EC.presence_of_element_located(
                        (By.ID, "Name")
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    category_name_field
                )

                self.wait.until(
                    EC.visibility_of_element_located(
                        (By.ID, "Name")
                    )
                )

                category_name_field.click()
                category_name_field.clear()
                category_name_field.send_keys(category_name)

                # Verify the actual input value
                actual_value = self.driver.execute_script(
                    "return arguments[0].value;",
                    category_name_field
                )

                print(
                    f"Category Name DOM value: {actual_value!r}"
                )

                if actual_value == category_name:
                    print("Category name entered successfully.")
                    return True

                print(
                    "Category name value mismatch. Retrying..."
                )

            except StaleElementReferenceException:

                print(
                    "Category Name field became stale. Retrying..."
                )

            except Exception as e:

                print(
                    f"Category name entry attempt {attempt} failed: {e}"
                )

        raise AssertionError(
            f"Unable to enter category name: {category_name}"
        )

    # -------------------------------------------------
    # Enter Category Description
    # -------------------------------------------------

    def setCategoryDescription(self, description):

        print("Entering category description...")

        description_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.txtCategoryDesc
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            description_field
        )

        # Click the actual editor container
        description_field.click()

        # Set the editor content using JavaScript
        self.driver.execute_script(
            """
            const editor = arguments[0];
            const text = arguments[1];

            editor.focus();

            editor.innerHTML = '<p>' + text + '</p>';

            editor.dispatchEvent(
                new InputEvent('input', {
                    bubbles: true,
                    inputType: 'insertText',
                    data: text
                })
            );

            editor.dispatchEvent(
                new Event('change', {
                    bubbles: true
                })
            );
            """,
            description_field,
            description
        )

        print("Category description entered")

        # Verify text was actually inserted
        print(
            "Description text:",
            repr(description_field.text)
        )

    # -------------------------------------------------
    # Save Category
    # -------------------------------------------------

    def clickSave(self):

        print("\n========== SAVE CATEGORY ==========")

        try:

            # -------------------------------------------------
            # Locate Save button
            # -------------------------------------------------

            save_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        self.btnSave
                    )
                )
            )

            print("Save button found.")
            print("Save button text:", repr(save_button.text))
            print("Save button enabled:", save_button.is_enabled())
            print("Save button displayed:", save_button.is_displayed())

            # -------------------------------------------------
            # Scroll Save button into view
            # -------------------------------------------------

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                save_button
            )

            # -------------------------------------------------
            # Capture current values before Save
            # -------------------------------------------------

            name_value = self.driver.find_element(
                By.ID,
                "Name"
            ).get_attribute("value")

            print(
                "Category Name before Save:",
                repr(name_value)
            )

            # -------------------------------------------------
            # Click Save
            # -------------------------------------------------

            try:

                save_button.click()

                print(
                    "Normal Selenium Save click executed"
                )

            except ElementClickInterceptedException:

                print(
                    "Save click intercepted. "
                    "Using JavaScript click..."
                )

                save_button = self.driver.find_element(
                    By.XPATH,
                    self.btnSave
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    save_button
                )

                print(
                    "JavaScript Save click executed"
                )

            # -------------------------------------------------
            # Give server time to process POST
            # -------------------------------------------------

            time.sleep(2)

            print(
                "\n========== AFTER SAVE =========="
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
            # Check success alerts
            # -------------------------------------------------

            success_alerts = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".alert-success"
            )

            print(
                "Success alert count:",
                len(success_alerts)
            )

            for alert in success_alerts:

                if alert.is_displayed():
                    print(
                        "SUCCESS ALERT:",
                        repr(alert.text)
                    )

            # -------------------------------------------------
            # Check ALL alerts
            # -------------------------------------------------

            alerts = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".alert"
            )

            print(
                "Total alert elements:",
                len(alerts)
            )

            for alert in alerts:

                if alert.is_displayed():
                    print(
                        "ALERT:",
                        repr(alert.text)
                    )

            # -------------------------------------------------
            # Check field validation errors
            # -------------------------------------------------

            validation_errors = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".field-validation-error"
            )

            print(
                "Field validation error count:",
                len(validation_errors)
            )

            for error in validation_errors:

                if error.is_displayed():
                    print(
                        "FIELD VALIDATION ERROR:",
                        repr(error.text)
                    )

            # -------------------------------------------------
            # Check validation summary
            # -------------------------------------------------

            validation_summaries = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".validation-summary-errors"
            )

            print(
                "Validation summary count:",
                len(validation_summaries)
            )

            for summary in validation_summaries:

                if summary.is_displayed():
                    print(
                        "VALIDATION SUMMARY:",
                        repr(summary.text)
                    )

            # -------------------------------------------------
            # Check Category Name value after POST
            # -------------------------------------------------

            try:

                name_after_save = self.driver.find_element(
                    By.ID,
                    "Name"
                ).get_attribute("value")

                print(
                    "Category Name after Save:",
                    repr(name_after_save)
                )

            except Exception:

                print(
                    "Category Name field no longer exists."
                )

            # -------------------------------------------------
            # Check URL
            # -------------------------------------------------

            if "/Admin/Category/List" in self.driver.current_url:
                print(
                    "Category save navigation completed."
                )

                return True

            # -------------------------------------------------
            # Success alert may exist without immediate URL
            # -------------------------------------------------

            for alert in success_alerts:

                if alert.is_displayed():
                    print(
                        "Category save appears successful."
                    )

                    return True

            # -------------------------------------------------
            # Save did not complete
            # -------------------------------------------------

            print(
                "\nCategory was NOT saved."
            )

            print(
                "The page remained on:",
                self.driver.current_url
            )

            return False

        except StaleElementReferenceException:

            print(
                "Save button became stale."
            )

            return False

        except TimeoutException:

            print(
                "Timed out locating Save button."
            )

            return False

    # -------------------------------------------------
    # Validate Success Message
    # -------------------------------------------------


    id = "x1m8q4"

    def isCategoryCreatedSuccessfully(self):

        print(
            "\n========== VERIFY CATEGORY CREATION =========="
        )

        try:

            # -------------------------------------------------
            # Wait for navigation back to Category List
            # -------------------------------------------------

            self.wait.until(
                EC.url_contains("/Admin/Category/List")
            )

            print(
                "Current URL after save:",
                self.driver.current_url
            )

            print(
                "Page title after save:",
                self.driver.title
            )

            # -------------------------------------------------
            # Wait for success message
            # -------------------------------------------------

            success_message = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class,'alert-success')]"
                    )
                )
            )

            message = success_message.text.strip()

            print(
                "Category success message:",
                repr(message)
            )

            # -------------------------------------------------
            # Validate expected message
            # -------------------------------------------------

            return (
                    "the new category has been added successfully"
                    in message.lower()
            )

        except TimeoutException:

            print(
                "Category creation success message "
                "was not found"
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



    def generateCategoryName(self):
        category_name = (
            f"Test Category {random.randint(1000,9999)}"
        )
        print("Generated Category Name: ",category_name)
        return category_name


