import os
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException, WebDriverException
)

class AddManufacturer:
    # -------------------------------------------------
    # Catalog / Categories menu
    # -------------------------------------------------

    lnkCatalog_menu_xpath = (
        "//a[@href='#']//p[contains(text(),'Catalog')]"
    )

    lnkManufacturers_menuitem_xpath = (
        "//a[@href='/Admin/Manufacturer/List']"
    )

    # Manufacturer Page
    btnAddNew_Manufacturer = (
        "//a[normalize-space()='Add new']"
    )

    txtManufacturer_Name = (
        "//input[@id='Name']"
    )

    txtManufacturerDesc = (
        "//div[@role='textbox']"
    )

    btnSave = (
        "//button[@name='save']"
    )

    success_msg = (
        "//div[contains(@class,'alert-success')]"
    )

    #constructor
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

    # click Manufacturers SubMenu

    def clickonManufacturersmenuItem(self):
        print("\n========== OPEN MANUFACTURERS MENU ITEM ==========")

        manufacturers_xpath = (
            "//a[@href='/Admin/Manufacturer/List'"
            " and normalize-space()='Manufacturers']"
        )

        for attempt in range(1, 4):
            try:
                print(
                    f"Opening Manufacturer menu Item "
                    f"(attempt {attempt}/3)"
                )

                manufacturers = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            manufacturers_xpath
                        )
                    )
                )

                print("Manufacturers menu item found.")

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    manufacturers
                )

                self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            manufacturers_xpath
                        )
                    )
                )

                try:
                    manufacturers = self.driver.find_element(
                        By.XPATH,
                        manufacturers_xpath
                    )

                    manufacturers.click()

                    print(
                        "Manufacturers menu item clicked "
                        "using normal Selenium click."
                    )

                except ElementClickInterceptedException:
                    print(
                        "Manufacturers click intercepted. "
                        "Using JavaScript click..."
                    )

                    manufacturers = self.driver.find_element(
                        By.XPATH,
                        manufacturers_xpath
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        manufacturers
                    )

                    print(
                        "Manufacturers menu item clicked "
                        "using JavaScript."
                    )

                except StaleElementReferenceException:
                    print(
                        "Manufacturers element became stale. "
                        "Refetching..."
                    )

                    manufacturers = self.wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                manufacturers_xpath
                            )
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        manufacturers
                    )

                    print(
                        "Manufacturers menu item clicked "
                        "after refetching."
                    )

                self.wait.until(
                    EC.url_contains(
                        "/Admin/Manufacturer/List"
                    )
                )

                print(
                    "Manufacturer List page opened successfully."
                )
                print(
                    "Current URL:",
                    self.driver.current_url
                )
                print(
                    "Page title:",
                    self.driver.title
                )

                return True

            except TimeoutException as e:
                print(
                    "Timeout while opening Manufacturer menu item."
                )
                print(
                    "Current URL:",
                    self.driver.current_url
                )
                print(
                    "Page title:",
                    self.driver.title
                )
                print(
                    "Error:",
                    str(e)
                )

                if attempt == 3:
                    raise

                print("Retrying Manufacturer menu item...")
                time.sleep(1)

            except StaleElementReferenceException as e:
                print(
                    "Manufacturer menu item became stale."
                )
                print(
                    "Error:",
                    str(e)
                )

                if attempt == 3:
                    raise

                print("Retrying Manufacturer menu item...")
                time.sleep(1)

            except WebDriverException as e:
                print(
                    "WebDriver error while opening "
                    "Manufacturer menu item:"
                )
                print(
                    type(e).__name__,
                    str(e)
                )

                if attempt == 3:
                    raise

                print("Retrying Manufacturer menu item...")
                time.sleep(1)

        return False

    # Add New
    def clickAddNew(self):
        print(
            "\n========== CLICK ADD NEW MANUFACTURER =========="
        )

        for attempt in range(1, 4):
            try:
                print(
                    f"Opening Manufacturer Create page "
                    f"(attempt {attempt}/3)"
                )

                # -------------------------------------------------
                # Locate exact Manufacturer Add New link
                # -------------------------------------------------

                add_new_xpath = (
                    "//a[@href='/Admin/Manufacturer/Create'"
                    " and normalize-space()='Add new']"
                )

                add_new = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            add_new_xpath
                        )
                    )
                )

                print("Add New link found.")

                # -------------------------------------------------
                # Scroll Add New link into view
                # -------------------------------------------------

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    add_new
                )

                # -------------------------------------------------
                # Verify href before clicking
                # -------------------------------------------------

                href = add_new.get_attribute("href")

                print(
                    "Add New href:",
                    href
                )

                # -------------------------------------------------
                # Wait until clickable
                # -------------------------------------------------

                self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            add_new_xpath
                        )
                    )
                )

                # -------------------------------------------------
                # Try normal Selenium click first
                # -------------------------------------------------

                try:
                    add_new = self.driver.find_element(
                        By.XPATH,
                        add_new_xpath
                    )

                    add_new.click()

                    print(
                        "Normal Selenium click executed"
                    )

                except ElementClickInterceptedException:

                    print(
                        "Add New click intercepted. "
                        "Using JavaScript click..."
                    )

                    add_new = self.driver.find_element(
                        By.XPATH,
                        add_new_xpath
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        add_new
                    )

                    print(
                        "JavaScript click executed"
                    )

                except StaleElementReferenceException:

                    print(
                        "Add New element became stale. "
                        "Refetching element..."
                    )

                    add_new = self.wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                add_new_xpath
                            )
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        add_new
                    )

                    print(
                        "JavaScript click executed "
                        "after refetching"
                    )

                # -------------------------------------------------
                # Wait for navigation
                # -------------------------------------------------

                self.wait.until(
                    EC.url_contains(
                        "/Admin/Manufacturer/Create"
                    )
                )

                print(
                    "Manufacturer Create page opened successfully."
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
                # Wait for Manufacturer Name field
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
                    "Manufacturer Name field is visible."
                )

                return True

            except TimeoutException:

                print(
                    "Manufacturer Create page did not open."
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

                print(
                    "Retrying Manufacturer Add New..."
                )

                time.sleep(1)

            except StaleElementReferenceException:

                print(
                    "Add New element became stale. "
                    "Retrying..."
                )

                if attempt == 3:
                    raise

                time.sleep(1)

            except WebDriverException as e:

                print(
                    "WebDriver error while opening "
                    "Manufacturer Create page:"
                )

                print(
                    type(e).__name__,
                    str(e)
                )

                if attempt == 3:
                    raise

                time.sleep(1)

        return False


    # -------------------------------------------------
    # Enter Manufacturer Name
    # -------------------------------------------------

    def setManufacturerName(self, manufacturer_name):
        print(
            "\n========== SET MANUFACTURER NAME =========="
        )
        print(
            f"Entering manufacturer name: {manufacturer_name}"
        )

        name_locator = (By.ID, "Name")

        for attempt in range(1, 4):
            try:
                print(
                    f"Manufacturer name entry attempt "
                    f"{attempt}/3"
                )

                # -------------------------------------------------
                # Re-find the element on every attempt
                # -------------------------------------------------
                manufacturer_name_field = self.wait.until(
                    EC.element_to_be_clickable(name_locator)
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
                    manufacturer_name_field
                )

                # -------------------------------------------------
                # Re-find after scrolling
                # -------------------------------------------------
                manufacturer_name_field = self.wait.until(
                    EC.element_to_be_clickable(name_locator)
                )

                # -------------------------------------------------
                # Clear existing value
                # -------------------------------------------------
                manufacturer_name_field.click()
                manufacturer_name_field.clear()

                # -------------------------------------------------
                # Enter manufacturer name
                # -------------------------------------------------
                manufacturer_name_field.send_keys(
                    manufacturer_name
                )

                # -------------------------------------------------
                # Verify using fresh DOM lookup
                # -------------------------------------------------
                actual_value = self.driver.execute_script(
                    """
                    return document.getElementById('Name').value;
                    """
                )

                print(
                    f"Manufacturer Name DOM value: "
                    f"{actual_value!r}"
                )

                # -------------------------------------------------
                # Exact verification
                # -------------------------------------------------
                if actual_value == manufacturer_name:
                    print(
                        "Manufacturer Name entered "
                        "successfully."
                    )
                    return True

                print(
                    "Manufacturer name value mismatch."
                    f"\nExpected: {manufacturer_name!r}"
                    f"\nActual:   {actual_value!r}"
                )

            except StaleElementReferenceException:
                print(
                    "Manufacturer Name field became stale. "
                    "Retrying..."
                )

            except Exception as e:
                print(
                    f"Manufacturer name entry attempt "
                    f"{attempt} failed: "
                    f"{type(e).__name__}: {e}"
                )

            if attempt < 3:
                time.sleep(1)

        raise AssertionError(
            "Unable to enter manufacturer name: "
            f"{manufacturer_name}"
        )

    # -------------------------------------------------
    # Enter Manufacturer Description
    # -------------------------------------------------

    def setManufacturerDescription(self,description):
        print("Entering manufacturer description...")
        description_field =self.wait.until(EC.visibility_of_element_located(
            (
                By.XPATH,
                self.txtManufacturerDesc
            )
        ))
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
        print("Manufacturer description entered")
        # Verify text was actually inserted
        print(
            "Description text:",
            repr(description_field.text)
        )

    # -------------------------------------------------
    # Save Manufacturer
    # -------------------------------------------------

    def clickSave(self):
        print("\n========== SAVE MANUFACTURER ==========")

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
            print(
                "Save button text:",
                repr(save_button.text)
            )
            print(
                "Save button enabled:",
                save_button.is_enabled()
            )
            print(
                "Save button displayed:",
                save_button.is_displayed()
            )

            # -------------------------------------------------
            # Scroll Save button into view
            # -------------------------------------------------

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                save_button
            )

            # -------------------------------------------------
            # Capture current Manufacturer Name before Save
            # -------------------------------------------------

            name_value = self.driver.find_element(
                By.ID,
                "Name"
            ).get_attribute("value")

            print(
                "Manufacturer Name before Save:",
                repr(name_value)
            )

            # -------------------------------------------------
            # Click Save
            # -------------------------------------------------

            try:
                save_button.click()

                print(
                    "Normal Selenium save click executed"
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

                try:
                    if alert.is_displayed():
                        print(
                            "SUCCESS ALERT:",
                            repr(alert.text)
                        )

                except Exception:
                    pass

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

                try:
                    if alert.is_displayed():
                        print(
                            "ALERT:",
                            repr(alert.text)
                        )

                except Exception:
                    pass

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

                try:
                    if error.is_displayed():
                        print(
                            "FIELD VALIDATION ERROR:",
                            repr(error.text)
                        )

                except Exception:
                    pass

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

                try:
                    if summary.is_displayed():
                        print(
                            "VALIDATION SUMMARY:",
                            repr(summary.text)
                        )

                except Exception:
                    pass

            # -------------------------------------------------
            # Check Manufacturer Name after POST
            # -------------------------------------------------

            try:

                name_after_save = self.driver.find_element(
                    By.ID,
                    "Name"
                ).get_attribute("value")

                print(
                    "Manufacturer Name after Save:",
                    repr(name_after_save)
                )

            except Exception:

                print(
                    "Manufacturer Name field no longer exists."
                )

            # -------------------------------------------------
            # Check navigation to Manufacturer List
            # -------------------------------------------------

            current_url = self.driver.current_url

            if "/Admin/Manufacturer/List" in current_url:
                print(
                    "Manufacturer save navigation completed."
                )

                return True

            # -------------------------------------------------
            # Success alert may exist without immediate URL
            # -------------------------------------------------

            for alert in success_alerts:

                try:

                    if alert.is_displayed():
                        print(
                            "Manufacturer save appears successful."
                        )

                        return True

                except Exception:
                    pass

            # -------------------------------------------------
            # Save did not complete
            # -------------------------------------------------

            print(
                "\nManufacturer was NOT saved."
            )

            print(
                "The page remained on:",
                self.driver.current_url
            )

            return False

        except Exception as e:

            print(
                "\nManufacturer Save failed."
            )

            print(
                "Exception:",
                type(e).__name__,
                str(e)
            )

            try:
                os.makedirs(
                    "Screenshots",
                    exist_ok=True
                )

                self.driver.save_screenshot(
                    "Screenshots/manufacturer_save_failed.png"
                )

                print(
                    "Screenshot saved:"
                    " Screenshots/manufacturer_save_failed.png"
                )

            except Exception:
                pass

            return False


    # Validate Success Message
    id = "x1m8q4"
    def isManufacturerCreatedSuccessfully(self):
        print(
            "\n========== VERIFY MANUFACTURER CREATION =========="
        )

        try:

            # -------------------------------------------------
            # Wait for navigation back to Manufacturer List
            # -------------------------------------------------

            self.wait.until(
                EC.url_contains("/Admin/Manufacturer/List")
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
                "Manufacturer success message:",
                repr(message)
            )

            # -------------------------------------------------
            # Validate expected message
            # -------------------------------------------------

            return (
                    "the new manufacturer has been added successfully"
                    in message.lower()
            )

        except TimeoutException:

            print(
                "Manufacturer creation success message "
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


    def generateManufacturerName(self):
        manufacturer_name = (
            f"Test Manufacturer {random.randint(1000, 9999)}"
        )
        print("Generated Manufacturer Name: ",manufacturer_name)
        return manufacturer_name








