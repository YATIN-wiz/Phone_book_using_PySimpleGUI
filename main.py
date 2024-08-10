import PySimpleGUI as sg
layout = [  [sg.Text("----MENU----")],
            [sg.Text("1. ADD A NEW NUMBER"), sg.Button("1")],
            [sg.Text("2. DELETE A NUMBER"), sg.Button("2")],
            [sg.Text("3. SEARCH FOR A NUMBER"), sg.Button("3")],
            [sg.Text("4. VIEW ALL THE CONTACTS"), sg.Button("4")],
            [sg.Text("5. TO VIEW THE CONTACTS OF A PARTICULAR RELATION "), sg.Button("5")],
            [sg.Text("6. EXIT"), sg.Button("CANCEL")] ]

# Create the Window
window = sg.Window('Window Title', layout)


#name = sg.popup_get_text('What is your name?')
#print(name)


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()