import os
import time
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddcustomerPage import AddCustomer
from pageObjects.SearchCustomerPage import SearchCustomer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen
from utilities.download_utils import clear_downloads, wait_for_download


class Test_ExportSelectedCustomers_XML_007:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_export_selected_customers_xml(self, setup):

        self.logger.info(
            "******* Exporting Selected Customers to XML *******"
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

        # Click Export Selected XML
        searchcust.clickExportSelected_XML()

        self.logger.info(
            "******* Export Selected XML button clicked *******"
        )

        # Wait for XML download to complete
        xml_file = wait_for_download(
            download_dir,
            ".xml",
            timeout=30
        )

        self.logger.info(
            f"******* XML Downloaded Successfully: {xml_file} *******"
        )

        # Verify XML file
        xml_path = os.path.join(download_dir, xml_file)

        assert os.path.exists(xml_path), (
            "XML file was not found in downloads folder"
        )

        assert os.path.getsize(xml_path) > 0, (
            "Downloaded XML file is empty"
        )

        self.logger.info(
            "******* XML File Verification Successful *******"
        )