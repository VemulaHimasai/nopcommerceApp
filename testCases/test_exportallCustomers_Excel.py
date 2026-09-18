import os
import time
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddCustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer

from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen
from utilities.download_utils import (
    clear_downloads,
    wait_for_download
)


class Test_ExportAllCustomers_Excel_008:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_export_all_customers(self, setup):

        self.logger.info(
            "******* Exporting All Customers to Excel *******"
        )

        # =================================================
        # Browser setup
        # =================================================

        self.driver = setup

        print(
            "Application URL:",
            self.baseURL
        )

        self.driver.get(self.baseURL)

        self.driver.maximize_window()

        print(
            "Current URL:",
            self.driver.current_url
        )

        print(
            "Page title:",
            self.driver.title
        )

        # Keep implicit wait only for existing project
        # compatibility.
        self.driver.implicitly_wait(10)

        # =================================================
        # Download directory
        # =================================================

        download_dir = os.path.abspath(
            os.path.join(
                os.getcwd(),
                "downloads"
            )
        )

        os.makedirs(
            download_dir,
            exist_ok=True
        )

        print(
            "Download directory:",
            download_dir
        )

        # =================================================
        # Clear previous downloads
        # =================================================

        clear_downloads(
            download_dir
        )

        self.logger.info(
            "******* Previous downloads cleared *******"
        )

        # =================================================
        # Login
        # =================================================

        self.lp = LoginPage(
            self.driver
        )

        self.lp.setUserName(
            self.username
        )

        self.lp.setPassword(
            self.password
        )

        self.lp.clickLogin()

        self.logger.info(
            "******* Login Successful *****"
        )

        # =================================================
        # Navigate to Customers
        # =================================================

        self.logger.info(
            "****** Starting Export All Customers *******"
        )

        self.addcust = AddCustomer(
            self.driver
        )

        self.addcust.clickOnCustomersMenu()

        self.addcust.clickonCustomersMenuItem()

        self.logger.info(
            "****** Customers page opened ******"
        )

        print(
            "Customers page URL:",
            self.driver.current_url
        )

        # =================================================
        # Search Customer page object
        # =================================================

        searchcust = SearchCustomer(
            self.driver
        )

        # -------------------------------------------------
        # Allow Customers DataTable to load
        # -------------------------------------------------

        time.sleep(2)

        # =================================================
        # Open Export dropdown
        # =================================================

        print(
            "Opening Export dropdown..."
        )

        searchcust.clickExport()

        time.sleep(1)

        # =================================================
        # Click Export All Excel
        # =================================================

        print(
            "Clicking Export All Excel..."
        )

        searchcust.clickExportAll_Excel()

        self.logger.info(
            "******* Export All Customers Excel "
            "button clicked *******"
        )

        # =================================================
        # Wait for Excel download
        # =================================================

        print(
            "\nWaiting for Excel download..."
        )

        excel_file = wait_for_download(
            download_dir,
            ".xlsx",
            timeout=60
        )

        self.logger.info(
            "******* Excel Downloaded Successfully: "
            f"{excel_file} *******"
        )

        print(
            "Excel file returned by download utility:",
            excel_file
        )

        # =================================================
        # Build full file path
        # =================================================

        excel_path = os.path.join(
            download_dir,
            excel_file
        )

        print(
            "Excel file path:",
            excel_path
        )

        # =================================================
        # Verify file exists
        # =================================================

        assert os.path.exists(
            excel_path
        ), (
            "Excel file was not found in downloads folder: "
            f"{excel_path}"
        )

        self.logger.info(
            "Excel file exists."
        )

        # =================================================
        # Verify file size
        # =================================================

        file_size = os.path.getsize(
            excel_path
        )

        print(
            "Downloaded Excel file size:",
            file_size,
            "bytes"
        )

        assert file_size > 0, (
            "Downloaded Excel file is empty: "
            f"{excel_path}"
        )

        # =================================================
        # Verify extension
        # =================================================

        assert excel_file.lower().endswith(
            ".xlsx"
        ), (
            "Downloaded file is not an Excel .xlsx file: "
            f"{excel_file}"
        )

        # =================================================
        # Final success
        # =================================================

        self.logger.info(
            "******* Excel File Verification Successful *******"
        )

        print(
            "\n========================================"
        )

        print(
            "Excel export test completed successfully."
        )

        print(
            "Downloaded file:",
            excel_file
        )

        print(
            "File size:",
            file_size,
            "bytes"
        )

        print(
            "========================================"
        )