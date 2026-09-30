from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ExportManufacturer:

    btnExport = "//button[normalize-space()='Export']"

    btnExportDropdown = (
        "//button[@class='btn btn-success dropdown-toggle']"
    )

    lstExport_xml = (
        "//a[normalize-space()='Export to XML']"
    )

    lstExport_excel = (
        "//a[normalize-space()='Export to Excel']"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # -------------------------------------------------
    # Open Export Dropdown
    # -------------------------------------------------

    def clickExportDropdown(self):

        print(
            "\n========== OPEN EXPORT DROPDOWN =========="
        )

        export_dropdown = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.btnExportDropdown
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
            export_dropdown
        )

        self.driver.execute_script(
            "arguments[0].click();",
            export_dropdown
        )

        print("Export dropdown clicked.")

    # -------------------------------------------------
    # Export Manufacturer to XML
    # -------------------------------------------------

    def exportManufacturerToXML(self):

        print(
            "\n========== EXPORT MANUFACTURER TO XML =========="
        )

        self.clickExportDropdown()

        export_xml = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.lstExport_xml
                )
            )
        )

        print(
            "XML export link found."
        )
        print("\n========== XML LINK DEBUG ==========")

        print(
            "XML href:",
            export_xml.get_attribute("href")
        )

        print(
            "XML download:",
            export_xml.get_attribute("download")
        )

        print(
            "XML target:",
            export_xml.get_attribute("target")
        )

        print(
            "XML outerHTML:",
            export_xml.get_attribute("outerHTML")
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            export_xml
        )

        self.driver.execute_script(
            "arguments[0].click();",
            export_xml
        )

        print(
            "XML export link clicked."
        )

    # -------------------------------------------------
    # Export Manufacturer to Excel
    # -------------------------------------------------

    def exportManufacturerToExcel(self):

        print(
            "\n========== EXPORT MANUFACTURER TO EXCEL =========="
        )

        self.clickExportDropdown()

        export_excel = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.lstExport_excel
                )
            )
        )

        print(
            "Excel export link found."
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            export_excel
        )

        self.driver.execute_script(
            "arguments[0].click();",
            export_excel
        )

        print(
            "Excel export link clicked."
        )