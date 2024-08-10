import PySimpleGUI as sg
import sqlite3

conn = sqlite3.connect("Contacts.db")

cursor = conn.cursor()

# Create table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS CONTACTS (Name text, Number string, Relation text)")

def menu():
    layout = [  [sg.Text("----MENU----")],
            [sg.Text("1. ADD A NEW NUMBER"), sg.Button("1")],
            [sg.Text("2. DELETE A NUMBER"), sg.Button("2")],
            [sg.Text("3. SEARCH FOR A NUMBER"), sg.Button("3")],
            [sg.Text("4. VIEW ALL THE CONTACTS"), sg.Button("4")],
            [sg.Text("5. TO VIEW THE CONTACTS OF A PARTICULAR RELATION "), sg.Button("5")],
            [sg.Text("6. EXIT"), sg.Button("CANCEL")] ]
    window = sg.Window('Window Title', layout)
    event = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        return
    return event[0]

while True:
    choice = menu()
    if choice == '1':
        layout = [ [sg.Text("Enter name:"),sg.Input()],
                [sg.Text("Enter number:"),sg.Input()],
                [sg.Text("Enter relation:"),sg.Input()],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
        window = sg.Window('1. ADD A NEW NUMBER', layout)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        else:
            cursor.execute("INSERT INTO CONTACTS VALUES (?,?,?)", (values[0], values[1], values[2]))
            conn.commit()
        sg.popup('Contact added successfully')
    
    
    
    
    
    
    elif choice == '6':
        break





#name = sg.popup_get_text('What is your name?')
#print(name)


# Event Loop to process "events" and get the "values" of the inputs
"""while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()"""