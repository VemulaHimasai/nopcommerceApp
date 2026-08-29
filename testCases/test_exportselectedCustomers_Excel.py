import os
import time
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen
from utilities.download_utils import clear_downloads, wait_for_download


class Test_ExportSelectedCustomers_XML_009:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_export_selected_customers_excel(self, setup):

        self.logger.info(
            "******* Exporting Selected Customers to Excel *******"
        )

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        # Download directory
        download_dir = os.path.join(os.getcwd(), "downloads")

        # Remove old downloaded files
        clear_downloads(download_dir)

        self.logger.info(
            f"******* Download directory: {download_dir} *******"
        )

        # Login
        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("******* Login Successful *****")

        # Navigate to Customers
        self.logger.info("****** Navigating to Customers ******")

        self.addcust = AddCustomer(self.driver)
        self.addcust.clickOnCustomersMenu()
        self.addcust.clickonCustomersMenuItem()

        self.logger.info("****** Customers page opened ******")

        # Search Customer page
        searchcust = SearchCustomer(self.driver)

        time.sleep(2)

        # Select customers
        searchcust.selectCustomerCheckBox(1)
        searchcust.selectCustomerCheckBox(2)

        self.logger.info(
            "******* Customers Selected Successfully *******"
        )

        # Click Export dropdown
        searchcust.clickExport()

        time.sleep(1)

        # Click Export Selected Excel
        searchcust.clickExportSelected_Excel()

        self.logger.info(
            "******* Export Selected Excel button clicked *******"
        )

        # Wait for XML download to complete
        excel_file = wait_for_download(
            download_dir,
            ".xlsx",
            timeout=30
        )

        self.logger.info(
            f"******* Excel Downloaded Successfully: {excel_file} *******"
        )

        # Verify XML file
        excel_path = os.path.join(download_dir, excel_file)

        assert os.path.exists(excel_path), (
            "Excel file was not found in downloads folder"
        )

        assert os.path.getsize(excel_path) > 0, (
            "Downloaded Excel file is empty"
        )

        self.logger.info(
            "******* Excel File Verification Successful *******"
        )