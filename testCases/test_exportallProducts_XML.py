import os
import time

import pytest

from pageObjects.AddProductPage import AddProduct
from pageObjects.LoginPage import LoginPage
from pageObjects.SearchProductPage import SearchProduct
from utilities.customLogger import LogGen
from utilities.download_utils import clear_downloads, wait_for_download
from utilities.readproperties import ReadConfig


class Test_ExportAllProducts_XML_046:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_export_all_products_xml(self, setup):

        self.logger.info(
            "******* Exporting All Products to XML *******"
        )

        self.driver = setup

        print("Application URL:", self.baseURL)

        self.driver.get(self.baseURL)

        print("Current URL:", self.driver.current_url)
        print("Page title:", self.driver.title)

        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        # -------------------------------------------------
        # Download directory
        # -------------------------------------------------

        download_dir = os.path.join(
            os.getcwd(),
            "downloads"
        )

        clear_downloads(download_dir)

        self.logger.info(
            f"******* Download directory: {download_dir} *******"
        )

        # -------------------------------------------------
        # Login
        # -------------------------------------------------

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "******* Login Successful *****"
        )

        # -------------------------------------------------
        # Navigate to Products
        # -------------------------------------------------

        self.logger.info(
            "****** Navigating to Products ******"
        )

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.logger.info(
            "****** Products page opened ******"
        )

        # -------------------------------------------------
        # Product page object
        # -------------------------------------------------

        searchproduct = SearchProduct(self.driver)

        time.sleep(2)

        # -------------------------------------------------
        # Export all products to XML
        # -------------------------------------------------

        searchproduct.clickExport()

        searchproduct.clickExportAllXML()

        # -------------------------------------------------
        # Wait for XML download
        # -------------------------------------------------

        downloaded_file = wait_for_download(
            download_dir,
            ".xml",
            timeout=60
        )

        downloaded_file_path = os.path.join(
            download_dir,
            downloaded_file
        )

        print(
            "Downloaded XML file:",
            downloaded_file_path
        )

        # -------------------------------------------------
        # Verify downloaded file
        # -------------------------------------------------

        assert os.path.exists(downloaded_file_path), (
            "XML file was not downloaded"
        )

        assert os.path.getsize(downloaded_file_path) > 0, (
            "Downloaded XML file is empty"
        )

        assert downloaded_file_path.lower().endswith(".xml"), (
            f"Unexpected downloaded file: "
            f"{downloaded_file_path}"
        )

        self.logger.info(
            "******* All Products XML Export Passed *******"
        )

        print(
            "\nAll products XML export PASSED"
        )