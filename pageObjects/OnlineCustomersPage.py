import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

class OnlineCustomersPage:

    lnkonlinecustomers_menuitem_xpath = "//a[@href='/Admin/OnlineCustomer/List']"


    txt_Customer_Roles_xpath = "//input[@role='searchbox']"
    lst_Administrators_xpath = "//li[contains(text(),'Administrators')]"
    lst_ForumModerators_xpath = "//li[contains(text(),'Forum Moderators')]"
    lst_Registered_xpath = "//li[contains(text(),'Registered')]"
    lst_Guests_xpath = "//li[contains(text(),'Guests')]"
    lst_Vendors_xpath = "//li[contains(text(),'Vendors')]"

    #search button
    btnSearchRoles_xpath = "//button[@id='search-customers']"

    #full table
    table_xpath = "//table[@id='onlinecustomers-grid']"
    table_rows_xpath = "//table[@id='onlinecustomers-grid']/tbody/tr"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def clickonOnlineCustomerMenuItem(self):
        online_customers_menu_item = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.lnkonlinecustomers_menuitem_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", online_customers_menu_item)
        self.driver.execute_script("arguments[0].click();", online_customers_menu_item)

    def getTableRows(self):
        rows = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH,self.table_rows_xpath)
        ))
        table_data = []
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            row_data =[column.text.strip() for column in columns]
            table_data.append(row_data)
        return table_data

    def getCustomerNames(self):

        rows = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, self.table_rows_xpath)
            )
        )

        customer_names = []

        for row in rows:

            cols = row.find_elements(By.TAG_NAME, 'td')

            if cols:

                customer_name = cols[0].text.strip()

                if customer_name != "No data available in table":
                    customer_names.append(customer_name)

        return customer_names

    def selectCustomerRole(self,role):
        role_xpaths = {
            "Administrators": self.lst_Administrators_xpath,
            "Forum Moderators": self.lst_ForumModerators_xpath,
            "Registered": self.lst_Registered_xpath,
            "Guests": self.lst_Guests_xpath,
            "Vendors": self.lst_Vendors_xpath
        }

        if role not in role_xpaths:
            raise ValueError("Invalid role selected")

        role_input = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.txt_Customer_Roles_xpath)
        ))
        role_input.click()
        role_input.send_keys(role)
        role_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,role_xpaths[role])
        ))
        role_option.click()
        print("Selected Customer Role:",role)

    def clickSearch(self):
        search_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.btnSearchRoles_xpath)
        ))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            search_button
        )

        search_button.click()

        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, self.table_xpath)
        ))

    def getSearchResults(self):

        for attempt in range(3):

            try:
                return self.getCustomerNames()

            except StaleElementReferenceException:

                print(
                    f"Search result table refreshed. "
                    f"Retrying... Attempt {attempt + 1}"
                )

                time.sleep(1)

        raise StaleElementReferenceException(
            "Search results table remained stale after 3 attempts."
        )



