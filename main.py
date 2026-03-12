import re
import sqlite3

import FreeSimpleGUI as sg  


if hasattr(sg, "theme"):
    sg.theme("DarkBlue3")


DB_FILE = "Contacts.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS CONTACTS (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT    NOT NULL,
        phone    TEXT    NOT NULL,
        email    TEXT
    )
""")
conn.commit()




def validate_contact(name: str, phone: str):  # returns str (error msg) or None
    """Return an error message string, or None if inputs are valid."""
    if not name.strip():
        return "Name cannot be empty."
    if not phone.strip():
        return "Phone cannot be empty."
    # Allow digits, spaces, +, -, (, )
    if not re.fullmatch(r"[\d\s\+\-\(\)]+", phone.strip()):
        return "Phone must contain only digits and +, -, (, ), spaces."
    return None  # all good




def db_search(name: str):
    """Return all contacts whose name contains the search term (case-insensitive)."""
    cursor.execute(
        "SELECT id, name, phone, email FROM CONTACTS WHERE name LIKE ?",
        (f"%{name}%",),
    )
    return cursor.fetchall()


def db_get_all():
    """Return every contact ordered by name."""
    cursor.execute("SELECT id, name, phone, email FROM CONTACTS ORDER BY name")
    return cursor.fetchall()


def db_insert(name: str, phone: str, email: str):
    cursor.execute(
        "INSERT INTO CONTACTS (name, phone, email) VALUES (?, ?, ?)",
        (name.strip(), phone.strip(), email.strip()),
    )
    conn.commit()


def db_update(contact_id: int, name: str, phone: str, email: str):
    cursor.execute(
        "UPDATE CONTACTS SET name=?, phone=?, email=? WHERE id=?",
        (name.strip(), phone.strip(), email.strip(), contact_id),
    )
    conn.commit()


def db_delete(contact_id: int):
    cursor.execute("DELETE FROM CONTACTS WHERE id=?", (contact_id,))
    conn.commit()




def window_new_contact():
    """Open a form to add a new contact. Returns True on success."""
    layout = [
        [sg.Text("New Contact", font=("Helvetica", 14, "bold"))],
        [sg.HorizontalSeparator()],
        [sg.Text("Name  :", size=8), sg.Input(key="-NAME-")],
        [sg.Text("Phone :", size=8), sg.Input(key="-PHONE-")],
        [sg.Text("Email :", size=8), sg.Input(key="-EMAIL-")],
        [sg.Button("Save"), sg.Button("Cancel")],
    ]
    win = sg.Window("New Contact", layout, keep_on_top=True)

    while True:
        event, values = win.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            win.close()
            return False

        if event == "Save":
            err = validate_contact(values["-NAME-"], values["-PHONE-"])
            if err:
                sg.popup_error(err, title="Validation Error")
                continue  # keep the window open for correction

            db_insert(values["-NAME-"], values["-PHONE-"], values["-EMAIL-"])
            win.close()
            sg.popup("Contact added successfully!", title="Success")
            return True


def window_contact_detail(contact: tuple):
    """
    Show details for one contact with Edit and Delete options.
    contact: (id, name, phone, email)
    """
    cid, name, phone, email = contact

    layout = [
        [sg.Text("Contact Details", font=("Helvetica", 14, "bold"))],
        [sg.HorizontalSeparator()],
        [sg.Text(f"Name  : {name}")],
        [sg.Text(f"Phone : {phone}")],
        [sg.Text(f"Email : {email or '—'}")],
        [sg.HorizontalSeparator()],
        [sg.Button("Edit"), sg.Button("Delete"), sg.Button("Close")],
    ]
    win = sg.Window("Contact Details", layout, keep_on_top=True)

    while True:
        event, _ = win.read()

        if event in (sg.WIN_CLOSED, "Close"):
            win.close()
            return

        if event == "Delete":
            
            if sg.popup_yes_no(f"Delete '{name}'?", title="Confirm") == "Yes":
                db_delete(cid)
                win.close()
                sg.popup("Contact deleted.", title="Deleted")
                return

        if event == "Edit":
            win.close()
            window_edit_contact(contact)
            return




def window_edit_contact(contact: tuple):
    """
    Pre-filled edit form for an existing contact.
    contact: (id, name, phone, email)
    """
    cid, name, phone, email = contact

    layout = [
        [sg.Text("Edit Contact", font=("Helvetica", 14, "bold"))],
        [sg.HorizontalSeparator()],
        [sg.Text("Name  :", size=8), sg.Input(name,  key="-NAME-")],
        [sg.Text("Phone :", size=8), sg.Input(phone, key="-PHONE-")],
        [sg.Text("Email :", size=8), sg.Input(email or "", key="-EMAIL-")],
        [sg.Button("Save"), sg.Button("Cancel")],
    ]
    win = sg.Window("Edit Contact", layout, keep_on_top=True)

    while True:
        event, values = win.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            win.close()
            return

        if event == "Save":
            err = validate_contact(values["-NAME-"], values["-PHONE-"])
            if err:
                sg.popup_error(err, title="Validation Error")
                continue

            db_update(cid, values["-NAME-"], values["-PHONE-"], values["-EMAIL-"])
            win.close()
            sg.popup("Contact updated successfully!", title="Success")
            return



def window_all_contacts():
    """Show a table of all contacts; double-click a row to view details."""
    rows = db_get_all()

    if not rows:
        sg.popup("No contacts in the database yet.", title="All Contacts")
        return

    # Table expects list-of-lists (not tuples), strip the id for display
    table_data = [[r[1], r[2], r[3] or ""] for r in rows]

    layout = [
        [sg.Text("All Contacts", font=("Helvetica", 14, "bold"))],
        [
            sg.Table(
                values=table_data,
                headings=["Name", "Phone", "Email"],
                auto_size_columns=True,
                display_row_numbers=False,
                justification="left",
                num_rows=min(15, len(table_data)),
                key="-TABLE-",
                enable_events=True,
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            )
        ],
        [sg.Button("Open Selected"), sg.Button("Close")],
    ]
    win = sg.Window("All Contacts", layout, keep_on_top=True)

    while True:
        event, values = win.read()

        if event in (sg.WIN_CLOSED, "Close"):
            win.close()
            return

        if event == "Open Selected":
            selected = values["-TABLE-"]
            if not selected:
                sg.popup("Please select a contact first.")
                continue
            idx = selected[0]           # row index in table_data
            win.close()
            window_contact_detail(rows[idx])  # pass full row with id
            return


# Main window 

def main():
    layout = [
        [sg.Text("📒 PhoneBook", font=("Helvetica", 18, "bold"), pad=(10, 10))],
        [sg.HorizontalSeparator()],
        [
            sg.Input(key="-SEARCH-", size=28, tooltip="Type a name to search"),
            sg.Button("Search", bind_return_key=True),
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("New Contact", size=14), sg.Button("All Contacts", size=14)],
        [sg.Button("Exit", size=14)],
    ]

    window = sg.Window("PhoneBook", layout, finalize=True)

    
    while True:
        event, values = window.read()

        
        if event in (sg.WIN_CLOSED, "Exit"):
            break

    
        elif event == "Search":
            search_term = values["-SEARCH-"].strip()
            if not search_term:
                sg.popup("Please enter a name to search.", title="Search")
                continue

            results = db_search(search_term)

            if not results:
                sg.popup(f"No contacts found for '{search_term}'.", title="Not Found")
                continue

            if len(results) == 1:
                # Only one match — open detail directly
                window_contact_detail(results[0])
            else:
                # Multiple matches — let user pick from a table
                table_data = [[r[1], r[2], r[3] or ""] for r in results]
                pick_layout = [
                    [sg.Text(f"{len(results)} contacts found:")],
                    [
                        sg.Table(
                            values=table_data,
                            headings=["Name", "Phone", "Email"],
                            auto_size_columns=True,
                            num_rows=min(10, len(table_data)),
                            key="-PICK-",
                            enable_events=True,
                            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        )
                    ],
                    [sg.Button("Open Selected"), sg.Button("Cancel")],
                ]
                pick_win = sg.Window("Search Results", pick_layout, keep_on_top=True)
                while True:
                    pe, pv = pick_win.read()
                    if pe in (sg.WIN_CLOSED, "Cancel"):
                        pick_win.close()
                        break
                    if pe == "Open Selected":
                        sel = pv["-PICK-"]
                        if not sel:
                            sg.popup("Select a row first.")
                            continue
                        pick_win.close()
                        window_contact_detail(results[sel[0]])
                        break

        
        elif event == "New Contact":
            window_new_contact()

        
        elif event == "All Contacts":
            window_all_contacts()

    window.close()
    conn.close()


if __name__ == "__main__":
    main()
