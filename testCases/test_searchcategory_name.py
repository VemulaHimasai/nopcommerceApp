import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.AddCategoryPage import AddCategory
from pageObjects.SearchCategoryPage import SearchCategory
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchCategoryByName_051:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchcategorybyname(self, setup):

        self.logger.info(
            "***** Test_SearchCategoryByName_051 *****"
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
            "***** Starting Search Category By Name Test *****"
        )

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addcategory = AddCategory(self.driver)
        self.addcategory.clickonCategoriesmenuItem()

        # =====================================================
        # SEARCH CATEGORY
        # =====================================================

        self.searchcategory = SearchCategory(self.driver)

        category_name = (
            self.searchcategory.getFirstCategoryName()
        )

        assert category_name, (
            "No existing category was found in the table"
        )

        self.logger.info(
            f"***** Category selected for search: "
            f"{category_name} *****"
        )

        # -----------------------------------------------------
        # Enter category name
        # -----------------------------------------------------

        self.searchcategory.enterCategoryName(
            category_name
        )

        # -----------------------------------------------------
        # Click Search
        # -----------------------------------------------------

        self.searchcategory.clickSearch()

        # -----------------------------------------------------
        # Verify category exists
        # -----------------------------------------------------

        category_present = (
            self.searchcategory.isCategoryPresent(
                category_name
            )
        )

        assert category_present, (
            f"Category '{category_name}' "
            f"was not found after searching by name"
        )

        self.logger.info(
            f"***** Category '{category_name}' "
            f"found successfully *****"
        )