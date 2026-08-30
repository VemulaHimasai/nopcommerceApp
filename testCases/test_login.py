import pytest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.LoginPage import LoginPage
from utilities.readproperties import ReadConfig
from utilities.customLogger import LogGen


class Test_001_Login:

    baseURL = ReadConfig.getApplicationURL()
    username = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    logger = LogGen.loggen()

    @pytest.mark.sanity
    @pytest.mark.regression
    def test_login(self, setup):

        self.logger.info("********Verify Login Test********")

        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.lp = LoginPage(self.driver)

        self.lp.setUserName(self.username)
        self.lp.setPassword(self.password)

        self.lp.clickLogin()

        # Wait until Dashboard page title appears
        WebDriverWait(self.driver, 20).until(
            EC.title_is("Dashboard / nopCommerce administration")
        )

        act_title = self.driver.title

        if act_title == "Dashboard / nopCommerce administration":

            self.logger.info("********Login test Passed********")
            assert True

        else:

            self.driver.save_screenshot(
                ".\\Screenshots\\test_login.png"
            )

            self.logger.error("********Login Test Failed********")
            assert False