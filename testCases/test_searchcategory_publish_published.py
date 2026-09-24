
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.AddCategoryPage import AddCategory
from pageObjects.SearchCategoryPage import SearchCategory
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchCategoryPublish_Published_053:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchcategorypyblish_published(self, setup):

        self.logger.info(
            "***** Test_SearchCategoryPublish_Published_053 *****"
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
            "***** Starting Search Category Publish = All Test *****"
        )

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addcategory = AddCategory(self.driver)
        self.addcategory.clickonCategoriesmenuItem()

        # =====================================================
        # SEARCH CATEGORY
        # =====================================================

        self.searchcategory = SearchCategory(self.driver)

        self.searchcategory.selectPublishedItem("Published only")

        self.searchcategory.clickSearch()

        # =====================================================
        # VERIFY RESULTS
        # =====================================================

        row_count = self.searchcategory.getCategoryRowCount()

        assert row_count > 0, (
            "No category rows were returned "
            "after selecting Published = Published only"
        )

        self.logger.info(
            f"***** Published = Published Only  returned "
            f"{row_count} category rows *****"
        )

