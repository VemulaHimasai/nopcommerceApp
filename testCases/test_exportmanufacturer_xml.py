import os

import pytest

from pageObjects.AddManufacturerPage import AddManufacturer
from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.ExportManufacturerPage import ExportManufacturer
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen
from utilities.download_utils import (
    clear_downloads,
    wait_for_download
)

class Test_ExportManufacturer_XML_063:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_exportmanufacturer_xml(self,setup):
        self.logger.info(
            "***** Test_ExportManufacturer_XML_063 Started *****"
        )
        self.driver = setup

        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # =====================================================
        # LOGIN
        # =====================================================

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "***** Login Successful *****"
        )

        # =====================================================
        # CATALOG -> MANUFACTURERS
        # =====================================================

        self.logger.info(
            "***** Navigating to Manufacturers *****"
        )

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addmanufacturer = AddManufacturer(self.driver)
        self.addmanufacturer.clickonManufacturersmenuItem()

        self.logger.info(
            "***** Manufacturers Page Opened *****"
        )

        # =====================================================
        # CLEAR DOWNLOADS
        # =====================================================

        self.logger.info(
            "***** Clearing previous downloaded files *****"
        )

        self.download_dir = os.path.join(
            os.getcwd(),
            "downloads"
        )

        clear_downloads(
            self.download_dir
        )
        self.logger.info(
            f"***** Download directory cleared: "
            f"{self.download_dir} *****"
        )

        # =====================================================
        # EXPORT MANUFACTURER TO XML
        # =====================================================
        self.exportmanufacturer = ExportManufacturer(self.driver)
        self.logger.info(
            "***** Starting Manufacturer XML Export *****"
        )
        self.exportmanufacturer.exportManufacturerToXML()
        self.logger.info(
            "***** Export Manufacturer to XML clicked *****"
        )

        # =====================================================
        # WAIT FOR DOWNLOAD
        # =====================================================

        downloaded_file = wait_for_download(
            self.download_dir,
            extension=".xml",
            timeout=60
        )

        assert downloaded_file is not None, (
            "Manufacturer XML file was not downloaded"
        )

        downloaded_file_path = os.path.join(
            self.download_dir,
            downloaded_file
        )

        # =====================================================
        # VERIFY DOWNLOAD
        # =====================================================

        assert os.path.exists(downloaded_file_path), (
            f"Downloaded XML file does not exist: "
            f"{downloaded_file_path}"
        )

        assert downloaded_file.lower().endswith(
            ".xml"
        ), (
            f"Downloaded file is not an XML file: "
            f"{downloaded_file}"
        )

        assert os.path.getsize(
            downloaded_file_path
        ) > 0, (
            f"Downloaded XML file is empty: "
            f"{downloaded_file_path}"
        )

        self.logger.info(
            f"***** Manufacturer XML file downloaded "
            f"successfully: {downloaded_file_path} *****"
        )

        self.logger.info(
            "***** Test_ExportManufacturer_XML_063 Passed *****"
        )
