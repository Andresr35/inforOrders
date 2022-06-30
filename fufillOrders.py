from distutils.log import error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
import traceback


class fufillOrders:
    def login(user,password):
        try:
            web = webdriver.Chrome()

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
            return web
            
        except Exception:
            print("Wasn't able to login")
            traceback.print_exc()
            return web


        # # 2124 in customer |warehouse v01 | customer po # = order number| ship via prepaid something | next
        # customer = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[1]/span/input')
        # customer.send_keys(2124)

        # warehouse=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[2]/span/input')
        # warehouse.send_keys('V01')

        # shipvia=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[2]/div[2]/span/input')
        # time.sleep(3)
        # shipvia.clear()
        # shipvia.send_keys('PPA')

        # orderID=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[2]/div/div[2]/div/div/div[1]/div[5]/input')
        # orderID.send_keys(54371)#--------------------------------------------------------------ADD ONE

        # initNext=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/form/div/div[1]/div/div[2]/button[1]')
        # initNext.click()
        # time.sleep(5)

        # # edit ship to address| three dot settings line entry quick| quantity| part number | add
        # editShip=web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[1]/div[1]/div/div[2]/div[2]/div/div/div/div/button')
        # editShip.click()
        # time.sleep(3)

        # name = web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/div/input')
        # name.clear()
        # name.send_keys("testName")

        # address =web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[1]/input')
        # address.clear()
        # address.send_keys('8750 Pioneer')

        # city = web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[5]/input')
        # city.clear()
        # city.send_keys('testCity')

        # state = web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[6]/div[1]/input')
        # state.clear()
        # state.send_keys('CA')

        # zip=web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[6]/div[2]/input')
        # zip.clear()
        # zip.send_keys(90670)

        # country = Select(web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[2]/div/custom-control/div/div/div/div[7]/select'))
        # country.select_by_visible_text("United States")

        # enterAddress = web.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/form/div[3]/button[2]')
        # enterAddress.click()

        # web.maximize_window()

        # settings = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[3]/button')
        # settings.click()

        # lineEntry = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[5]')
        # lineEntry.click()

        # quickLine = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/div/ul/li[2]/a')
        # quickLine.click()
        # time.sleep(3)

        # product = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/span/input')
        # product.send_keys("gh-12050")

        # quantity = web.find_element(By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[1]/input')
        # quantity.click()
        # quantity.clear()    
        # quantity.send_keys(5)

        # add =web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[1]/div/div/button')
        # add.click()
        # time.sleep(2)
        # # add lines | three dots customer order settings | check stuff???????????? save | back | Finsih

        # addLines = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/button[1]')
        # addLines.click()
        # time.sleep(3)

        # customerSettings = web.find_element(By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div/div/div[1]/div/form/div/div[1]/div/div[2]/button[4]')
        # customerSettings.click()
        # time.sleep(3)

        # input()
        # web.close()