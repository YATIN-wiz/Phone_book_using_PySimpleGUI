import PySimpleGUI as sg
import sqlite3

conn = sqlite3.connect("Contacts.db")

cursor = conn.cursor()

# Create table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS CONTACTS (Name text, Number string, Relation text)")

def menu():
    layout = [[ sg.Input(),sg.Button("SEARCH")],
              [ sg.Button("NEW CONTACT")],]
    window = sg.Window('Window Title', layout) # change the windown title
    event,values = window.read()
    print(event)
    if event == sg.WIN_CLOSED or event == 'Cancel': 
        return event,values[0]
    window.close()
    return event,values[0]


while True:
    event,name = menu()
  
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'SEARCH':
        cursor.execute("SELECT * FROM CONTACTS WHERE Name=?", (name,))
        
        result = cursor.fetchone()
       
        if result:
            
            layout = [[sg.Text(f"Name: {result[0]}, Number: {result[1]}, Relation: {result[2]}")], #change relation to category
                      [sg.Button("DELETE")],
                      [sg.Button("EDIT")]] #use this layout for the SEARCH event also. 
            #make the Texts 'disabled' so that the used wont be able to edit it at the first place
            #then when the user clicks on "edit contact" they should become 'enabled'
            #This is to learn dynamic state change of the controls/GUI elements.
            #This way you can remove one layout.
            window = sg.Window('Contact Details', layout)
            events = window.read()
            print(events)
            window.close()
            if events == sg.WIN_CLOSED or events == 'Cancel': 
                break
            elif events[0] == "DELETE":
                cursor.execute("DELETE FROM CONTACTS WHERE Name=?", (name,))
                conn.commit()
                sg.popup("Contact deleted successfully!")
                window.close()
            elif events[0] == "EDIT":
                layout = [ [sg.Text("Enter new name:"),sg.Input(result[0])], #remove 'enter' from everywhere
                        [sg.Text("Enter new number:"),sg.Input(result[1])],
                        [sg.Text("Enter new relation:"),sg.Input(result[2])],
                        [sg.Button('Save'), sg.Button('Cancel')] ]
                window = sg.Window('Edit Contact', layout)
                res, val = window.read()
                if res == sg.WIN_CLOSED or res == 'Cancel':
                    window.close()
                    continue
                cursor.execute("UPDATE CONTACTS SET Name=?, Number=?, Relation=? WHERE Name=?", (val[0], val[1], val[2], name))
                conn.commit()
                sg.popup("Contact updated successfully!")
            window.close()
                
        
        else:
            sg.popup("Name not found!")

    elif event == 'NEW CONTACT':
        layout = [ [sg.Text("Enter name:"),sg.Input()],
                [sg.Text("Enter number:"),sg.Input()],
                [sg.Text("Enter relation:"),sg.Input()],
                [sg.Button('Save'), sg.Button('Cancel')] ]
        window = sg.Window('NEW CONTACT', layout)
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            continue
        cursor.execute("INSERT INTO CONTACTS VALUES (?,?,?)", (values[0], values[1], values[2]))
        conn.commit()
        sg.popup("Contact added successfully!")
        window.close()  

    
