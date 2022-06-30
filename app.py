import PySimpleGUI as sg
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
            res = fufillOrders.login("ANR","ANR@0117")
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        

    window.close()




