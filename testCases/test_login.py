import pytest
from selenium import webdriver
from pageObjects.LoginPage import LoginPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


#test case for login page
class Test_001_Login:
    baseURL = ReadConfig.getApplicationURL()
    username=ReadConfig.getUseremail()
    password=ReadConfig.getPassword()

    logger = LogGen.loggen()

    #test methods
    @pytest.mark.regression
    def test_homePageTitle(self, setup):
        self.logger.info("********Test_001_Login********")
        self.logger.info("********Verify Home Page Title********")
        self.driver = setup
        self.driver.get(self.baseURL)

        print("Current URL:", self.driver.current_url)
        print("Page Title:", self.driver.title)

        self.driver.save_screenshot(".\\Screenshots\\"+"test_homePageTitle.png")

        assert self.driver.title == "Your store. Login"
        self.logger.info("********Home Page Title test is passed********")

    @pytest.mark.sanity
    @pytest.mark.regression
    def test_login(self,setup):
        self.logger.info("********Verify Login Test********")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.lp = LoginPage(self.driver)
        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        act_title = self.driver.title

        #validation
        if act_title == "Dashboard / nopCommerce administration":
            assert True
            self.logger.info("********Login test Passed********")
            self.driver.close()

        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_login.png")
            self.driver.close()
            self.logger.error("********Login Test Failed********")
            assert False


