import PySimpleGUI as sg
from WebDriver import EnviromentSetUp
from csvUtils import csvUtils
from fufillOrders import fufillOrders


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
        csvInput = values["-File-"]
        if event == 'Ok':
            print(csvUtils.readCSV(csvInput))
            fufillOrders.login("ANR","ANR@0117")
            fufillOrders.setUpOrder("test2","testName","testAddress","Santa Fe Springs","CA",90670,"United States","40010")
            fufillOrders.addLineItem("FB-CT202-4",2)
            fufillOrders.addLineItem("F5-MES008-FE-BDK",4)

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            fufillOrders.closeWeb()
            break
        

    window.close()




