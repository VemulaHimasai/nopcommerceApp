import os

import pytest
from selenium.webdriver.support.ui import WebDriverWait


from pageObjects.SearchProductPage import SearchProduct
from pageObjects.LoginPage import LoginPage
from utilities.customLogger import LogGen
from utilities.readproperties import ReadConfig
from pageObjects.AddProductPage import AddProduct



class Test_DownloadCatalogPDF_049:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_download_catalog_as_pdf(self, setup):
        self.logger.info("********Test_DownloadCatalog as PDF********")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # -------------------------------------------------
        # Login
        # -------------------------------------------------

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***** Login Successful *****")

        self.logger.info(
            "***** Starting Download Catalog as PDF Test *****"
        )

        # -------------------------------------------------
        # Navigate to Products
        # -------------------------------------------------

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        product_page = SearchProduct(self.driver)

        product_page.clickDownloadCatalogAsPDF()

        # Verify PDF download
        download_dir = os.path.abspath("downloads")

        WebDriverWait(self.driver, 30).until(
            lambda driver: any(
                file.lower().endswith(".pdf")
                for file in os.listdir(download_dir)
            )
        )

        pdf_files = [
            file
            for file in os.listdir(download_dir)
            if file.lower().endswith(".pdf")
        ]

        assert pdf_files, "Catalog PDF was not downloaded"

        print("Downloaded PDF:", pdf_files[-1])



