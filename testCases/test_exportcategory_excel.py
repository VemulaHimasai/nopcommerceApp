
import os

import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.AddCategoryPage import AddCategory
from pageObjects.ExportCategoryPage import ExportCategory

from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen
from utilities.download_utils import (
    clear_downloads,
    wait_for_download
)


class Test_ExportCategory_Excel_056:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_exportcategory_excel(self, setup):

        self.logger.info(
            "***** Test_ExportCategory_Excel_056 Started *****"
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
        # CATALOG -> CATEGORIES
        # =====================================================

        self.logger.info(
            "***** Navigating to Categories *****"
        )

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addcategory = AddCategory(self.driver)
        self.addcategory.clickonCategoriesmenuItem()

        self.logger.info(
            "***** Categories Page Opened *****"
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
        # EXPORT CATEGORY TO EXCEL
        # =====================================================

        self.exportcategory = ExportCategory(
            self.driver
        )

        self.logger.info(
            "***** Starting Category Excel Export *****"
        )

        self.exportcategory.exportCategoryToExcel()

        self.logger.info(
            "***** Export Category to Excel clicked *****"
        )

        # =====================================================
        # WAIT FOR DOWNLOAD
        # =====================================================

        downloaded_file = wait_for_download(
            self.download_dir,
            extension=".xlsx",
            timeout=30
        )

        assert downloaded_file is not None, (
            "Category Excel file was not downloaded"
        )

        downloaded_file_path = os.path.join(
            self.download_dir,
            downloaded_file
        )

        # =====================================================
        # VERIFY DOWNLOAD
        # =====================================================

        assert os.path.exists(downloaded_file_path), (
            f"Downloaded Excel file does not exist: "
            f"{downloaded_file_path}"
        )

        assert downloaded_file.lower().endswith(
            ".xlsx"
        ), (
            f"Downloaded file is not an Excel file: "
            f"{downloaded_file}"
        )

        assert os.path.getsize(
            downloaded_file_path
        ) > 0, (
            f"Downloaded Excel file is empty: "
            f"{downloaded_file_path}"
        )

        self.logger.info(
            f"***** Category Excel file downloaded "
            f"successfully: {downloaded_file_path} *****"
        )

        self.logger.info(
            "***** Test_ExportCategory_Excel_056 Passed *****"
        )

