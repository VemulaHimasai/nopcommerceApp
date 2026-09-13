import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.SearchProductPage import SearchProduct
from pageObjects.EditProductPage import EditProductPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_EditProduct_032:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_editproduct(self, setup):

        self.logger.info("***** Test_EditProduct_032 *****")

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        # =========================================================
        # LOGIN
        # =========================================================

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("***** Login Successful *****")

        # =========================================================
        # OPEN CATALOG -> PRODUCTS
        # =========================================================

        self.logger.info(
            "***** Opening Catalog -> Products *****"
        )

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()
        self.addproduct.clickonProductMenuItem()

        # =========================================================
        # GET AN EXISTING PRODUCT DYNAMICALLY
        # =========================================================

        self.searchproduct = SearchProduct(self.driver)

        product_name = self.searchproduct.getFirstProductName()

        assert product_name is not None, \
            "No existing product was found in Products table"

        self.logger.info(
            f"***** Dynamic Product Selected: {product_name} *****"
        )

        print(
            "========================================"
        )
        print(
            "Dynamic Product Name:",
            product_name
        )
        print(
            "========================================"
        )

        # =========================================================
        # OPEN EDIT PAGE FOR THAT PRODUCT
        # =========================================================

        edit_clicked = self.searchproduct.clickEditByProductName(
            product_name
        )

        assert edit_clicked, \
            f"Could not open Edit page for product: {product_name}"

        self.logger.info(
            f"***** Edit page opened for: {product_name} *****"
        )

        # =========================================================
        # EDIT PRODUCT
        # =========================================================

        self.editproduct = EditProductPage(self.driver)

        # Generate a new SKU dynamically.
        # No hardcoded existing SKU is used.
        new_sku = f"SKU{__import__('random').randint(10000, 99999)}"

        new_price = "999"

        print(
            "New SKU:",
            new_sku
        )

        print(
            "New Price:",
            new_price
        )

        # =========================================================
        # UPDATE SKU
        # =========================================================

        self.editproduct.setSKU(new_sku)

        # =========================================================
        # UPDATE PRICE
        # =========================================================

        self.editproduct.setPrice(new_price)

        self.logger.info(
            f"***** Product details updated: "
            f"SKU={new_sku}, Price={new_price} *****"
        )

        # =========================================================
        # SAVE
        # =========================================================

        self.editproduct.clickSave()

        self.logger.info(
            "***** Save button clicked *****"
        )

        # =========================================================
        # VERIFY SUCCESS MESSAGE
        # =========================================================

        assert self.editproduct.isProductUpdatedSuccessfully(), \
            "Product update success message was not displayed"

        self.logger.info(
            "***** Product updated successfully *****"
        )