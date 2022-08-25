import os

import PySimpleGUI as sg
from fufillOrders import fufillOrders
from Utils import csvUtils


def setUpGui() -> sg.Window:
    """This sets up the main GUI with themes and stuff

    Returns:
        window: selenium window
    """

    # Add a touch of color DarkBlue3 or Default
    sg.theme('DefaultNoMoreNagging')
    # All the stuff inside your window.

    layout = [
        # [sg.Titlebar(title='Order Automation')],
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
# window = setUpGui()


def main():
    window = setUpGui()

    while True:
        event, values = window.read()

        if event == 'Ok':
            csvInput = values["-File-"]

            orders = csvUtils.readCSV(csvInput)
            # NOTE: Tries to login and if not then brings the window in focus to try again
            try:
                fufillOrders.login(values["-Username-"], values["-Password-"])
            except Exception:
                window['-Update-'].update("Could not login. Try again!")
                window.force_focus()
                continue

            finishedOrders = []
            failedOrders = []

            # For loop to go through each order. Must be logged in first.
            for key, value in orders.items():

                # this will try to set up the order
                try:
                    fufillOrders.setUpOrder(
                        key, value["shippingState"], value["shippingCountry"], value["method"])
                # will only login, wont cancel order since it doesnt need to then continue
                except Exception:
                    print("Could not do order " + key)
                    failedOrders.append(key)
                    fufillOrders.closeWeb()
                    fufillOrders.login(
                        values["-Username-"], values["-Password-"])
                    continue

                # will try to do the rest of the order, will need to cancel order if fails
                try:
                    # edit shipping stuff
                    try:
                        fufillOrders.editShipping(value["shippingName"], value["shippingStreet"], value["shippingCity"],
                                                  value["shippingState"], value["shippingZip"], value["shippingCountry"])
                    except Exception:
                        raise

                    # Tries to add line items
                    try:
                        for item in value["lineItems"]:

                            fufillOrders.addLineItem(
                                # all the values from the line items
                                item["sku"], item["quantity"], item["price"])
                    except Exception:
                        raise

                    # Finishes up the order by doing taxes and shipping
                    try:
                        fufillOrders.finishOrder(
                            value["shippingAmount"], value["discount"], value["shippingZip"], len(value["lineItems"]))
                    except Exception:
                        raise

                    # finished order and add to array
                    finishedOrders.append(key)
                    print("Finished order " + key)

                # Will relogin and cancel previous order then continue
                except Exception:
                    print("Could not do order " + key)
                    failedOrders.append(key)

                    fufillOrders.login(
                        values["-Username-"], values["-Password-"])
                    fufillOrders.cancelFailedOrder()
                    continue

            # prints failed and finished orders to gui
            window['-Failed-'].update("Failed orders: "+str(failedOrders))
            window['-Finished-'].update("Finished orders: " +
                                        str(finishedOrders))

            csvUtils.createCSV(finishedOrders, failedOrders)

            window.force_focus()

            fufillOrders.closeWeb()
            print("finished")
        if event == '-Export-':
            os.system('orders.csv')
        if event in (sg.WIN_CLOSED, 'Cancel'):  # if user closes window or clicks cancel
            try:
                fufillOrders.closeWeb()
            except Exception:
                print("not closed properly..doesn't matter")
            break

    window.close()


if __name__ == "__main__":
    main()
