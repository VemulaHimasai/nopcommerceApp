
import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.AddCategoryPage import AddCategory
from pageObjects.SearchCategoryPage import SearchCategory
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_SearchCategoryPublish_Unpublished_054:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_searchcategorypyblish_unpublished(self, setup):

        self.logger.info(
            "***** Test_SearchCategoryPublish_Unpublished_054 *****"
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
            "***** Starting Search Category "
            "Publish = Unpublished Only Test *****"
        )

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addcategory = AddCategory(self.driver)
        self.addcategory.clickonCategoriesmenuItem()

        # =====================================================
        # SEARCH CATEGORY
        # =====================================================

        self.searchcategory = SearchCategory(self.driver)

        self.searchcategory.selectPublishedItem(
            "Unpublished only"
        )

        self.searchcategory.clickSearch()

        # =====================================================
        # VERIFY RESULTS
        # =====================================================

        if self.searchcategory.isNoDataAvailable():

            self.logger.info(
                "***** No unpublished categories exist. "
                "No data available in table displayed. *****"
            )

        else:

            row_count = (
                self.searchcategory.getCategoryRowCount()
            )

            assert row_count > 0, (
                "Search returned neither unpublished "
                "categories nor the expected "
                "'No data available in table' message"
            )

            self.logger.info(
                f"***** Published = Unpublished Only "
                f"returned {row_count} category rows *****"
            )

