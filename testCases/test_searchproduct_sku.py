import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchProductPage import SearchProduct
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchProductBySKU_030:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchproductbysku(self, setup):

        self.logger.info(
            "*****Test_SearchProductBySKU_030*****"
        )

        self.driver = setup

        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # -------------------------------------------------
        # LOGIN
        # -------------------------------------------------

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info(
            "*****Login Successful******"
        )

        # -------------------------------------------------
        # OPEN PRODUCTS
        # -------------------------------------------------

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        self.searchproduct = SearchProduct(
            self.driver
        )

        # -------------------------------------------------
        # GET PRODUCT + SKU DYNAMICALLY
        # -------------------------------------------------

        product_name, sku = (
            self.searchproduct.getFirstProductAndSKU()
        )

        assert product_name, (
            "No product was found in the Products table"
        )

        assert sku, (
            f"No SKU was found for product "
            f"'{product_name}'"
        )

        print(
            "========================================"
        )

        print(
            "Dynamic Product Name:",
            product_name
        )

        print(
            "Dynamic SKU:",
            sku
        )

        print(
            "========================================"
        )

        # -------------------------------------------------
        # SEARCH PRODUCT BY DYNAMIC SKU
        # -------------------------------------------------

        self.searchproduct.setSKU(sku)

        self.searchproduct.clickGo()

        print(
            "URL after Go:",
            self.driver.current_url
        )

        print(
            "Title after Go:",
            self.driver.title
        )

        # -------------------------------------------------
        # VERIFY SKU ON EDIT PRODUCT PAGE
        # -------------------------------------------------

        assert self.searchproduct.verifySKU(sku), (
            f"Expected SKU '{sku}' "
            f"was not found on the product page"
        )