import json

import PySimpleGUI as sg

from csvUtils import csvUtils
from fufillOrders import fufillOrders
from WebDriver import EnviromentSetUp

PATH = "C:\Program Files (x86)\chromedriver.exe"


# andresisabozo
class Window:

    def setUpGui():

        # Add a touch of color DarkBlue3 or Default
        sg.theme('DefaultNoMoreNagging')
        # All the stuff inside your window.

        layout = [
            # [sg.Titlebar(title='Order Automation')],
            [sg.Push(), sg.Text('Enter your infor Login!'), sg.Push()],
            [sg.Push(), sg.Text('', key="-Update-", text_color="red"), sg.Push()],
            [sg.Text('Username:'), sg.InputText(key="-Username-")],
            [sg.Text('Password:'), sg.InputText(key="-Password-")],
            [sg.Push(), sg.Text('Import the CSV file from Shopify'), sg.Push()],
            [sg.Push(), sg.Input(enable_events=True, size=(18, 1)),
             sg.FileBrowse(key="-File-"), sg.Push()],
            [sg.Push(), sg.Button('Ok'), sg.Button('Cancel')]]

        # Create the Window
        window = sg.Window('Order Automation', layout)
        return window

    window = setUpGui()

    while True:
        event, values = window.read()
        csvInput = values["-File-"]
        # csvInput = 'orders_export (4)(1).csv'KC

        if event == 'Ok':

            # the dict holding all the orders
            orders = csvUtils.readCSV(csvInput)
            try:
                fufillOrders.login(values["-Username-"], values["-Password-"])
            except Exception:
                print("could not login")
                window['-Update-'].update("Could not login. Try again!")
                window.force_focus()
                continue

            for key, value in orders.items():

                fufillOrders.setUpOrder(key, value["shippingName"], value["shippingStreet"], value["shippingCity"],
                                        value["shippingState"], value["shippingZip"], value["shippingCountry"], value["method"])

                # all the values of an order

                for item in value["lineItems"]:

                    fufillOrders.addLineItem(
                        item["sku"], item["quantity"], item["price"])
                    # all the values from the line items

                fufillOrders.finishOrder(
                    value["shippingAmount"], value["discount"], value["shippingZip"])

            print("out of loop")
            # print(json.dumps(orders,indent=4,sort_keys=True))
            # fufillOrders.login("ANR","ANR@0117")
            # fufillOrders.setUpOrder("test85","testName","testAddress","Clintonville","WI",54929,"United States","PayPal Express Checkout")
            # fufillOrders.addLineItem("F5-MES008-FE-BDK",4,30)
            # fufillOrders.finishOrder(20,2,54929)
            # #
            #
            # fufillOrders.addLineItem("F5-MES008-FE-BDK",4,30)
            #

        # if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):  # if user closes window or clicks cancel
            try:
                fufillOrders.closeWeb()
            except Exception:
                print("not closed properly..doesn't matter")
            break
    window.close()
