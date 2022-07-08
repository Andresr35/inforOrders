import PySimpleGUI as sg
from WebDriver import EnviromentSetUp
from csvUtils import csvUtils
from fufillOrders import fufillOrders
import json

PATH = "C:\Program Files (x86)\chromedriver.exe"



#andresisabozo
class Window:

    def setUpGui():
        
        sg.theme('DarkAmber')   # Add a touch of color
        # All the stuff inside your window.
        layout = [ 
                [sg.Text('Select your csv file'), sg.FileBrowse(key="-File-")],
                [sg.Button('Ok'), sg.Button('Cancel')] ]

        # Create the Window
        window = sg.Window('Window Title', layout)
        return window
      
    window = setUpGui()

    while True:
        event, values = window.read()
        # csvInput = values["-File-"]
        csvInput = 'orders_export (4).csv'

        if event == 'Ok':
        #     orders = csvUtils.readCSV(csvInput)#the dict holding all the orders
        #     fufillOrders.login("ANR","ANR@0117")
        #     for key,value in orders.items():
        #         fufillOrders.setUpOrder(key,value["shippingName"],value["shippingStreet"],value["shippingCity"],value["shippingState"],value["shippingZip"],value["shippingCountry"])
        #         #all the values of an order
        #         for item in value["lineItems"]:
        #             fufillOrders.addLineItem(item["sku"],item["quantity"],item["price"])
        #             #all the values from the line items
                    
        #         fufillOrders.finishOrder(value["shippingAmount"],value["discount"],value["shippingZip"])


            print("out of loop")
            # print(json.dumps(orders,indent=4,sort_keys=True))
            fufillOrders.login("ANR","ANR@0117")
            fufillOrders.setUpOrder("test74","testName","testAddress","Santa Fe Springs","CA",90670,"United States","PayPal Express Checkout")
            fufillOrders.addLineItem("F5-MES008-FE-BDK",4,30)
            fufillOrders.finishOrder(20,2,54929)
            # 
            # 
            # fufillOrders.addLineItem("F5-MES008-FE-BDK",4,30)
            # 

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            fufillOrders.closeWeb()
            break
        

    window.close()




