import os

import PySimpleGUI as sg

from inforOrders.fufillOrders import fufillOrders
from inforOrders.Utils import csvUtils


def setUpGui() -> sg.Window:
    """This sets up the main GUI with themes and stuff

    Returns:
        window: selenium window
    """

    # Add a touch of color DarkBlue3 or Default
    sg.theme('DefaultNoMoreNagging')

    # All the stuff inside your window.
    layout = [
        [sg.Push(), sg.Text('Enter your infor Login!'), sg.Push()],
        [sg.Push(), sg.Text('Order Automation: Version 1.4'), sg.Push()],
        [sg.Push(), sg.Text('', key="-Update-", text_color="red"), sg.Push()],
        [sg.Text('Username:'), sg.InputText(key="-Username-")],
        [sg.Text('Password:'), sg.InputText(key="-Password-")],
        [sg.Push(), sg.Text('Import the CSV file from Shopify'), sg.Push()],
        [sg.Push(), sg.Input(enable_events=True, size=(18, 1)),
            sg.FileBrowse(key="-File-"), sg.Push()],
        [sg.Push(), sg.Button('Ok'), sg.Button('Cancel')],
        [sg.Push(), sg.Text('', key="-Failed-", text_color="red"), sg.Push()],
        [sg.Push(), sg.Text('', key="-Finished-", text_color="green"), sg.Push()],
        [sg.Push(), sg.Button('Export Failed Orders', key='-Export-'), sg.Push()],
    ]

    # Create the Window
    window = sg.Window('Order Automation', layout, resizable=True)
    return window


def main():
    window = setUpGui()

    while True:
        event, values = window.read()

        if event == 'Ok':

            finishedOrders = []
            failedOrders = []

            # NOTE: Tries to login and if not then brings the window in focus to try again
            try:
                fufillOrders.login(values["-Username-"], values["-Password-"])
            except Exception:
                window['-Update-'].update("Could not login. Try again!")
                window.force_focus()
                continue

            orders = csvUtils.readCSV(values["-File-"])

            # For loop to go through each order. Must be logged in first.
            for orderNumber, value in orders.items():
                try:
                    fufillOrders.setUpOrder(
                        orderNumber, value["shippingState"], value["shippingCountry"], value["method"])

                except Exception:
                    # Will relogin
                    print("Could not do order " + orderNumber)
                    failedOrders.append(orderNumber)
                    fufillOrders.closeWeb()
                    fufillOrders.login(
                        values["-Username-"], values["-Password-"])
                    continue

                try:
                    fufillOrders.editShipping(value["shippingName"], value["shippingStreet"], value["shippingCity"],
                                              value["shippingState"], value["shippingZip"], value["shippingCountry"])
                    for item in value["lineItems"]:
                        # Looping through each line item
                        fufillOrders.addLineItem(
                            item["sku"], item["quantity"], item["price"])
                    fufillOrders.finishOrder(
                        value["shippingAmount"], value["discount"], value["shippingZip"], len(value["lineItems"]))

                    # Finished order and add to array
                    finishedOrders.append(orderNumber)
                    print("Finished order " + orderNumber, "\n")

                except Exception:
                    # Will relogin and cancel previous order then continue
                    print("Could not do order " + orderNumber)
                    failedOrders.append(orderNumber)
                    fufillOrders.login(
                        values["-Username-"], values["-Password-"])
                    fufillOrders.cancelFailedOrder()
                    continue

            # Prints failed and finished orders to GUI
            window['-Failed-'].update("Failed orders: "+str(failedOrders))
            window['-Finished-'].update("Finished orders: " +
                                        str(finishedOrders))

            csvUtils.createCSV(finishedOrders, failedOrders)
            window.force_focus()
            fufillOrders.closeWeb()
            print("inished")# TODO: Make this on the GUI instead

        if event == '-Export-':
            os.system('orders.csv')

        if event in (sg.WIN_CLOSED, 'Cancel'):  # If user closes window or clicks cancel
            try:
                fufillOrders.closeWeb()
            except Exception:
                print("Not closed properly..doesn't matter")
            break

    window.close()


if __name__ == "__main__":
    main()
