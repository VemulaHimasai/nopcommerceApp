import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
    ElementClickInterceptedException
)


class BulkEditProductSearchPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            20,
            poll_frequency=0.2
        )

        # =====================================================
        # SEARCH PRODUCT NAME
        # =====================================================

        self.txtsearchproduct_name = (
            "//input[@id='SearchProductName']"
        )

        # =====================================================
        # SELECT2 DROPDOWNS
        # =====================================================

        self.drpVendor = (
            "//label[normalize-space()='Vendor']"
            "/ancestor::div[contains(@class,'form-group')][1]"
            "//span[contains(@class,'select2-selection') "
            "and @role='combobox']"
        )

        self.drpProducttype = (
            "//span[@role='combobox' "
            "and @aria-labelledby="
            "'select2-SearchProductTypeId-container']"
        )

        self.drpPublishedtype = (
            "//span[@role='combobox' "
            "and @aria-labelledby="
            "'select2-SearchPublishedId-container']"
        )

        # =====================================================
        # UNDERLYING SELECT ELEMENTS
        # =====================================================

        self.selectProductType = (
            "//select[@id='SearchProductTypeId']"
        )

        self.selectPublishedType = (
            "//select[@id='SearchPublishedId']"
        )

        self.selectVendor = (
            "//select[@id='SearchVendorId']"
        )

        # =====================================================
        # SELECT2 DISPLAY CONTAINERS
        # =====================================================

        self.productTypeContainerId = (
            "select2-SearchProductTypeId-container"
        )

        self.publishedTypeContainerId = (
            "select2-SearchPublishedId-container"
        )

        self.vendorContainerId = (
            "select2-SearchVendorId-container"
        )

        # =====================================================
        # SEARCH BUTTON
        # =====================================================

        self.btnSearch = (
            "//button[normalize-space()='Search']"
        )

        # =====================================================
        # PRODUCT TABLE
        # =====================================================

        self.product_table = (
            "//table[contains(@class,'table-hover') "
            "and contains(@class,'table-bordered') "
            "and contains(@class,'table-striped')]"
        )

        self.product_rows = (
            self.product_table
            + "//tbody//tr"
        )

        # =====================================================
        # PROCESSING INDICATOR
        # =====================================================

        self.processing = "//div[contains(@class,'dataTables_processing')]"

    # =========================================================
    # GENERIC SCROLL
    # =========================================================

    def _scroll_into_view(self, element):

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            element
        )

        time.sleep(0.2)

    # =========================================================
    # GENERIC NORMAL CLICK
    # =========================================================

    def _normal_click(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(
                locator
            )
        )

        self._scroll_into_view(element)

        try:

            element.click()

        except (
            StaleElementReferenceException,
            ElementClickInterceptedException
        ):

            element = self.wait.until(
                EC.element_to_be_clickable(
                    locator
                )
            )

            self._scroll_into_view(element)

            element.click()

        return True

    # =========================================================
    # GENERIC SCROLL + JS CLICK
    # =========================================================

    def _scroll_and_js_click(self, element):

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            element
        )

        time.sleep(0.2)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    # =========================================================
    # SELECT2 POPUP DETECTION
    # =========================================================

    def _wait_for_select2_popup(self):

        def popup_exists(driver):

            try:

                return bool(
                    driver.execute_script(
                        """
                        const containers =
                            Array.from(
                                document.querySelectorAll(
                                    '.select2-container--open'
                                )
                            );

                        for (const container of containers) {

                            const style =
                                window.getComputedStyle(
                                    container
                                );

                            if (
                                style.display !== 'none' &&
                                style.visibility !== 'hidden'
                            ) {
                                return true;
                            }
                        }

                        return false;
                        """
                    )
                )

            except Exception:

                return False

        try:

            WebDriverWait(
                self.driver,
                5,
                poll_frequency=0.2
            ).until(popup_exists)

            print(
                "Select2 dropdown is open"
            )

            return True

        except TimeoutException:

            print(
                "Select2 popup was not detected."
            )

            return False

    # =========================================================
    # GET OPTION FROM UNDERLYING SELECT
    # =========================================================

    def _find_select_option_by_text(
        self,
        select_id,
        option_text
    ):

        option_text = option_text.strip()

        script = """
        const select = document.getElementById(arguments[0]);
        const wanted = arguments[1].trim();

        if (!select) {
            return null;
        }

        const options =
            Array.from(select.options);

        for (const option of options) {

            const text =
                (option.textContent || '').trim();

            if (text === wanted) {

                return {
                    value: option.value,
                    text: text
                };
            }
        }

        return null;
        """

        try:

            return self.driver.execute_script(
                script,
                select_id,
                option_text
            )

        except Exception:

            return None

    # =========================================================
    # SELECT2 OPTION USING UNDERLYING SELECT
    # =========================================================

    def _select2_by_underlying_select(
            self,
            select_id,
            container_id,
            option_text
    ):

        option_text = option_text.strip()

        script = """
        const select =
            document.getElementById(arguments[0]);

        const wanted =
            arguments[1].trim();

        if (!select) {
            return {
                success: false,
                reason: 'select-not-found'
            };
        }

        let matchingOption = null;

        for (
            const option of Array.from(select.options)
        ) {

            const text =
                (option.textContent || '').trim();

            if (text === wanted) {

                matchingOption = option;
                break;
            }
        }

        if (!matchingOption) {

            return {
                success: false,
                reason: 'option-not-found',
                available: Array.from(
                    select.options
                ).map(function(option) {
                    return (
                        option.textContent || ''
                    ).trim();
                })
            };
        }

        /*
         * Set the underlying select value.
         */

        select.value =
            matchingOption.value;

        /*
         * Trigger native change event.
         */

        select.dispatchEvent(
            new Event(
                'change',
                {
                    bubbles: true
                }
            )
        );

        /*
         * Trigger jQuery / Select2 change event.
         */

        if (
            window.jQuery &&
            window.jQuery(select).length
        ) {

            window.jQuery(select).trigger(
                'change'
            );
        }

        /*
         * Return the selected value.
         */

        return {
            success: true,
            value: matchingOption.value,
            text: (
                matchingOption.textContent ||
                ''
            ).trim()
        };
        """

        try:

            result = self.driver.execute_script(
                script,
                select_id,
                option_text
            )

            if result and result.get("success"):
                print(
                    f"Underlying Select2 select "
                    f"updated: {option_text}"
                )

                return True

            if result:

                print(
                    f"Underlying select could not "
                    f"find '{option_text}'. "
                    f"Reason: "
                    f"{result.get('reason')}"
                )

                available = result.get(
                    "available",
                    []
                )

                if available:
                    print(
                        "Available options:",
                        available
                    )

            return False

        except Exception as e:

            print(
                "Underlying Select2 selection "
                f"failed: {e}"
            )

            return False

    # =========================================================
    # VERIFY SELECT2 VALUE
    # =========================================================

    def _select2_dropdown_text(
        self,
        container_id
    ):

        try:

            return self.driver.execute_script(
                """
                const element =
                    document.getElementById(
                        arguments[0]
                    );

                if (!element) {
                    return '';
                }

                return (
                    element.textContent || ''
                ).trim();
                """,
                container_id
            )

        except Exception:

            return ""

    # =========================================================
    # VERIFY SELECT2 VALUE
    # =========================================================

    def _verify_select2_value(
            self,
            container_id,
            expected_text
    ):

        expected_text = expected_text.strip().lower()

        # Convert:
        # select2-SearchPublishedId-container
        # into:
        # SearchPublishedId
        select_id = container_id.replace(
            "select2-", ""
        ).replace(
            "-container", ""
        )

        def selected(driver):

            try:

                result = driver.execute_script(
                    """
                    const select =
                        document.getElementById(arguments[0]);

                    if (!select) {
                        return false;
                    }

                    const option =
                        select.options[
                            select.selectedIndex
                        ];

                    if (!option) {
                        return false;
                    }

                    const text =
                        (option.textContent || '')
                        .trim()
                        .toLowerCase();

                    return text === arguments[1];
                    """,
                    select_id,
                    expected_text
                )

                return bool(result)

            except Exception:

                return False

        try:

            return self.wait.until(selected)

        except TimeoutException:

            actual = self.driver.execute_script(
                """
                const select =
                    document.getElementById(arguments[0]);

                if (!select) {
                    return {
                        found: false
                    };
                }

                const option =
                    select.options[
                        select.selectedIndex
                    ];

                return {
                    found: true,
                    value: select.value,
                    text: option
                        ? (option.textContent || '').trim()
                        : ''
                };
                """,
                select_id
            )

            print(
                "Select2 underlying value verification "
                f"failed. Expected: '{expected_text}', "
                f"Actual: {actual}"
            )

            return False


    # =========================================================
    # FALLBACK: OPEN SELECT2
    # =========================================================

    def _open_select2_dropdown(
        self,
        dropdown_locator
    ):

        # -----------------------------------------------------
        # First attempt: normal Selenium click.
        # -----------------------------------------------------

        try:

            element = self.wait.until(
                EC.element_to_be_clickable(
                    dropdown_locator
                )
            )

            self._scroll_into_view(element)

            element.click()

            time.sleep(0.4)

            if self._wait_for_select2_popup():

                return True

        except (
            StaleElementReferenceException,
            ElementClickInterceptedException,
            TimeoutException
        ):

            pass

        # -----------------------------------------------------
        # Second attempt: reacquire and JavaScript click.
        # -----------------------------------------------------

        try:

            element = self.wait.until(
                EC.element_to_be_clickable(
                    dropdown_locator
                )
            )

            self._scroll_and_js_click(
                element
            )

            time.sleep(0.5)

            if self._wait_for_select2_popup():

                return True

        except (
            StaleElementReferenceException,
            ElementClickInterceptedException,
            TimeoutException
        ):

            pass

        return False

    # =========================================================
    # FALLBACK: CLICK SELECT2 OPTION FROM LIVE DOM
    # =========================================================

    def _click_select2_option(
        self,
        option_text
    ):

        option_text = option_text.strip()

        last_exception = None

        # -----------------------------------------------------
        # Wait briefly for the option.
        # -----------------------------------------------------

        try:

            self.wait.until(
                lambda driver:
                self._select2_option_exists_js(
                    option_text
                )
            )

        except TimeoutException as e:

            last_exception = e

            print(
                f"Select2 option '{option_text}' "
                f"was not detected."
            )

            # -------------------------------------------------
            # Print diagnostic options.
            # -------------------------------------------------

            try:

                visible_options = (
                    self.driver.execute_script(
                        """
                        return Array.from(
                            document.querySelectorAll(
                                'li.select2-results__option'
                            )
                        )
                        .filter(function(option) {

                            const style =
                                window.getComputedStyle(
                                    option
                                );

                            return (
                                style.display !== 'none' &&
                                style.visibility !== 'hidden' &&
                                option.offsetParent !== null
                            );
                        })
                        .map(function(option) {

                            return (
                                option.textContent || ''
                            ).trim();

                        });
                        """
                    )
                )

                print(
                    "Visible Select2 options:",
                    visible_options
                )

            except Exception:

                pass

            raise TimeoutException(
                f"Select2 option "
                f"'{option_text}' did not appear."
            ) from last_exception

        # -----------------------------------------------------
        # Click from live DOM.
        # -----------------------------------------------------

        for attempt in range(1, 6):

            try:

                print(
                    f"Looking for Select2 option "
                    f"'{option_text}' "
                    f"(attempt {attempt}/5)"
                )

                clicked = self.driver.execute_script(
                    """
                    const wanted =
                        arguments[0].trim();

                    const options =
                        Array.from(
                            document.querySelectorAll(
                                'li.select2-results__option'
                            )
                        );

                    for (const option of options) {

                        const style =
                            window.getComputedStyle(
                                option
                            );

                        const visible =
                            style.display !== 'none' &&
                            style.visibility !== 'hidden' &&
                            option.offsetParent !== null;

                        if (!visible) {
                            continue;
                        }

                        const text =
                            (
                                option.textContent || ''
                            ).trim();

                        if (text === wanted) {

                            option.scrollIntoView({
                                block: 'center',
                                inline: 'nearest'
                            });

                            option.click();

                            return true;
                        }
                    }

                    return false;
                    """,
                    option_text
                )

                if clicked:

                    print(
                        f"Select2 option clicked: "
                        f"{option_text}"
                    )

                    return True

            except Exception as e:

                last_exception = e

                print(
                    "Select2 live-DOM click failed. "
                    f"Retrying ({attempt}/5)..."
                )

            time.sleep(0.3)

        raise TimeoutException(
            f"Unable to select Select2 option: "
            f"{option_text}"
        ) from last_exception

    # =========================================================
    # CHECK SELECT2 OPTION
    # =========================================================

    def _select2_option_exists_js(
        self,
        option_text
    ):

        option_text = option_text.strip()

        try:

            return bool(
                self.driver.execute_script(
                    """
                    const wanted =
                        arguments[0].trim();

                    const options =
                        Array.from(
                            document.querySelectorAll(
                                'li.select2-results__option'
                            )
                        );

                    for (const option of options) {

                        const style =
                            window.getComputedStyle(
                                option
                            );

                        const visible =
                            style.display !== 'none' &&
                            style.visibility !== 'hidden' &&
                            option.offsetParent !== null;

                        if (!visible) {
                            continue;
                        }

                        const text =
                            (
                                option.textContent || ''
                            ).trim();

                        if (text === wanted) {
                            return true;
                        }
                    }

                    return false;
                    """,
                    option_text
                )
            )

        except Exception:

            return False

    # =========================================================
    # SELECT BY PRODUCT TYPE
    # =========================================================

    def SelectByProductType(
        self,
        product_type
    ):

        product_type = product_type.strip()

        print(
            f"Selecting Product Type: "
            f"{product_type}"
        )

        # -----------------------------------------------------
        # PRIMARY METHOD
        # Use underlying Select2 <select>.
        # -----------------------------------------------------

        for attempt in range(1, 4):

            print(
                "Product Type selection "
                f"(attempt {attempt}/3)"
            )

            selected = (
                self._select2_by_underlying_select(
                    "SearchProductTypeId",
                    self.productTypeContainerId,
                    product_type
                )
            )

            if selected:

                if self._verify_select2_value(
                    self.productTypeContainerId,
                    product_type
                ):

                    print(
                        f"Product Type "
                        f"'{product_type}' selected"
                    )

                    return

            time.sleep(0.5)

        # -----------------------------------------------------
        # FALLBACK
        # Use actual Select2 UI.
        # -----------------------------------------------------

        print(
            "Falling back to Select2 UI "
            "for Product Type"
        )

        for attempt in range(1, 4):

            try:

                opened = (
                    self._open_select2_dropdown(
                        (
                            By.XPATH,
                            self.drpProducttype
                        )
                    )
                )

                if not opened:

                    continue

                self._click_select2_option(
                    product_type
                )

                if self._verify_select2_value(
                    self.productTypeContainerId,
                    product_type
                ):

                    print(
                        f"Product Type "
                        f"'{product_type}' selected"
                    )

                    return

            except (
                TimeoutException,
                StaleElementReferenceException,
                NoSuchElementException,
                ElementClickInterceptedException
            ):

                pass

            time.sleep(0.5)

        raise TimeoutException(
            f"Unable to select Product Type: "
            f"{product_type}"
        )

    # =========================================================
    # SELECT BY PUBLISHED TYPE
    # =========================================================

    def SelectByPublishedType(
        self,
        published_type
    ):

        published_type = published_type.strip()

        print(
            f"Selecting Published Type: "
            f"{published_type}"
        )

        # -----------------------------------------------------
        # PRIMARY METHOD
        # -----------------------------------------------------

        for attempt in range(1, 4):

            print(
                "Published Type selection "
                f"(attempt {attempt}/3)"
            )

            selected = (
                self._select2_by_underlying_select(
                    "SearchPublishedId",
                    self.publishedTypeContainerId,
                    published_type
                )
            )

            if selected:

                if self._verify_select2_value(
                    self.publishedTypeContainerId,
                    published_type
                ):

                    print(
                        f"Published Type "
                        f"'{published_type}' selected"
                    )

                    return

            time.sleep(0.5)

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        print(
            "Falling back to Select2 UI "
            "for Published Type"
        )

        for attempt in range(1, 4):

            try:

                opened = (
                    self._open_select2_dropdown(
                        (
                            By.XPATH,
                            self.drpPublishedtype
                        )
                    )
                )

                if not opened:

                    continue

                self._click_select2_option(
                    published_type
                )

                if self._verify_select2_value(
                    self.publishedTypeContainerId,
                    published_type
                ):

                    print(
                        f"Published Type "
                        f"'{published_type}' selected"
                    )

                    return

            except (
                TimeoutException,
                StaleElementReferenceException,
                NoSuchElementException,
                ElementClickInterceptedException
            ):

                pass

            time.sleep(0.5)

        raise TimeoutException(
            "Unable to select Published Type: "
            f"{published_type}"
        )

    # =========================================================
    # SELECT BY VENDOR
    # =========================================================


    def SelectByVendor(self, vendor):

        print(f"Selecting Vendor: {vendor}")

        vendor = vendor.strip()

        for attempt in range(1, 4):

            try:

                print(
                    f"Vendor selection "
                    f"(attempt {attempt}/3)"
                )

                # -----------------------------------------
                # 1. Locate the actual Select2 container
                # -----------------------------------------
                dropdown = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.drpVendor)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    dropdown
                )

                # Click the real Select2 control
                dropdown.click()

                # -----------------------------------------
                # 2. Wait for Select2 results
                # -----------------------------------------
                option_xpath = (
                    "//li[contains("
                    "@class,"
                    "'select2-results__option'"
                    ") and normalize-space(.)="
                    f"'{vendor}']"
                )

                option = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, option_xpath)
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    option
                )

                # -----------------------------------------
                # 3. Click the actual Vendor1 option
                # -----------------------------------------
                self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, option_xpath)
                    )
                ).click()

                # -----------------------------------------
                # 4. Verify visible Select2 text
                # -----------------------------------------
                container = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.vendorContainerId
                        )
                    )
                )

                selected_text = (
                        container.text or ""
                ).strip()

                print(
                    "Visible Select2 Vendor:",
                    selected_text
                )

                if selected_text.lower() != vendor.lower():
                    print(
                        "Visible Select2 value mismatch. "
                        f"Expected: {vendor}, "
                        f"Actual: {selected_text}"
                    )

                    continue

                # -----------------------------------------
                # 5. Verify underlying select
                # -----------------------------------------
                if self._verify_select2_value(
                        self.vendorContainerId,
                        vendor
                ):
                    print(
                        f"Vendor '{vendor}' selected"
                    )

                    return

                print(
                    "Underlying Vendor select "
                    "verification failed"
                )

            except StaleElementReferenceException:

                print(
                    "Vendor selection became stale. "
                    "Retrying..."
                )

            except TimeoutException:

                print(
                    "Vendor option was not available. "
                    "Retrying..."
                )

            except ElementClickInterceptedException:

                print(
                    "Vendor option click intercepted. "
                    "Retrying..."
                )

        raise TimeoutException(
            f"Unable to select vendor: {vendor}"
        )



    # =========================================================
    # SET PRODUCT NAME
    # =========================================================

    def setProductName(
        self,
        product_name
    ):

        product_name = product_name.strip()

        print(
            f"Setting Product Name: "
            f"{product_name}"
        )

        for attempt in range(1, 8):

            try:

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            self.txtsearchproduct_name
                        )
                    )
                )

                self._scroll_into_view(
                    element
                )

                # -------------------------------------------------
                # Focus and clear through JS.
                # This avoids Firefox stale-element problems.
                # -------------------------------------------------

                self.driver.execute_script(
                    """
                    const input = arguments[0];

                    input.focus();

                    input.value = '';

                    input.dispatchEvent(
                        new Event(
                            'input',
                            {
                                bubbles: true
                            }
                        )
                    );

                    input.dispatchEvent(
                        new Event(
                            'change',
                            {
                                bubbles: true
                            }
                        )
                    );
                    """,
                    element
                )

                # -------------------------------------------------
                # Reacquire before send_keys.
                # -------------------------------------------------

                element = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.txtsearchproduct_name
                        )
                    )
                )

                element.send_keys(
                    product_name
                )

                # -------------------------------------------------
                # Verify.
                # -------------------------------------------------

                current_value = self.driver.execute_script(
                    """
                    const input =
                        document.getElementById(
                            'SearchProductName'
                        );

                    return input
                        ? input.value
                        : '';
                    """
                )

                if current_value == product_name:

                    print(
                        "Product Name entered successfully:"
                        f" {product_name}"
                    )

                    return

            except (
                StaleElementReferenceException,
                NoSuchElementException,
                ElementClickInterceptedException,
                TimeoutException
            ) as e:

                print(
                    "Product name entry failed. "
                    f"Retrying ({attempt}/7)... "
                    f"{type(e).__name__}"
                )

                time.sleep(0.4)

        raise TimeoutException(
            f"Unable to enter Product Name: "
            f"{product_name}"
        )

    # =========================================================
    # CLICK SEARCH
    # =========================================================



    def clickSearch(self):
        print("\n========== CLICK SEARCH ==========")

        search_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.btnSearch)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_button
        )

        search_button.click()

        print("Search button clicked")

        # -------------------------------------------------
        # Wait for DataTables processing to START
        # -------------------------------------------------
        try:
            WebDriverWait(
                self.driver,
                5,
                poll_frequency=0.1
            ).until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.processing)
                )
            )

            print("DataTables processing started")

        except TimeoutException:
            # Processing may be extremely fast, so don't fail here.
            print(
                "DataTables processing indicator "
                "was not observed"
            )

        # -------------------------------------------------
        # Wait for DataTables processing to FINISH
        # -------------------------------------------------
        try:
            WebDriverWait(
                self.driver,
                20,
                poll_frequency=0.2
            ).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, self.processing)
                )
            )

            print("DataTables processing completed")

        except TimeoutException:
            print(
                "DataTables processing completion "
                "wait timed out"
            )

        # -------------------------------------------------
        # Wait until the table has a REAL final result
        # -------------------------------------------------
        def result_loaded(driver):

            try:

                # Check "No data available in table"
                no_data_elements = driver.find_elements(
                    By.XPATH,
                    self.product_table
                    + "//tbody//td[contains("
                      "normalize-space(),"
                      "'No data available in table'"
                      ")]"
                )

                for element in no_data_elements:

                    try:
                        if element.is_displayed():
                            print(
                                "Bulk Edit search returned NO DATA"
                            )

                            return True

                    except StaleElementReferenceException:
                        return False

                # Check actual product rows
                rows = driver.find_elements(
                    By.XPATH,
                    self.product_rows
                    + "[.//input[contains(@id,'name-')]]"
                )

                if rows:
                    print(
                        "Bulk Edit search returned "
                        f"{len(rows)} product rows"
                    )

                    return True

                return False

            except StaleElementReferenceException:
                return False

        try:

            self.wait.until(result_loaded)

            print(
                "Bulk Edit search result loaded"
            )

        except TimeoutException:

            print(
                "Timed out waiting for "
                "Bulk Edit search result"
            )

        print("==================================\n")



    # =========================================================
    # GET SEARCH RESULTS
    # =========================================================

    def getSearchResults(self):

        print("\n========== GET SEARCH RESULTS ==========")

        try:
            rows = self.wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        self.product_rows
                        + "[not(td[contains("
                          "normalize-space(),"
                          "'No data available in table'"
                          ")])]"
                    )
                )
            )

            print("Product rows found:", len(rows))

            for index, row in enumerate(rows[:5], start=1):

                try:
                    inputs = row.find_elements(
                        By.XPATH,
                        ".//input"
                    )

                    values = []

                    for input_element in inputs:
                        value = input_element.get_attribute(
                            "value"
                        )

                        if value:
                            values.append(value)

                    print(
                        f"Row {index}:",
                        values
                    )

                except Exception as e:
                    print(
                        f"Unable to read row {index}:",
                        e
                    )

            print("========================================\n")

            return rows

        except TimeoutException:

            print(
                "No product rows found "
                "in Bulk Edit table"
            )

            return []



    def wait_for_datatable_load(self, timeout=30):

        print("\nWaiting for DataTable AJAX request to complete...")

        try:

            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("""
                    if (
                        !window.jQuery ||
                        !jQuery.fn ||
                        !jQuery.fn.dataTable
                    ) {
                        return false;
                    }

                    if (
                        !jQuery.fn.dataTable.isDataTable(
                            '#products-grid'
                        )
                    ) {
                        return false;
                    }

                    const dt =
                        jQuery('#products-grid').DataTable();

                    const settings =
                        dt.settings()[0];

                    return (
                        settings &&
                        settings.json !== undefined &&
                        settings.json !== null
                    );
                """)
            )

            print("DataTable AJAX request completed.")

        except TimeoutException:

            print(
                "WARNING: DataTable AJAX request did not "
                "complete within timeout."
            )

            return False

        return True
    # =========================================================
    # SAVE SCREENSHOT
    # =========================================================

    def save_screenshot(self, filename):

        import os

        screenshot_dir = os.path.join(
            os.getcwd(),
            "Screenshots"
        )

        os.makedirs(
            screenshot_dir,
            exist_ok=True
        )

        screenshot_path = os.path.join(
            screenshot_dir,
            filename
        )

        self.driver.save_screenshot(
            screenshot_path
        )

        print(
            f"Screenshot saved: {screenshot_path}"
        )

        return screenshot_path

    def isNoDataAvailable(self):

        print("\n========== CHECK NO DATA ==========")

        no_data_xpath = (
                self.product_table
                + "//tbody//td[contains("
                  "normalize-space(),"
                  "'No data available in table'"
                  ")]"
        )

        try:
            element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, no_data_xpath)
                )
            )

            print(
                "No data message found:",
                element.text
            )

            return True

        except TimeoutException:

            print(
                "No data message was not found."
            )

            try:
                table_text = self.driver.execute_script(
                    """
                    const table = arguments[0];

                    if (!table) {
                        return 'table not found';
                    }

                    const tbody =
                        table.querySelector('tbody');

                    if (!tbody) {
                        return 'tbody not found';
                    }

                    return tbody.innerText || '';
                    """,
                    self.driver.find_element(
                        By.XPATH,
                        self.product_table
                    )
                )

                print(
                    "Current Bulk Edit table body:"
                )
                print(table_text)

            except Exception as e:
                print(
                    "Unable to read Bulk Edit table:",
                    e
                )

            return False

    def getProductData(self):

        print("\n========== GET PRODUCT DATA ==========")

        rows = self.getSearchResults()

        products = []

        for index, row in enumerate(rows, start=1):

            try:
                inputs = row.find_elements(
                    By.XPATH,
                    ".//input"
                )

                values = []

                for element in inputs:
                    value = element.get_attribute("value")

                    if value:
                        values.append(value)

                if len(values) >= 6:

                    product = {
                        "name": values[1],
                        "sku": values[2],
                        "price": values[3],
                        "old_price": values[4],
                        "quantity": values[5]
                    }

                    products.append(product)

                    if index <= 5:
                        print(
                            f"Product {index}:",
                            product
                        )

            except StaleElementReferenceException:
                print(
                    f"Row {index} became stale; skipping."
                )

            except Exception as e:
                print(
                    f"Unable to read row {index}: {e}"
                )

        print(
            "Total products extracted:",
            len(products)
        )

        print("======================================\n")

        return products

    def isProductDisplayed(self, product_name):

        print(
            f"\nChecking whether product is displayed: {product_name}"
        )

        product_name = product_name.strip().lower()

        # Wait until the Bulk Edit table is present
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//table[contains(@class,'table-hover') "
                    "and contains(@class,'table-bordered') "
                    "and contains(@class,'table-striped')]"
                )
            )
        )

        rows = self.driver.find_elements(
            By.XPATH,
            "//table[contains(@class,'table-hover') "
            "and contains(@class,'table-bordered') "
            "and contains(@class,'table-striped')]"
            "//tbody/tr"
        )

        print(f"Total Bulk Edit rows found: {len(rows)}")

        for index, row in enumerate(rows, start=1):

            try:
                # Get product-name input from this row
                name_inputs = row.find_elements(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                )

                if not name_inputs:
                    print(
                        f"Checking product row {index}: "
                        "name input not found"
                    )
                    continue

                actual_name = (
                        name_inputs[0]
                        .get_attribute("value")
                        or ""
                ).strip()

                print(
                    f"Checking product row {index}: "
                    f"{actual_name}"
                )

                if actual_name.lower() == product_name:
                    print(
                        f"Product found: {actual_name}"
                    )
                    return True

            except StaleElementReferenceException:
                print(
                    f"Product row {index} became stale. "
                    "Re-reading rows..."
                )

                # Re-read rows and continue searching
                rows = self.driver.find_elements(
                    By.XPATH,
                    "//table[contains(@class,'table-hover') "
                    "and contains(@class,'table-bordered') "
                    "and contains(@class,'table-striped')]"
                    "//tbody/tr"
                )

                continue

        print(
            f"Product not found: {product_name}"
        )

        return False