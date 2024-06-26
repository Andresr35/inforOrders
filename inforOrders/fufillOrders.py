'''
This file has all the functions for running through all the order steps in infor
most of the selenium work will be done here.

'''
import json
import math
import time
import traceback
from configparser import ConfigParser

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from inforOrders.Utils import jsonUtils
from inforOrders.WebDriver import EnviromentSetUp

# Getting up env variables
config = ConfigParser()
config.read("config.ini")


class fufillOrders(EnviromentSetUp):
    """Base class moves the web driver around. This class holds 
    all the functions that get around the infor website

    Args:
        EnviromentSetUp (Class): Base class for moving web driver around
    """

    def login(user: str, password: str) -> None:
        """starts the web selenium server and logs into infor on company 40. Ends up taking you to order entry page

        Args:
            user (str): username for infor
            password (str): password for infor
        """
        
        try:

            # Setting up web objects to be passed around and timeouts
            EnviromentSetUp.setUp()
            web = EnviromentSetUp.web
            wait = WebDriverWait(web, 30)#FIXME: make this a config.ini
            longerWait = WebDriverWait(web, 60)
            transition = float(config.get("time","transition"))

            # This is the link to the Order Entry page. First asks to login to infor account and then personal infor account.
            web.get("https://xisrv.stronghandtools.com/infor/d7de089b-7e09-4476-a5f5-80697edc7524?favoriteContext=oeet.initiate&LogicalId=lid://infor.sx.1")
            signInUser: WebElement = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="userNameInput"]')))
            signInUser.send_keys(config.get("infor", "inforAccountLogin"))
            signInPassword: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="passwordInput"]')))
            signInPassword.send_keys(config.get(
                "infor", "inforAccountPassword"))
            signInSubmit: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="submitButton"]')))
            signInSubmit.click()

            # Checking to see if the document management tab is open cause it needs to be closed
            documentMng: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="body"]/infor-mingle-shell/nav-menu/div/header/section[2]/drop-menu/div[1]/ul/li[5]')))
            if ("expanded" in documentMng.get_attribute("class")):
                close: WebElement = wait.until(EC.visibility_of_element_located((
                    By.XPATH, '/html/body/div[2]/infor-mingle-shell/nav-menu/div/header/section[2]/drop-menu/div[1]/ul/li[5]/button')))
                close.click()

            # Entering the frame inside the infor website which is where all the action is
            wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.NAME, "sxeweb_d7de089b-7e09-4476-a5f5-80697edc7524")))  # class =m-app-frame

            # Signing into personal infor account.
            time.sleep(transition)
            inforUser: WebElement = longerWait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="signin-userid"]')))

            inforPassword: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="signin-password"]')))
            inforCompany: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="signin-company"]')))
            inforUser.send_keys(str(user))
            inforPassword.send_keys(str(password))
            inforCompany.send_keys("40")

            inforSubmit: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="sign-in-view"]/section/form/button')))
            inforSubmit.click()

            try:
                # Trying to clear past operator session. Sometimes this doesn't pop up, if it
                # doesn't check to see if we made it to the customer setup page and continue
                time.sleep(transition)
                inforOp: WebElement = wait.until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'btn-modal-primary')))
                inforOp.click()
            except:
                try:
                    customerField = wait.until(EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[1]/span/input')))
                except:
                    raise

            print("Logged in!")

        except Exception:
            print("Could not login!")
            raise

    def closeWeb() -> None:
        """uses web.close() should work if there is still a web that is open
        """
        web = EnviromentSetUp.web
        web.close()

    def setUpOrder(po: str,  state: str,  country: str, method: str) -> None:
        '''
        :Args:
            - po - PO number from shopify of the customer
            - state - shipping state
            - country - shipping country
            - method - payment method used in shopify        
        '''
        try:

            # Setting up web objects to be passed around
            web = EnviromentSetUp.web
            wait = WebDriverWait(web, float(config.get("time", "wait")))
            longerWait = WebDriverWait(web, 30)
            transition = float(config.get("time", "transition"))
            inputTrans = float(config.get("time", "inputTransition"))

            # Defining the customer number, which is dependent on the country
            # state, and method of payment
            if(method == "Shopify Payments"):
                if(country == "United States" or country == "US"):
                    if(state == "CA"):
                        customer = "40010"
                    else:
                        customer = "40011"
                else:
                    customer = "40012"
            elif(method == "PayPal Express Checkout"):
                print(country)
                if(country == "United States" or country == "US"):
                    if(state == "CA"):
                        customer = "40003"
                    else:
                        customer = "40004"
                else:
                    customer = "40005"

            # Starting to fill out all fields of this page.
            time.sleep(transition)
            customerField: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[1]/span/input')))
            # Try block in case customer was not defined. This happens when the method is different.
            try:
                customerField.send_keys(str(customer))
                time.sleep(inputTrans)
            except:
                print("Only 'Paypal Express Checkout' and 'Shopify Payments' is accepted as a payment method. '",
                      method, "' was entered.")
                raise Exception("Invalid Payment Method entered. Manual Order Entry required")
            warehouse: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[2]/span/input')))
            warehouse.send_keys('V01')#NOTE: This is the warehouse Valtra. Can change if company scales up
            time.sleep(inputTrans)
            shipvia: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[2]/div[2]/span/input')))
            time.sleep(inputTrans)
            shipvia.clear()
            shipvia.send_keys('UG')
            time.sleep(inputTrans)
            orderID: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[5]/input')))
            orderID.send_keys(str(po))
            initNext: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[1]')))
            initNext.click()

        except Exception:
            print("Could not setup order")
            traceback.print_exc()
            raise

    def editShipping(name: str, address: str, city: str, state: str, zip, countryCode: str) -> None:
        """edits the shipping address in infor and gets ready to start adding line items.

        Args:
            name (str): shipping name
            address (str): shipping address
            city (str): shipping city
            state (str): state abbreviation
            zip (int): shipping zip
            country (str): shipping country
        """

        # Setting up web objects to be passed around
        web = EnviromentSetUp.web
        wait = WebDriverWait(web, float(config.get("time", "wait")))
        longerWait = WebDriverWait(web, 30)
        transition = float(config.get("time", "transition"))
        inputTrans = float(config.get("time", "inputTransition"))

        try:
            # Start inputting address of the customer
            time.sleep(transition)
            print("Starting to input shipping details.")
            editShip: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[1]/div[1]/div/div[2]/div[2]/div/div/div/div/button')))
            editShip.click()
            time.sleep(transition)
            nameField: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/div/input')))
            nameField.clear()
            nameField.send_keys(str(name))
            addressField: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[1]/input')))
            addressField.clear()
            addressField.send_keys(str(address))
            cityField: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[5]/input')))
            cityField.clear()
            cityField.send_keys(str(city))
            stateField: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[6]/div[1]/input')))
            stateField.clear()
            stateField.send_keys(str(state))
            zipField: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[6]/div[2]/input')))
            zipField.clear()
            zipField.send_keys(str(zip))

            # Comes from countries.json. Converts shopify country code to full name to use to find inner html
            countryDict = jsonUtils.readJSON()
            country = countryDict[countryCode]
            countryDrop: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[7]/div/div')))
            countryDrop.click()
            countryList: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@id="dropdown-list"]/ul')))
            countryClicked = False
            # Goes through each item in the country list to click the right shipping country.
            for child in countryList.find_elements(By.XPATH, './/*'):
                for otherChild in child.find_elements(By.XPATH, './/*'):
                    if(otherChild.get_attribute("innerHTML") == country):
                        otherChild.click()
                        countryClicked = True
                        break
                else:
                    continue
                break

            # In Case none of the countries were clicked.
            if (countryClicked == False):
                raise Exception(
                    "Country was not clicked. Wrong Country Code or Infor Country Spelling")

            # Moving on and getting ready to start adding products.
            enterAddress: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[3]/button[2]')))
            enterAddress.click()
            print("Finished editing shipping!")
            time.sleep(transition)
            lineEntry: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[5]')))
            lineEntry.click()
            quickLine: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/div/ul/li[2]/a')))
            quickLine.click()

        except Exception:
            print("Could not edit shipping")
            traceback.print_exc()
            raise

    def addLineItem(sku: str, quantity, price: float) -> None:
        """adds in products to the product

        Args:
            sku (str): sku of product you are referring to
            quantity (int): quantity they are trying to buy
            price (float): price the product was sold for
        """
        try:
            # Setting up web objects to be passed around
            web = EnviromentSetUp.web
            wait = WebDriverWait(web, float(config.get("time", "wait")))
            longerWait = WebDriverWait(web, 30)
            transition = float(config.get("time", "transition"))
            inputTrans = float(config.get("time", "inputTransition"))

            # Starting to input products to line item section.
            time.sleep(transition)
            product: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/span/input')))
            product.send_keys(str(sku))
            time.sleep(inputTrans)
            quantityField: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[1]/input')))
            quantityField.click()
            quantityField.clear()
            quantityField.send_keys(quantity)
            time.sleep(inputTrans)
            priceField: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[3]/input')))
            priceField.clear()
            time.sleep(inputTrans)
            priceField.click()
            priceField.send_keys(price)
            time.sleep(inputTrans)
            add: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/button')))
            add.click()
            print("Added in:\t", sku)

        except Exception:
            print("Wasn't able to add a line item")
            traceback.print_exc()
            raise

    def finishOrder(shipping: float, discount, zip: int, shopTotalQuantity: int) -> None:
        """does taxes and shipping, then gets ready to do next order entry

        Args:
            shipping (float): shipping amount
            discount (float): discount amount
            zip (int): zip code
        """
        try:
            # Setting up web objects to be passed around
            web = EnviromentSetUp.web
            wait = WebDriverWait(web, float(config.get("time", "wait")))
            longerWait = WebDriverWait(web, 30)
            transition = float(config.get("time", "transition"))
            inputTrans = float(config.get("time", "inputTransition"))

            # Getting the County from Zip code,and other address values.
            data = json.loads(open("./inforOrders/assets/cities.json").read())
            state = ''
            for i in data:
                if str(i['zip_code']) == str(zip):
                    county = (i['county'])
                    state = (i['state'])
                    city = (i['city'])
                    break

            # Checking to see if all products were added before continuing
            totalQuantityElement: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/span[2]')))
            inforTotalQuanity = ((totalQuantityElement.get_attribute(
                "innerHTML")).replace("(", "")).replace(")", "")
            print("Infor total:\t", inforTotalQuanity)
            print("Shop quant: \t", shopTotalQuantity)
            if(shopTotalQuantity == int(inforTotalQuanity)):
                print("good!")
            else:
                print("bad")
                raise Exception("Total quantiy does not match")
            addLines: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/button[1]')))
            addLines.click()

            # Getting ready to input tax information
            time.sleep(transition)
            taxButton: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[1]/div/div/div/a[3]')))
            try:
                taxButton.click()
            except:
                try:
                    # INFOR randomly gives an error. This dismisses it.
                    # if the warning pops up, prob handle it here. /html/body/div[30]/div/div/div/div[2]/div/p x path for message..."Units Not Set Up in Unit Table - ICSEU or SASTT (4026)"
                    unitError: WebElement = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div/div/div[3]/button')))
                    unitError.click()
                    time.sleep(3)
                    taxButton.click()
                except:
                    traceback.print_exc()
                    print(
                        "Tried to go to taxes tab, but was not able to click... wait more on timeout\n")
                    raise

            # CA requires more work on taxes
            time.sleep(inputTrans)
            print("Working on Taxes")
            try:
                if (state == "CA"):
                    stateDrop: WebElement = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/div')))
                    stateDrop.click()
                    time.sleep(inputTrans)
                    stateDrop: WebElement = wait.until(EC.element_to_be_clickable((
                        By.XPATH, '/html/body/div[@id="dropdown-list"]/span')))
                    stateDrop.click()
                    countyField: WebElement = wait.until(EC.element_to_be_clickable((
                        By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[2]/div/div')))
                    countyField.click()
                    time.sleep(inputTrans)
                    county = str(county).upper()
                    if(len(county) > 12):
                        shortCounty = county[0:12]
                    else:
                        shortCounty = county
                    countyList: WebElement = wait.until(EC.visibility_of_element_located((
                        By.XPATH, '/html/body/div[@id="dropdown-list"]/ul')))
                    cityState = False
                    # Looping through list of county to click
                    for child in countyList.find_elements(By.XPATH, './/*'):
                        for otherChild in child.find_elements(By.XPATH, './/*'):
                            if(otherChild.get_attribute("innerHTML") == shortCounty.replace(" ", "")):
                                otherChild.click()
                                cityState = True
                                break
                            elif(otherChild.get_attribute("innerHTML") == shortCounty):
                                otherChild.click()
                                cityState = True
                                break
                        else:
                            continue
                        break
                    # Making sure a city was clicked
                    if (cityState == False):
                        print("County was not clicked in Taxes section")
                        raise Exception("County Not Found")

                    # Loop through all the cities and clicking it
                    cityField: WebElement = wait.until(EC.element_to_be_clickable((
                        By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div')))
                    cityField.click()
                    time.sleep(inputTrans)
                    city = str(city).upper()
                    county = county.replace(" ", "")
                    betterCounty = county[0:4]
                    # This is for infor spelling syntax
                    if(len(city) > 12):
                        betterCity = city[0:12]+"-"+betterCounty
                    else:
                        betterCity = city+"-"+betterCounty
                    cityList: WebElement = wait.until(EC.visibility_of_element_located((
                        By.XPATH, '/html/body/div[@id="dropdown-list"]/ul')))
                    countyState = False
                    for child in cityList.find_elements(By.XPATH, './/*'):
                        for otherChild in child.find_elements(By.XPATH, './/*'):
                            if(otherChild.get_attribute("innerHTML") == betterCity.replace(" ", "")):
                                otherChild.click()
                                countyState = True
                                break
                            elif(otherChild.get_attribute("innerHTML") == betterCity):
                                otherChild.click()
                                countyState = True
                                break
                        else:
                            continue
                        break
                    if (countyState == False):
                        print("City was not clicked in Taxes section")
                        raise Exception("City Not Found")

            except UnboundLocalError:
                print("Not defined")
                raise

            # Adding in freight
            time.sleep(inputTrans)
            recalculate = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[3]')))
            recalculate.click()
            time.sleep(transition)
            addons: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[2]')))
            addons.click()
            print("Working on freight cost")
            time.sleep(transition)
            addShipping: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[1]/div/button')))
            addShipping.click()
            time.sleep(inputTrans)
            freightDropdown: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[1]/div/div/div[1]/div/div')))
            freightDropdown.click()
            freight: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@id="dropdown-list"]/ul/li[3]/a')))
            freight.click()
            freightAmount: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[1]/div/div/div[2]/input')))
            freightAmount.clear()
            time.sleep(inputTrans)
            freightAmount.send_keys(shipping)
            finishFreight: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[2]/div[2]/button[1]')))
            finishFreight.click()
            print("Finished Freight")
            goBack: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[1]/div/button')))
            time.sleep(transition)
            goBack.click()
            time.sleep(transition)

            # Working on inputing any discounts
            discounts: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[4]')))
            discounts.click()
            print("Working on Discounts")
            # This hits backspace since infor doesn't allow to type a decimal
            discountAmount: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/input')))
            discountAmount.clear()
            dec, whole = math.modf(discount)
            discountAmount.send_keys(int(whole))
            discountAmount.send_keys(Keys.TAB)
            discountAmount.click()
            actions = ActionChains(web)
            actions.key_down(Keys.CONTROL)
            actions.send_keys(Keys.ARROW_RIGHT)
            actions.key_up(Keys.CONTROL)
            actions.perform()
            discountAmount.send_keys(Keys.BACKSPACE)
            discountAmount.send_keys(Keys.BACKSPACE)
            dec *= 100
            discountAmount.send_keys(int(dec))
            discountDropdown: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div')))
            discountDropdown.click()
            discountType: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@id="dropdown-list"]/ul/li[1]/a')))
            discountType.click()
            discountAmount.click()
            time.sleep(inputTrans)
            submit: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[1]')))
            submit.click()
            time.sleep(inputTrans)
            finish: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[1]')))
            finish.click()

        except Exception:
            print("Wasn't able to do taxes and shipping")
            traceback.print_exc()
            raise

    def cancelFailedOrder() -> None:
        """cancels an order when a past cancled order goes wrong.
        """
        # Setting up web objects to be passed around
        web = EnviromentSetUp.web
        wait = WebDriverWait(web, 10)
        longerWait = WebDriverWait(web, 30)
        transition = 4
        inputTrans = 0.5

        try:
            time.sleep(transition)
            cancel: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[2]')))
            cancel.click()
            time.sleep(inputTrans)
            create: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[3]')))
            create.click()
            time.sleep(inputTrans)
            print("Canceling the past failed order...continuing after this order")

        except Exception:
            traceback.print_exc()
            print("Could not cancel order, will have to abort all")
            raise
