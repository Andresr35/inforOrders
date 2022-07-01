import json
import time
import traceback
from pytz import country_names

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from WebDriver import EnviromentSetUp


class fufillOrders(EnviromentSetUp):

    def login(user,password):
        try:
            whatever = EnviromentSetUp
            whatever.setUp()
            web = EnviromentSetUp.web
            #this is the first page that they will be led to, which is some weird login
            web.get("https://xisrv.stronghandtools.com/infor/d7de089b-7e09-4476-a5f5-80697edc7524?favoriteContext=oeet.initiate&LogicalId=lid://infor.sx.1")
            signInUser=web.find_element(By.XPATH,'//*[@id="userNameInput"]')
            signInUser.send_keys("acumen@val2017")
            signInPassword=web.find_element(By.XPATH,'//*[@id="passwordInput"]')
            signInPassword.send_keys('17SHTinfor/')
            signInSubmit=web.find_element(By.XPATH,'//*[@id="submitButton"]')
            signInSubmit.click()
            wait = WebDriverWait(web,10)

            #https://xisrv.stronghandtools.com/infor/d7de089b-7e09-4476-a5f5-80697edc7524
            # this is the second page that they will be led to, which is the infor loging
          
            
            #checking to see if the document management tab is open cause it needs to be closed
            documentMng = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="body"]/infor-mingle-shell/nav-menu/div/header/section[2]/drop-menu/div[1]/ul/li[5]')))
            if ("expanded" in documentMng.get_attribute("class")):
                close = web.find_element(By.XPATH,'/html/body/div[2]/infor-mingle-shell/nav-menu/div/header/section[2]/drop-menu/div[1]/ul/li[5]/button')
                close.click()
                print("i closed it")
            elif("collapsed" in documentMng.get_attribute("class")):
                print("it is closed")

            #entering the frame inside the infor website which is where all the action is
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"sxeweb_d7de089b-7e09-4476-a5f5-80697edc7524")))#class =m-app-frame
            inforUser = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="signin-userid"]')))
            inforUser.send_keys(str(user))

            inforPassword = web.find_element(By.XPATH,'//*[@id="signin-password"]')
            inforCompany = web.find_element(By.XPATH,'//*[@id="signin-company"]')

            inforPassword.send_keys(str(password))
            inforCompany.send_keys("40")

            inforSubmit=web.find_element(By.XPATH,'//*[@id="sign-in-view"]/section/form/button')
            inforSubmit.click()
            inforOp = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'btn-modal-primary')))
            inforOp.click()
            print("logged in")
            

        except Exception:
            print("Wasn't able to login")
            traceback.print_exc()
           
    def closeWeb():
        EnviromentSetUp.closeWeb()
   
    def setUpOrder(po,name,address,city,state,zip,country,customer="40010"):
        #just gets ready to actually start looping through orders
        web = EnviromentSetUp.web
        wait = WebDriverWait(web,10)
        # 2124 in customer |warehouse v01 | customer po # = order number| ship via prepaid something | next
        customerField = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[1]/span/input')))
        customerField.send_keys(str(customer))

        warehouse=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[2]/span/input')
        warehouse.send_keys('V01')


        # shipvia=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[2]/div[2]/span/input')
        # print(shipvia.get_attribute("value"))
        # print("text should be ^")
        # time.sleep(3)
        # shipvia.clear()
        # shipvia.send_keys('UG')
        time.sleep(.5)
        orderID=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[5]/input')
        orderID.send_keys(str(po))#--------------------------------------------------------------ADD ONE

        initNext=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[1]')
        initNext.click()

        # edit ship to address| three dot settings line entry quick| quantity| part number | add
        editShip=wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[1]/div[1]/div/div[2]/div[2]/div/div/div/div/button')))
        editShip.click()
        

        nameField = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/div/input')))
        nameField.clear()
        nameField.send_keys(str(name))

        addressField =web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[1]/input')
        addressField.clear()
        addressField.send_keys(str(address))

        cityField = web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[5]/input')
        cityField.clear()
        cityField.send_keys(str(city))

        stateField = web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[6]/div[1]/input')
        stateField.clear()
        stateField.send_keys(str(state))

        zipField=web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[6]/div[2]/input')
        zipField.clear()
        zipField.send_keys(zip)

        countryField = Select(web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[7]/select'))
        countryField.select_by_visible_text(str(country))

        enterAddress = web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[3]/button[2]')
        enterAddress.click()
        
        settings = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[3]/button')
        settings.click()

        lineEntry = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[5]')
        lineEntry.click()

        quickLine = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/div/ul/li[2]/a')
        quickLine.click()
        
    def addLineItem(sku,quantity,price:float):
        web=EnviromentSetUp.web
        wait = WebDriverWait(web,10)

        product = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/span/input')))
        product.send_keys(str(sku))

        quantityField = web.find_element(By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[1]/input')
        quantityField.click()
        quantityField.clear()    
        quantityField.send_keys(quantity)

        priceField = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[3]/input')
        priceField.clear()
        time.sleep(0.5)
        priceField.click()
        priceField.send_keys(price)

        add =web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/button')
        add.click()
    
    def finishOrder(shipping,discount,zip:int): 
        try:
            web=EnviromentSetUp.web
            wait =WebDriverWait(web,10)


            data = json.loads(open("cities.json").read())

            for i in data:
                if i['zip_code'] == zip:
                    county =(i['county'])
                    state = (i['state'])
                    city = (i['city'])
                    break

            addLines = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/button[1]')))
            addLines.click()

            taxButton = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[1]/div/div/div/a[3]')))
            taxButton.click()

            if (state == "CA"):
                countryDrop = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/div')))
                countryDrop.click()
                time.sleep(0.5)
                countryDrop=web.find_element(By.XPATH,'/html/body/div[8]/span')
                countryDrop.click()
                countyField = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[2]/div/div')
                countyField.click()
                time.sleep(0.25)
                county = str(county).upper()
                countyList = web.find_element(By.XPATH,'/html/body/div[8]/ul')

                for child in countyList.find_elements(By.XPATH,'.//*'):
                    for otherChild in child.find_elements(By.XPATH,'.//*'):               
                        
                        if(otherChild.get_attribute("innerHTML") == county.replace(" ","")):
                            otherChild.click()
                            break
                        elif(otherChild.get_attribute("innerHTML") == county):
                            otherChild.click()
                            break
                    else:
                        continue
                    break

                cityField = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div')
                cityField.click()
                time.sleep(0.25)
                city = str(city).upper()
                if(len(city)>12):
                    betterCity = city[0:12]
                county = county.replace(" ","")
                betterCounty =county[0:4]
                betterCity+="-"+betterCounty
                cityList = web.find_element(By.XPATH,'/html/body/div[8]/ul')

                for child in cityList.find_elements(By.XPATH,'.//*'):
                    for otherChild in child.find_elements(By.XPATH,'.//*'):
                        print(otherChild.get_attribute("innerHTML"))
                        #SANTA FE SPR-LOSA first 12 + "-LOSA"
                        #RANCHO DOMIN-LOSA    HACIENDA HEI-LOSA
                        if(otherChild.get_attribute("innerHTML") == betterCity.replace(" ","")):
                            otherChild.click()
                            break
                        elif(otherChild.get_attribute("innerHTML") == betterCity):
                            otherChild.click()
                            break
                    else:
                        continue
                    break
                    

            recalculate = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[3]')))
            recalculate.click()
            time.sleep(1)
            addons = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[2]')))
            addons.click()

            addShipping = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[1]/div/button')))
            addShipping.click()
            
            freight = Select(wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[1]/div/div/div[1]/select'))))
            freight.select_by_value('freight charge')
            
            freightAmount =wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[1]/div/div/div[2]/input')))
            freightAmount.clear()
            freightAmount.send_keys(shipping)

            finishFreight = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/div/div/div/div/div[2]/div[2]/button[1]')
            finishFreight.click()

            goBack = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[1]/div/button')
            goBack.click()

            discounts = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[4]')
            discounts.click()

            discountAmount = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/input')
            discountAmount.clear()
            discountAmount.send_keys(discount)

            discountType = Select(web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/select'))
            discountType.select_by_visible_text("Amount")

            submit =web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[1]')
            submit.click()
        
        except Exception:
            print("Wasn't able to login")
            traceback.print_exc()
        # customerSettings = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[4]')
        # customerSettings.click()
