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
            [sg.Text("6. EXIT"), sg.Button("6")] ]
    window = sg.Window('Window Title', layout)
    event = window.read()
    window.close()
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
        window.close()

    elif choice == '2':
        layout = [ [sg.Text("Enter name to delete:"),sg.Input()],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
        window = sg.Window('2. DELETE A NUMBER', layout)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        else:
            result = cursor.execute("DELETE FROM CONTACTS WHERE Name=?", (values[0],))
            conn.commit()
            if result.rowcount == 0:
                sg.popup("Name not found!")
            else:
                sg.popup('Contact deleted successfully')
        window.close()

    elif choice == '3':
        layout = [ [sg.Text("Enter name to search:"),sg.Input()],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
        window = sg.Window('3. SEARCH FOR A NUMBER', layout)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        else:
            cursor.execute("SELECT * FROM CONTACTS WHERE Name=?", (values[0],))
            result = cursor.fetchall()
            for record in result:
                sg.popup(f"Name: {record[0]}, Number: {record[1]}, Relation: {record[2]}")
           
        """ else:
                sg.popup('Contact not found')"""
    elif choice == '4':
        cursor.execute("SELECT * FROM CONTACTS")
        result = cursor.fetchall()
        for record in result:
            
            sg.popup(f"Name: {record[0]}, Number: {record[1]}, Relation: {record[2]}")
    
    elif choice == '5':
        layout = [ [sg.Text("Enter relation to view:"),sg.Input()],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
        window = sg.Window('5. VIEW THE CONTACTS OF A PARTICULAR RELATION', layout)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        else:
            cursor.execute("SELECT * FROM CONTACTS WHERE Relation=?", (values[0],))
            result = cursor.fetchall()
            for record in result:
                sg.popup(f"Name: {record[0]}, Number: {record[1]}, Relation: {record[2]}")
            """else:
                sg.popup('No contacts found for this relation')"""
       
        window.close()

    elif choice == '6':
        break