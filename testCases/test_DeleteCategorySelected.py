import pytest

from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.AddCategoryPage import AddCategory
from pageObjects.DeleteCategoryPage import DeleteCategory
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_DeleteCategorySelected_057:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()
    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_deletecategoryselect(self, setup):

        self.logger.info(
            "*****Test_DeleteCategory_Selected_057*****"
        )

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

        self.logger.info(
            "*****Login Successful******"
        )

        self.logger.info(
            "*****Starting Delete Selected Category test*****"
        )

        # -------------------------------------------------
        # Open Catalog
        # -------------------------------------------------

        self.addproduct = AddProduct(self.driver)

        self.addproduct.clickonCatalogMenu()

        # -------------------------------------------------
        # Open Categories
        # -------------------------------------------------

        self.addcategory = AddCategory(self.driver)

        self.addcategory.clickonCategoriesmenuItem()

        self.logger.info(
            "*****Categories page opened*****"
        )

        # -------------------------------------------------
        # Create category to delete
        # -------------------------------------------------

        category_name = "Test Category 057"

        self.addcategory.clickAddNew()

        self.addcategory.setCategoryName(
            category_name
        )

        self.addcategory.setCategoryDescription(
            "This category is created for delete testing."
        )

        self.addcategory.clickSave()

        self.logger.info(
            f"*****Category created: "
            f"{category_name}*****"
        )

        # -------------------------------------------------
        # Open Categories list
        # -------------------------------------------------

        self.addcategory.clickonCategoriesmenuItem()

        # -------------------------------------------------
        # Select category
        # -------------------------------------------------

        self.deletecategory = DeleteCategory(
            self.driver
        )

        self.deletecategory.selectCategory(
            category_name
        )

        self.logger.info(
            f"*****Category selected: "
            f"{category_name}*****"
        )

        # -------------------------------------------------
        # Delete selected category
        # -------------------------------------------------

        self.deletecategory.clickDeleteSelected()

        self.logger.info(
            "*****Delete Selected clicked*****"
        )

        # -------------------------------------------------
        # Confirm deletion
        # -------------------------------------------------

        self.deletecategory.confirmDelete()

        self.logger.info(
            "*****Category deletion confirmed*****"
        )

        # -------------------------------------------------
        # Verify category deleted
        # -------------------------------------------------

        assert not self.deletecategory.isCategoryPresent(
            category_name
        ), (
            f"Category was not deleted: "
            f"{category_name}"
        )

        self.logger.info(
            f"*****Category deleted successfully: "
            f"{category_name}*****"
        )