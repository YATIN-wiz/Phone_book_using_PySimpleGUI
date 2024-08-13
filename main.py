import PySimpleGUI as sg
import sqlite3

conn = sqlite3.connect("Contacts.db")

cursor = conn.cursor()

# Create table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS CONTACTS (Name text, Number string, Relation text)")

def menu():
    layout = [[ sg.Input(),sg.Button("SEARCH")],
              [ sg.Button("NEW CONTACT")],]
    window = sg.Window('Window Title', layout)
    event,values = window.read()
    print(event)
    if event == sg.WIN_CLOSED or event == 'Cancel': 
        return event,values[0]
    window.close()
    return event,values[0]


while True:
    event,value = menu()
    print(event,value)
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    
