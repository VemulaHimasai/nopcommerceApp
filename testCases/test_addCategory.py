import pytest
from selenium.webdriver.support.ui import WebDriverWait


from pageObjects.LoginPage import LoginPage
from pageObjects.AddProductPage import AddProduct
from pageObjects.AddCategoryPage import AddCategory
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen

class Test_AddCategory_050:
    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.regression
    def test_addcategory(self,setup):
        self.logger.info("*****Test_AddCategory_050*****")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        wait = WebDriverWait(self.driver, 15)

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.logger.info("*****Login Successful******")

        self.logger.info("*****Staring Add Category test*****")

        self.addproduct = AddProduct(self.driver)
        self.addproduct.clickonCatalogMenu()

        self.addctgory = AddCategory(self.driver)
        self.addctgory.clickonCategoriesmenuItem()

        #click add new
        self.addctgory.clickAddNew()

        self.logger.info("*****Providing category details*******")

        category_name = self.addctgory.generateCategoryName()

        self.addctgory.setCategoryName(category_name)

        self.addctgory.setCategoryDescription(
            "This is a test category created using Selenium automation."
        )

        self.addctgory.clickSave()

        assert self.addctgory.isCategoryCreatedSuccessfully(), \
            "Category was not created successfully"

