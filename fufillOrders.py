'''
This file has all the functions for running through all the order steps in infor
most of the selenium work will be done here.
'''
import json
import math
import time
import traceback

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Utils import jsonUtils
from WebDriver import EnviromentSetUp

# fufillOrders grabs the login info for a user


class fufillOrders(EnviromentSetUp):

    # FIXME: Error handling kinda sucks with printing to console... Make easier to troubleshoot
    def login(user, password) -> None:
        """starts the web selenium server and logs into infor on company 40. Ends up taking you to order entry page

        Args:
            user (str): username for infor
            password (str): password for infor
        """
        try:
            whatever = EnviromentSetUp
            whatever.setUp()
            web = EnviromentSetUp.web
            # this is the first page that they will be led to, which is some weird login
            web.get("https://xisrv.stronghandtools.com/infor/d7de089b-7e09-4476-a5f5-80697edc7524?favoriteContext=oeet.initiate&LogicalId=lid://infor.sx.1")
            signInUser = web.find_element(By.XPATH, '//*[@id="userNameInput"]')
            signInUser.send_keys("acumen@val2017")
            signInPassword = web.find_element(
                By.XPATH, '//*[@id="passwordInput"]')
            signInPassword.send_keys('17SHTinfor/')
            signInSubmit = web.find_element(
                By.XPATH, '//*[@id="submitButton"]')
            signInSubmit.click()
            wait = WebDriverWait(web, 30)
            longerWait = WebDriverWait(web, 120)

            # https://xisrv.stronghandtools.com/infor/d7de089b-7e09-4476-a5f5-80697edc7524
            # this is the second page that they will be led to, which is the infor loging

            # checking to see if the document management tab is open cause it needs to be closed
            documentMng: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="body"]/infor-mingle-shell/nav-menu/div/header/section[2]/drop-menu/div[1]/ul/li[5]')))
            if ("expanded" in documentMng.get_attribute("class")):
                close = web.find_element(
                    By.XPATH, '/html/body/div[2]/infor-mingle-shell/nav-menu/div/header/section[2]/drop-menu/div[1]/ul/li[5]/button')
                close.click()

            # elif("collapsed" in documentMng.get_attribute("class")):

            # entering the frame inside the infor website which is where all the action is
            wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.NAME, "sxeweb_d7de089b-7e09-4476-a5f5-80697edc7524")))  # class =m-app-frame
            inforUser: WebElement = longerWait.until(EC.element_to_be_clickable(  # /html/body/div[2]/div/section/form/div[2]/input or //*[@id="signin-userid"]
                (By.XPATH, '//*[@id="signin-userid"]')))
            inforUser.send_keys(str(user))

            inforPassword = web.find_element(
                By.XPATH, '//*[@id="signin-password"]')
            inforCompany = web.find_element(
                By.XPATH, '//*[@id="signin-company"]')

            inforPassword.send_keys(str(password))
            inforCompany.send_keys("40")

            inforSubmit = web.find_element(
                By.XPATH, '//*[@id="sign-in-view"]/section/form/button')
            inforSubmit.click()

            # FIXME: Sometimes inforOp will not pop up on the first time? I'll do a try catch for this where if it fails check to see if customer field is there, if not then raise error
            try:
                inforOp: WebElement = wait.until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'btn-modal-primary')))
                inforOp.click()
            except:
                try:
                    customerField = wait.until(EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[1]/span/input')))
                except:
                    raise
            customerField = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[1]/span/input')))

            print("logged in")

        except Exception:
            print("could not login")
            raise

    def closeWeb() -> None:
        """uses web.close() should work if there is still a web that is open
        """
        web = EnviromentSetUp.web
        web.close()

   # AV == shopify vs paypal which changes the customer number thign ex.40010

    def setUpOrder(po,  state,  country, method) -> None:
        '''
        :Args:
            - po - PO number from shopify of the customer
            - state - shipping state
            - country - shipping country
            - method - payment method used in shopify        
        '''
        try:

         # just gets ready to actually start looping through orders
            web = EnviromentSetUp.web
            wait = WebDriverWait(web, 10)

            if(method == "Shopify Payments"):
                print(country)
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
                        # print("CA worked")
                    else:
                        customer = "40004"
                        # print("out of state")k
                else:
                    customer = "40005"
                    # print("INT worked")k

            time.sleep(0.25)
            customerField: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[1]/span/input')))
            try:
                customerField.send_keys(str(customer))
                time.sleep(0.25)
            except:
                print("Only 'Paypal Express Checkout' and 'Shopify Payments' is accepted as a payment method. '",
                      method, "' was entered.")
                raise Exception("Invalid Payment Method entered.")

            warehouse = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[2]/span/input')
            warehouse.send_keys('V01')
            time.sleep(0.25)

            shipvia = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[2]/div[2]/span/input')

            time.sleep(.5)
            shipvia.clear()
            shipvia.send_keys('UG')

            time.sleep(.5)
            orderID = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[5]/input')
            orderID.send_keys(str(po))

            initNext = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[1]')
            initNext.click()
        except Exception:
            print("could not setup order")
            traceback.print_exc()
            raise

    def editShipping(name, address, city, state, zip, countryCode: str) -> None:
        """edits the shipping address in infor and gets ready to start adding line items.

        Args:
            name (str): shipping name
            address (str): shipping address
            city (str): shipping city
            state (str): state abbreviation
            zip (int): shipping zip
            country (str): shipping country
        """

        web = EnviromentSetUp.web
        wait = WebDriverWait(web, 10)
        try:
            editShip:WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[1]/div[1]/div/div[2]/div[2]/div/div/div/div/button')))
            editShip.click()

            nameField:WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/div/input')))
            nameField.clear()
            nameField.send_keys(str(name))

            addressField = web.find_element(
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[1]/input')
            addressField.clear()
            addressField.send_keys(str(address))

            cityField = web.find_element(
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[5]/input')  # /html/body/div[6]
            cityField.clear()
            cityField.send_keys(str(city))

            stateField = web.find_element(
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[6]/div[1]/input')
            stateField.clear()
            stateField.send_keys(str(state))

            zipField = web.find_element(
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[6]/div[2]/input')
            zipField.clear()
            zipField.send_keys(str(zip))

            # Comes from countries.json. Converts shopify country code to full name to use to find inner html
            countryDict = jsonUtils.readJSON()
            country = countryDict[countryCode]

            # TODO: make this work with all other countries.. maybe get a json with country codes and match them up to their actual country name. Test out taxes for it too.

            countryDrop: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[7]/div/div')))
            countryDrop.click()

            countryList: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@id="dropdown-list"]/ul')))

            countryClicked = False
            for child in countryList.find_elements(By.XPATH, './/*'):

                for otherChild in child.find_elements(By.XPATH, './/*'):

                    if(otherChild.get_attribute("innerHTML") == country):
                        otherChild.click()
                        countryClicked = True
                        break
                else:
                    continue
                break

            if (countryClicked == False):
                raise Exception("Country was not clicked")

            enterAddress = web.find_element(
                By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[3]/button[2]')
            enterAddress.click()

            lineEntry = wait.until(EC.element_to_be_clickable((
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[5]')))
            lineEntry.click()

            quickLine = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/div/ul/li[2]/a')
            quickLine.click()

        except Exception:
            print("could not edit shipping")
            traceback.print_exc()
            raise

    def addLineItem(sku, quantity, price: float) -> None:
        """adds in products to the product

        Args:
            sku (str): sku of product you are referring to
            quantity (int): quantity they are trying to buy
            price (float): price the product was sold for
        """
        try:
            web = EnviromentSetUp.web
            wait = WebDriverWait(web, 10)

            product = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/span/input')))
            product.send_keys(str(sku))

            quantityField = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[1]/input')
            quantityField.click()
            quantityField.clear()
            quantityField.send_keys(quantity)

            priceField = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[3]/input')
            priceField.clear()
            time.sleep(0.5)
            priceField.click()
            priceField.send_keys(price)

            add = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/button')
            add.click()

        except Exception:
            print("wasn't able to add a line item")
            traceback.print_exc()

    def finishOrder(shipping: float, discount, zip: int, shopTotalQuantity: int) -> None:
        """does taxes and shipping, then gets ready to do next order entry

        Args:
            shipping (float): shipping amount
            discount (float): discount amount
            zip (int): zip code
        """
        try:
            web = EnviromentSetUp.web
            wait = WebDriverWait(web, 10)

            data = json.loads(open("cities.json").read())
            state = ''
            for i in data:

                if str(i['zip_code']) == str(zip):

                    county = (i['county'])
                    state = (i['state'])
                    city = (i['city'])
                    break
            # FIXME: make sure we are putting down the right quantiy of products before proceeding, because ezra says we have not been doing that
            # so i need a total products in the dict and i need to find the html for it here and some code to check if they are matching.
            # if they are not matching raise error.

            totalQuantityElement: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/span[2]')))

            inforTotalQuanity = ((totalQuantityElement.get_attribute(
                "innerHTML")).replace("(", "")).replace(")", "")

            print("infor total:\t", inforTotalQuanity)
            print("shop quant: \t", shopTotalQuantity)

            if(shopTotalQuantity == int(inforTotalQuanity)):
                print("good!", "\n")
            else:
                print("bad")
                raise Exception("Total quantiy does not match")

            addLines: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/button[1]')))

            addLines.click()

            time.sleep(4)
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

            time.sleep(0.25)
            try:
                if (state == "CA"):
                    stateDrop: WebElement = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/div')))

                    stateDrop.click()
                    time.sleep(0.5)

                    stateDrop = web.find_element(
                        By.XPATH, '/html/body/div[@id="dropdown-list"]/span')
                    stateDrop.click()
                    countyField = web.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[2]/div/div')
                    countyField.click()
                    time.sleep(0.25)
                    county = str(county).upper()

                    if(len(county) > 12):
                        shortCounty = county[0:12]
                    else:
                        shortCounty = county

                    countyList = web.find_element(
                        By.XPATH, '/html/body/div[@id="dropdown-list"]/ul')
                    cityState = False
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

                    if (cityState == False):
                        print("City was not clicked in Taxes section")
                        raise Exception("City Not Found")

                    cityField = web.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div')
                    cityField.click()
                    time.sleep(0.25)
                    city = str(city).upper()
                    county = county.replace(" ", "")
                    betterCounty = county[0:4]
                    if(len(city) > 12):
                        betterCity = city[0:12]+"-"+betterCounty
                    else:
                        betterCity = city+"-"+betterCounty

                    cityList = web.find_element(
                        By.XPATH, '/html/body/div[@id="dropdown-list"]/ul')

                    for child in cityList.find_elements(By.XPATH, './/*'):
                        for otherChild in child.find_elements(By.XPATH, './/*'):

                            if(otherChild.get_attribute("innerHTML") == betterCity.replace(" ", "")):
                                otherChild.click()
                                break
                            elif(otherChild.get_attribute("innerHTML") == betterCity):
                                otherChild.click()
                                break
                        else:
                            continue
                        break

            except UnboundLocalError:
                print("not defined")

            recalculate = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[3]')))
            recalculate.click()
            time.sleep(3)
            addons: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[2]')))
            addons.click()

            addShipping = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[1]/div/button')))
            addShipping.click()

            freightDropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[1]/div/div/div[1]/div/div')))
            freightDropdown.click()

            freight = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@id="dropdown-list"]/ul/li[3]/a')))
            freight.click()

            freightAmount = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[1]/div/div/div[2]/input')))
            freightAmount.clear()
            time.sleep(0.5)
            freightAmount.send_keys(shipping)

            finishFreight = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[2]/div[2]/button[1]')
            finishFreight.click()

            goBack = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[1]/div/button')))
            time.sleep(2)
            goBack.click()

            discounts = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[4]')))
            discounts.click()

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

            discountDropdown = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div')
            discountDropdown.click()

            discountType = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@id="dropdown-list"]/ul/li[1]/a')))
            discountType.click()

            discountAmount.click()

            submit = web.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[1]')
            submit.click()

            finish = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[1]')))
            finish.click()

        except Exception:
            print("Wasn't able to do taxes and shipping")
            traceback.print_exc()
            raise

    def cancelFailedOrder() -> None:
        """cancels an order when a past cancled order goes wrong.
        """
        web = EnviromentSetUp.web
        wait = WebDriverWait(web, 10)
        try:
            time.sleep(4)
            cancel: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[2]')))
            cancel.click()
            create: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[3]')))
            create.click()
            print("Canceling the past failed order...continuing after this order")
        except Exception:
            traceback.print_exc()
            print("Could not cancel order, will have to abort all")
            raise
