import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
#Add Product Page
class AddProduct:
    #Catalog Menu
    lnkCatalog_menu_xpath = "//a[@href='#']//p[contains(text(),'Catalog')]"
    lnkProducts_menuitem_xpath = "//a[@href='/Admin/Product/List']"

    #Add New Button
    btnAddnew_xpath = "//a[normalize-space()='Add new']"

    #Product fields
    txtProductName_xpath = "//input[@id='Name']"
    txtshortdesc_xpath = "//textarea[@id='ShortDescription']"
    txtfulldesc_xpath = "//div[@role='textbox']"
    txtsku_xpath = "//input[@id='Sku']"

    #prices section
    prices_section = "//div[@id='product-price']"

    #prices fields
    numprice_xpath = "//input[@id='Price']"
    chktax_attempt = "//input[@id='IsTaxExempt']"

    #tax-category
    drptax_category = "//span[@id='select2-TaxCategoryId-container']"
    lstBooks_element = "//li[contains(text(),'Books')]"
    lstelecsoftware_xpath = "//li[contains(text(),'Electronics & Software')]"
    lstdownloadproducts_xpath = "//li[contains(text(),'Downloadable Products')]"
    lstjewelry_xpath = "//li[contains(text(),'Jewelry')]"
    lstapparel_xpath = "//li[contains(text(),'Apparel')]"

    #shipping section
    shipping_section = "//div[@id='product-shipping']"

    #shipping-fields
    weight_xpath = "//input[@id='Weight']"
    length_xpath = "//input[@id='Length']"
    width_xpath = "//input[@id='Width']"
    height_xpath = "//input[@id='Height']"

    #inventory-section
    inventory_section = "//div[@id='product-inventory']"


    #inventory
    drpinventory = "//span[@id='select2-ManageInventoryMethodId-container']"
    lst_donttrack = """//li[contains(., "Don't track inventory")]"""
    lst_track = "//li[normalize-space(.)='Track inventory']"
    lst_track_product = "//li[normalize-space(.)='Track inventory by product attributes']"

    #save button
    btnSave_xpath = "//button[@name='save']"

    success_message_xpath = "//div[contains(@class,'alert-success')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def clickonCatalogMenu(self):
        for attempt in range(3):
            try:
                catalog_menu = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, self.lnkCatalog_menu_xpath)
                ))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", catalog_menu)
                self.driver.execute_script("arguments[0].click();", catalog_menu)
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,"//a[contains(@href,'/Admin/Product/List')]")
                ))
                print("Catalog menu opened")
                return
            except (StaleElementReferenceException, TimeoutException):
                print(f"Catalog menu not ready."
                      f"Retrying ({attempt+1}/3)...")
                if attempt == 2:
                    raise

    def clickonProductMenuItem(self):
        for attempt in range(3):
            try:
                product_menu_item = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, self.lnkProducts_menuitem_xpath)
                ))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", product_menu_item)
                self.driver.execute_script("arguments[0].click();", product_menu_item)
                self.wait.until(EC.url_contains("/Admin/Product/List"))
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,self.btnAddnew_xpath)
                ))
                print("Product menu opened")
                print("Current url: ",self.driver.current_url)
                return
            except (StaleElementReferenceException, TimeoutException):
                print(f"Catalog menu not ready."
                      f"Retrying ({attempt + 1}/3)...")
                if attempt < 2:
                    try:
                        catalog_menu = self.wait.until(EC.element_to_be_clickable(
                            (By.XPATH,self.lnkCatalog_menu_xpath)
                        ))
                        self.driver.execute_script("arguments[0].click();", catalog_menu)
                    except (StaleElementReferenceException, TimeoutException):
                        pass
                else:
                    raise

    # add new product

    def clickonAddNew(self):
        add_new_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnAddnew_xpath)
        ))
        print("Button found:", add_new_button.text)
        print("Button href:", add_new_button.get_attribute("href"))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_new_button
        )
        # Firefox workaround: navigate using the actual href
        self.driver.get(
            add_new_button.get_attribute("href")
        )

        print("After Add New navigation")
        print("Current URL:", self.driver.current_url)
        print("Current Title:", self.driver.title)

        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.txtProductName_xpath)
        ))

    # Product details
    def setProduct(self,product_name=None,short_description="Test product short description",
                   full_description="Test product full description",sku=None,price="1000",
                   tax_category="Books",weight="1",length="10",width="10",
                   height="10",inventory_method="Don't track inventory"):

        if product_name is None:
            product_name = "Test Product " + str(random.randint(1000, 9999))

        if sku is None:
            sku = "SKU" + str(random.randint(10000, 99999))

        product_name_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.txtProductName_xpath)
        ))
        product_name_field.clear()
        product_name_field.send_keys(product_name)

        short_desc_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.txtshortdesc_xpath)
        ))
        short_desc_field.clear()
        short_desc_field.send_keys(short_description)
        full_desc_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.txtfulldesc_xpath)
        ))
        full_desc_field.clear()
        full_desc_field.send_keys(full_description)

        sku_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.txtsku_xpath)
        ))
        sku_field.clear()
        sku_field.send_keys(sku)

        #prices section
        self.scrollToSection(self.prices_section)

        price_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.numprice_xpath)
        ))
        price_field.clear()
        price_field.send_keys(str(price))

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.drptax_category)
        )).click()

        tax_options = {
            "Books": self.lstBooks_element,
            "Electronics & Software": self.lstelecsoftware_xpath,
            "Downloadable Products" : self.lstdownloadproducts_xpath,
            "Jewelry": self.lstjewelry_xpath,
            "Apparel":self.lstapparel_xpath
        }

        if tax_category in tax_options:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH,tax_options[tax_category])
            )).click()
        else:
            raise ValueError(f"Invalid tax category: {tax_category}")

        #shipping

        self.scrollToSection(self.shipping_section)

        weight_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.weight_xpath)
        ))
        weight_field.clear()
        weight_field.send_keys(str(weight))

        length_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.length_xpath)
        ))
        length_field.clear()
        length_field.send_keys(str(length))

        width_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.width_xpath)
        ))

        width_field.clear()
        width_field.send_keys(str(width))

        height_field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,self.height_xpath)
        ))
        height_field.clear()
        height_field.send_keys(str(height))

        #inventory

        self.scrollToSection(self.inventory_section)

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.drpinventory)
        )).click()

        inventory_options = {
            "Don't track inventory": self.lst_donttrack,
            "Track inventory": self.lst_track,
            "Track inventory by product attributes": self.lst_track_product

        }

        if inventory_method in inventory_options:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH,inventory_options[inventory_method])
            )).click()
        else:
            raise ValueError(f"Invalid inventory method: {inventory_method}")

        print("Product details entered successfully")

    def clickSave(self):
        save_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnSave_xpath)
        ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button)
        save_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,self.btnSave_xpath)
        ))
        self.driver.execute_script("arguments[0].click();", save_button)

        print("Save Button clicked")

    def scrollToSection(self,section_xpath):
        section = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,section_xpath)
        ))
        self.driver.execute_script( "arguments[0].scrollIntoView({block:'center'});",section)

    def isProductCreatedSuccessfully(self):

        try:

            self.wait.until(
                EC.url_contains("/Admin/Product/List")
            )

            print("Product List page loaded after saving")

            message = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.success_message_xpath)
                )
            )

            print("Success message:", message.text)

            if message.is_displayed():
                print("Product created successfully")
                return True

            return False

        except (StaleElementReferenceException, TimeoutException):

            print("Product creation success message not found")
            print("Current URL:", self.driver.current_url)

            return False











