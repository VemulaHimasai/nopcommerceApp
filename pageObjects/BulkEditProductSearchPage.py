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
        # BULK EDIT PRODUCT TABLE
        #
        # IMPORTANT:
        # Bulk Edit does NOT use #products-grid.
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

        # A REAL product row must contain a name input.
        self.real_product_rows = (
            self.product_table
            + "//tbody//tr"
            "[.//input[contains(@id,'name-')]]"
        )

        # =====================================================
        # NO DATA
        # =====================================================

        self.no_data_xpath = (
            self.product_table
            + "//tbody//td[contains("
            "normalize-space(.),"
            "'No data available in table'"
            ")]"
        )

        # =====================================================
        # PROCESSING INDICATOR
        # =====================================================

        self.processing = (
            "//div[contains(@class,'dataTables_processing')]"
        )

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
            EC.element_to_be_clickable(locator)
        )

        self._scroll_into_view(element)

        try:

            element.click()

        except (
            StaleElementReferenceException,
            ElementClickInterceptedException
        ):

            element = self.wait.until(
                EC.element_to_be_clickable(locator)
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
    # FIND OPTION FROM UNDERLYING SELECT
    # =========================================================

    def _find_select_option_by_text(
        self,
        select_id,
        option_text
    ):

        option_text = option_text.strip()

        script = """
        const select =
            document.getElementById(arguments[0]);

        const wanted =
            arguments[1].trim();

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
    # SELECT2 USING UNDERLYING SELECT
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

                available:
                    Array.from(select.options)
                    .map(function(option) {
                        return (
                            option.textContent || ''
                        ).trim();
                    })
            };
        }

        select.value =
            matchingOption.value;

        select.dispatchEvent(
            new Event(
                'change',
                {
                    bubbles: true
                }
            )
        );

        if (
            window.jQuery &&
            window.jQuery(select).length
        ) {

            window.jQuery(select).trigger(
                'change'
            );
        }

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

    def _verify_select2_value(
        self,
        container_id,
        expected_text
    ):

        expected_text = (
            expected_text
            .strip()
            .lower()
        )

        select_id = (
            container_id
            .replace("select2-", "")
            .replace("-container", "")
        )

        def selected(driver):

            try:

                result = driver.execute_script(
                    """
                    const select =
                        document.getElementById(
                            arguments[0]
                        );

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

                    value:
                        select.value,

                    text:
                        option
                            ? (
                                option.textContent ||
                                ''
                            ).trim()
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
    # CLICK SELECT2 OPTION FROM LIVE DOM
    # =========================================================

    def _click_select2_option(
        self,
        option_text
    ):

        option_text = option_text.strip()

        last_exception = None

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

        print(
            f"Selecting Product Type: "
            f"{product_type}"
        )

        product_type = product_type.strip()

        for attempt in range(1, 4):

            try:

                print(
                    f"Product Type selection "
                    f"(attempt {attempt}/3)"
                )

                dropdown = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            self.drpProducttype
                        )
                    )
                )

                self._scroll_into_view(
                    dropdown
                )

                dropdown.click()

                option_xpath = (
                    "//li[contains("
                    "@class,"
                    "'select2-results__option'"
                    ") and normalize-space(.)="
                    f"'{product_type}']"
                )

                option = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            option_xpath
                        )
                    )
                )

                self._scroll_into_view(
                    option
                )

                self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            option_xpath
                        )
                    )
                ).click()

                container = self.wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.ID,
                            self.productTypeContainerId
                        )
                    )
                )

                selected_text = (
                    container.text or ""
                ).strip()

                print(
                    "Visible Select2 Product Type:",
                    selected_text
                )

                if (
                    selected_text.lower()
                    != product_type.lower()
                ):

                    print(
                        "Visible Select2 value mismatch."
                    )

                    continue

                if self._verify_select2_value(
                    self.productTypeContainerId,
                    product_type
                ):

                    print(
                        f"Product Type "
                        f"'{product_type}' selected"
                    )

                    return

            except StaleElementReferenceException:

                print(
                    "Product Type selection became stale. "
                    "Retrying..."
                )

            except TimeoutException:

                print(
                    "Product Type option was not available. "
                    "Retrying..."
                )

            except ElementClickInterceptedException:

                print(
                    "Product Type option click intercepted. "
                    "Retrying..."
                )

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

    def SelectByVendor(
        self,
        vendor
    ):

        print(
            f"Selecting Vendor: {vendor}"
        )

        vendor = vendor.strip()

        for attempt in range(1, 4):

            try:

                print(
                    f"Vendor selection "
                    f"(attempt {attempt}/3)"
                )

                dropdown = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.drpVendor)
                    )
                )

                self._scroll_into_view(
                    dropdown
                )

                dropdown.click()

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

                self._scroll_into_view(
                    option
                )

                self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, option_xpath)
                    )
                ).click()

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

                if (
                    selected_text.lower()
                    != vendor.lower()
                ):

                    print(
                        "Visible Select2 value mismatch."
                    )

                    continue

                if self._verify_select2_value(
                    self.vendorContainerId,
                    vendor
                ):

                    print(
                        f"Vendor '{vendor}' selected"
                    )

                    return

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

        print(
            "\n========== CLICK SEARCH =========="
        )

        search_clicked = False

        for attempt in range(1, 4):

            try:

                print(
                    f"Search button click "
                    f"(attempt {attempt}/3)"
                )

                search_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, self.btnSearch)
                    )
                )

                self._scroll_into_view(
                    search_button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    search_button
                )

                print(
                    "Search button clicked"
                )

                search_clicked = True
                break

            except StaleElementReferenceException:

                print(
                    "Search button became stale. "
                    "Reacquiring and retrying..."
                )

            except ElementClickInterceptedException:

                print(
                    "Search button click intercepted. "
                    "Retrying..."
                )

            except TimeoutException:

                print(
                    "Search button was not ready. "
                    "Retrying..."
                )

        if not search_clicked:

            raise TimeoutException(
                "Unable to click Search button "
                "after 3 attempts."
            )

        # -----------------------------------------------------
        # Processing START
        # -----------------------------------------------------

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

            print(
                "DataTables processing started"
            )

        except TimeoutException:

            print(
                "DataTables processing indicator "
                "was not observed"
            )

        # -----------------------------------------------------
        # Processing FINISH
        # -----------------------------------------------------

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

            print(
                "DataTables processing completed"
            )

        except TimeoutException:

            print(
                "DataTables processing completion "
                "wait timed out"
            )

        # -----------------------------------------------------
        # Wait for REAL final result
        # -----------------------------------------------------

        try:

            self.wait.until(
                self._search_result_loaded
            )

            print(
                "Bulk Edit search result loaded"
            )

        except TimeoutException:

            print(
                "Timed out waiting for "
                "Bulk Edit search result"
            )

        print(
            "==================================\n"
        )

    # =========================================================
    # SEARCH RESULT STATE
    # =========================================================

    def _search_result_loaded(
        self,
        driver
    ):

        try:

            # -------------------------------------------------
            # 1. Check no-data message
            # -------------------------------------------------

            no_data_elements = driver.find_elements(
                By.XPATH,
                self.no_data_xpath
            )

            for element in no_data_elements:

                try:

                    if element.is_displayed():

                        print(
                            "Bulk Edit search returned "
                            "NO DATA"
                        )

                        return True

                except StaleElementReferenceException:

                    return False

            # -------------------------------------------------
            # 2. Check REAL product rows
            # -------------------------------------------------

            rows = driver.find_elements(
                By.XPATH,
                self.real_product_rows
            )

            if rows:

                print(
                    "Bulk Edit search returned "
                    f"{len(rows)} product rows"
                )

                return True

            # -------------------------------------------------
            # 3. Table may exist but AJAX is still replacing
            #    the tbody.
            # -------------------------------------------------

            table = driver.find_elements(
                By.XPATH,
                self.product_table
            )

            if not table:

                return False

            return False

        except StaleElementReferenceException:

            return False

    # =========================================================
    # GET SEARCH RESULTS
    # =========================================================

    def getSearchResults(self):

        print(
            "\n========== GET SEARCH RESULTS =========="
        )

        # -----------------------------------------------------
        # FIRST: Check whether NO DATA is displayed.
        # -----------------------------------------------------

        try:

            no_data_elements = self.driver.find_elements(
                By.XPATH,
                self.no_data_xpath
            )

            for element in no_data_elements:

                try:

                    if element.is_displayed():

                        print(
                            "No product rows found."
                        )

                        print(
                            "Reason: "
                            "No data available in table"
                        )

                        print(
                            "========================================\n"
                        )

                        return []

                except StaleElementReferenceException:

                    pass

        except Exception:

            pass

        # -----------------------------------------------------
        # SECOND: Find ONLY real product rows.
        #
        # This is the important fix.
        #
        # Do not return DataTables placeholder rows.
        # -----------------------------------------------------

        try:

            rows = self.wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        self.real_product_rows
                    )
                )
            )

            print(
                "Product rows found:",
                len(rows)
            )

            for index, row in enumerate(
                rows[:5],
                start=1
            ):

                try:

                    inputs = row.find_elements(
                        By.XPATH,
                        ".//input"
                    )

                    values = []

                    for input_element in inputs:

                        value = (
                            input_element
                            .get_attribute("value")
                        )

                        if value:

                            values.append(value)

                    print(
                        f"Row {index}:",
                        values
                    )

                except (
                    StaleElementReferenceException
                ):

                    print(
                        f"Unable to read row {index}: "
                        "row became stale"
                    )

                except Exception as e:

                    print(
                        f"Unable to read row {index}:",
                        e
                    )

            print(
                "========================================\n"
            )

            return rows

        except TimeoutException:

            print(
                "No real product rows found "
                "in Bulk Edit table"
            )

            print(
                "========================================\n"
            )

            return []

    # =========================================================
    # WAIT FOR BULK EDIT TABLE LOAD
    # =========================================================

    def wait_for_datatable_load(
        self,
        timeout=30
    ):

        print(
            "\nWaiting for Bulk Edit table "
            "AJAX request to complete..."
        )

        # IMPORTANT:
        #
        # Do NOT use:
        #
        # #products-grid
        #
        # because Bulk Edit does not have that ID.

        try:

            WebDriverWait(
                self.driver,
                timeout,
                poll_frequency=0.2
            ).until(
                self._search_result_loaded
            )

            print(
                "Bulk Edit table search completed."
            )

            return True

        except TimeoutException:

            print(
                "WARNING: Bulk Edit table result "
                "did not appear within timeout."
            )

            return False

    # =========================================================
    # SAVE SCREENSHOT
    # =========================================================

    def save_screenshot(
        self,
        filename
    ):

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

    # =========================================================
    # CHECK NO DATA AVAILABLE
    # =========================================================

    def isNoDataAvailable(self):

        print(
            "\n========== CHECK NO DATA =========="
        )

        try:

            element = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        self.no_data_xpath
                    )
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

            # -------------------------------------------------
            # Diagnostic table body
            # -------------------------------------------------

            try:

                table = self.driver.find_element(
                    By.XPATH,
                    self.product_table
                )

                table_text = self.driver.execute_script(
                    """
                    const table = arguments[0];

                    const tbody =
                        table.querySelector('tbody');

                    if (!tbody) {
                        return 'tbody not found';
                    }

                    return tbody.innerText || '';
                    """,
                    table
                )

                print(
                    "Current Bulk Edit table body:"
                )

                print(
                    table_text
                )

            except Exception as e:

                print(
                    "Unable to read Bulk Edit table:",
                    e
                )

            return False

    # =========================================================
    # GET PRODUCT DATA
    # =========================================================

    def getProductData(self):

        print(
            "\n========== GET PRODUCT DATA =========="
        )

        rows = self.getSearchResults()

        products = []

        for index, row in enumerate(
            rows,
            start=1
        ):

            try:

                # ---------------------------------------------
                # Locate inputs by ID.
                #
                # Do NOT depend on input order.
                # ---------------------------------------------

                name_element = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                )

                sku_element = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'sku-')]"
                )

                price_element = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'price-')]"
                )

                old_price_element = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'old-price-')]"
                )

                quantity_element = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'quantity-')]"
                )

                product = {
                    "name": (
                        name_element
                        .get_attribute("value")
                        or ""
                    ),

                    "sku": (
                        sku_element
                        .get_attribute("value")
                        or ""
                    ),

                    "price": (
                        price_element
                        .get_attribute("value")
                        or ""
                    ),

                    "old_price": (
                        old_price_element
                        .get_attribute("value")
                        or ""
                    ),

                    "quantity": (
                        quantity_element
                        .get_attribute("value")
                        or ""
                    )
                }

                products.append(
                    product
                )

                if index <= 5:

                    print(
                        f"Product {index}:",
                        product
                    )

            except (
                StaleElementReferenceException
            ):

                print(
                    f"Row {index} became stale; skipping."
                )

            except NoSuchElementException as e:

                print(
                    f"Required product input "
                    f"missing in row {index}:",
                    e
                )

            except Exception as e:

                print(
                    f"Unable to read row {index}:",
                    e
                )

        print(
            "Total products extracted:",
            len(products)
        )

        print(
            "======================================\n"
        )

        return products

    # =========================================================
    # CHECK PRODUCT DISPLAYED
    # =========================================================

    def isProductDisplayed(
        self,
        product_name
    ):

        print(
            f"\nChecking whether product is displayed: "
            f"{product_name}"
        )

        product_name = (
            product_name
            .strip()
            .lower()
        )

        # -----------------------------------------------------
        # Wait for either real rows OR no-data.
        # -----------------------------------------------------

        try:

            self.wait.until(
                self._search_result_loaded
            )

        except TimeoutException:

            print(
                "Search result did not load."
            )

            return False

        # -----------------------------------------------------
        # Find ONLY real product rows.
        # -----------------------------------------------------

        rows = self.driver.find_elements(
            By.XPATH,
            self.real_product_rows
        )

        print(
            f"Total real Bulk Edit rows found: "
            f"{len(rows)}"
        )

        for index, row in enumerate(
            rows,
            start=1
        ):

            try:

                name_input = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                )

                actual_name = (
                    name_input
                    .get_attribute("value")
                    or ""
                ).strip()

                print(
                    f"Checking product row {index}: "
                    f"{actual_name}"
                )

                if (
                    actual_name.lower()
                    == product_name
                ):

                    print(
                        f"Product found: {actual_name}"
                    )

                    return True

            except StaleElementReferenceException:

                print(
                    f"Product row {index} became stale."
                )

                continue

            except NoSuchElementException:

                print(
                    f"Product row {index} "
                    "does not contain name input."
                )

                continue

        print(
            f"Product not found: {product_name}"
        )

        return False

    # =========================================================
    # VERIFY ALL SEARCH RESULTS ARE PUBLISHED
    # =========================================================

    def areAllProductsPublished(self):

        print(
            "\n========== VERIFY PUBLISHED PRODUCTS =========="
        )

        rows = self.driver.find_elements(
            By.XPATH,
            self.real_product_rows
        )

        print(
            f"Products returned: {len(rows)}"
        )

        if not rows:

            print(
                "No published product rows found."
            )

            print(
                "=============================================="
            )

            return False

        for index in range(
            1,
            len(rows) + 1
        ):

            try:

                # Reacquire every row using current DOM.
                current_rows = self.driver.find_elements(
                    By.XPATH,
                    self.real_product_rows
                )

                if index > len(current_rows):

                    print(
                        f"Unable to reacquire row {index}"
                    )

                    return False

                row = current_rows[index - 1]

                product_name = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                ).get_attribute("value")

                product_name = (
                    product_name or ""
                ).strip()

                published_checkbox = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'published-')]"
                )

                is_published = (
                    published_checkbox.is_selected()
                )

                print(
                    f"Row {index}: "
                    f"{product_name} | "
                    f"Published = {is_published}"
                )

                if not is_published:

                    print(
                        "FAILED: Unpublished product "
                        f"found: {product_name}"
                    )

                    print(
                        "=============================================="
                    )

                    return False

            except (
                StaleElementReferenceException,
                NoSuchElementException
            ):

                print(
                    f"Unable to verify row {index}"
                )

                return False

        print(
            "All returned products are Published"
        )

        print(
            "=============================================="
        )

        return True

    # =========================================================
    # VERIFY ALL SEARCH RESULTS ARE UNPUBLISHED
    # =========================================================

    def areAllProductsUnpublished(self):

        print(
            "\n========== VERIFY UNPUBLISHED PRODUCTS =========="
        )

        rows = self.driver.find_elements(
            By.XPATH,
            self.real_product_rows
        )

        print(
            f"Products returned: {len(rows)}"
        )

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # If Unpublished Only currently returns:
        #
        # "No data available in table"
        #
        # then there is nothing to verify.
        #
        # Return False because the test should distinguish
        # between "filter returned no products" and
        # "products were returned and all were unpublished."
        # -----------------------------------------------------

        if not rows:

            print(
                "No unpublished product rows returned."
            )

            print(
                "This means the current database contains "
                "no products matching Unpublished Only."
            )

            print(
                "================================================"
            )

            return False

        for index in range(
            1,
            len(rows) + 1
        ):

            try:

                current_rows = self.driver.find_elements(
                    By.XPATH,
                    self.real_product_rows
                )

                if index > len(current_rows):

                    print(
                        f"Unable to reacquire row {index}"
                    )

                    return False

                row = current_rows[index - 1]

                product_name = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'name-')]"
                ).get_attribute("value")

                product_name = (
                    product_name or ""
                ).strip()

                published_checkbox = row.find_element(
                    By.XPATH,
                    ".//input[contains(@id,'published-')]"
                )

                is_published = (
                    published_checkbox.is_selected()
                )

                print(
                    f"Row {index}: "
                    f"{product_name} | "
                    f"Published = {is_published}"
                )

                if is_published:

                    print(
                        "FAILED: Published product found: "
                        f"{product_name}"
                    )

                    print(
                        "================================================"
                    )

                    return False

            except (
                StaleElementReferenceException,
                NoSuchElementException
            ):

                print(
                    f"Unable to verify row {index}"
                )

                return False

        print(
            "All returned products are Unpublished"
        )

        print(
            "================================================"
        )

        return True

    # =========================================================
    # DEBUG PUBLISHED FILTER
    # =========================================================

    def debug_published_filter(self):

        print(
            "\n========== DEBUG PUBLISHED FILTER =========="
        )

        result = self.driver.execute_script(
            """
            const select =
                document.getElementById(
                    'SearchPublishedId'
                );

            if (!select) {

                return {
                    select_found: false
                };
            }

            const selected =
                select.options[
                    select.selectedIndex
                ];

            return {

                select_found: true,

                selected_value:
                    select.value,

                selected_text:
                    selected
                        ? (
                            selected.textContent ||
                            ''
                        ).trim()
                        : '',

                selected_index:
                    select.selectedIndex,

                options:
                    Array.from(
                        select.options
                    ).map(
                        function(option) {

                            return {

                                text:
                                    (
                                        option.textContent ||
                                        ''
                                    ).trim(),

                                value:
                                    option.value,

                                selected:
                                    option.selected
                            };
                        }
                    )
            };
            """
        )

        print(
            "SearchPublishedId state:"
        )

        print(
            result
        )

        print(
            "============================================\n"
        )

        return result

    # =========================================================
    # DEBUG PUBLISHED CONTROLS
    # =========================================================

    def debug_published_controls(self):

        print(
            "\n========== DEBUG ALL PUBLISHED CONTROLS =========="
        )

        result = self.driver.execute_script(
            """
            const selects = Array.from(
                document.querySelectorAll(
                    "select[id='SearchPublishedId'], " +
                    "select[name='SearchPublishedId']"
                )
            );

            const buttons = Array.from(
                document.querySelectorAll(
                    "button"
                )
            ).filter(
                button =>
                    (
                        button.textContent ||
                        ""
                    ).trim() === "Search"
            );

            return {

                currentUrl:
                    window.location.href,

                publishedSelects:
                    selects.map(
                        (
                            select,
                            index
                        ) => ({

                            index: index,

                            id:
                                select.id,

                            name:
                                select.name,

                            value:
                                select.value,

                            selectedText:
                                select.selectedOptions.length
                                    ? (
                                        select
                                            .selectedOptions[0]
                                            .textContent
                                            .trim()
                                    )
                                    : "",

                            formAction:
                                select.form
                                    ? select.form.action
                                    : null,

                            formMethod:
                                select.form
                                    ? select.form.method
                                    : null,

                            visible:
                                !!(
                                    select.offsetWidth ||
                                    select.offsetHeight ||
                                    select.getClientRects()
                                        .length
                                ),

                            parent:
                                select.parentElement
                                    ? select
                                        .parentElement
                                        .outerHTML
                                        .substring(
                                            0,
                                            1500
                                        )
                                    : "",

                            selectHTML:
                                select.outerHTML
                        })
                    ),

                searchButtons:
                    buttons.map(
                        (
                            button,
                            index
                        ) => ({

                            index: index,

                            id:
                                button.id,

                            name:
                                button.name,

                            type:
                                button.type,

                            formAction:
                                button.form
                                    ? button.form.action
                                    : null,

                            formMethod:
                                button.form
                                    ? button.form.method
                                    : null,

                            outerHTML:
                                button.outerHTML
                                .substring(
                                    0,
                                    2000
                                )
                        })
                    )
            };
            """
        )

        print(
            "Current URL:"
        )

        print(
            result["currentUrl"]
        )

        print(
            "\n--- SearchPublishedId elements ---"
        )

        for select in result[
            "publishedSelects"
        ]:

            print(
                select
            )

        print(
            "\n--- Search buttons ---"
        )

        for button in result[
            "searchButtons"
        ]:

            print(
                button
            )

        print(
            "\n=================================================="
        )