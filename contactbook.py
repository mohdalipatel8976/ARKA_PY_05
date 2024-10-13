import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

contacts = {}

def save_contacts_to_file():
    with open("contacts.txt", "w") as f:
        for name, details in contacts.items():
            f.write(f"{name},{details['phone']},{details['email']},{details['address']}\n")

def load_contacts_from_file():
    try:
        with open("contacts.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                name = parts[0]
                phone = parts[1]
                email = parts[2]
                address = ",".join(parts[3:])
                contacts[name] = {'phone': phone, 'email': email, 'address': address}
    except FileNotFoundError:
        pass


def display_contacts(show_empty_message=True):
    contact_list.delete(*contact_list.get_children())
    if contacts:
        for name, details in contacts.items():
            contact_list.insert("", "end", values=(name, details['phone'], details['email'], details['address']))
    elif show_empty_message:
        messagebox.showinfo("Info", "Contact book is empty.")

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if name and phone:
        contacts[name] = {'phone': phone, 'email': email, 'address': address}
        display_contacts(show_empty_message=False)  
        clear_entries()
        save_contacts_to_file()
    else:
        messagebox.showwarning("Input Error", "Name and Phone number are required.")

def search_contact():
    search_name = search_entry.get() 
    if search_name in contacts:
        details = contacts[search_name]
        messagebox.showinfo("Search Result", f"Name: {search_name}\nPhone: {details['phone']}\nEmail: {details['email']}\nAddress: {details['address']}")
    else:
        messagebox.showwarning("Not Found", "Contact not found.")

def update_contact():
    edit_name = simpledialog.askstring("Update Contact", "Enter the contact name to edit:")
    if edit_name in contacts:
        new_phone = simpledialog.askstring("Update Phone", "Enter new phone number:")
        new_email = simpledialog.askstring("Update Email", "Enter new email:")
        new_address = simpledialog.askstring("Update Address", "Enter new address:")
        contacts[edit_name] = {'phone': new_phone, 'email': new_email, 'address': new_address}
        display_contacts()
        save_contacts_to_file()
    else:
        messagebox.showwarning("Not Found", "Contact not found.")

def delete_contact():
    del_name = simpledialog.askstring("Delete Contact", "Enter the contact name to delete:")
    if del_name in contacts:
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {del_name}?")
        if confirm:
            del contacts[del_name]
            display_contacts()
            save_contacts_to_file()
    else:
        messagebox.showwarning("Not Found", "Contact not found.")

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

root = tk.Tk()
root.title("ARKA Contact Book")
root.geometry("800x600")
root.configure(bg="#f7f7f7")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 12), background="#f7f7f7")
style.configure("Treeview", font=("Arial", 12), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

frame = ttk.Frame(root, padding=(20, 20))
frame.grid(row=0, column=0, sticky="nsew")

ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
name_entry = ttk.Entry(frame)
name_entry.grid(row=0, column=1)

ttk.Label(frame, text="Phone:").grid(row=1, column=0, sticky=tk.W)
phone_entry = ttk.Entry(frame)
phone_entry.grid(row=1, column=1)

ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky=tk.W)
email_entry = ttk.Entry(frame)
email_entry.grid(row=2, column=1)

ttk.Label(frame, text="Address:").grid(row=3, column=0, sticky=tk.W)
address_entry = ttk.Entry(frame)
address_entry.grid(row=3, column=1)

button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0)

ttk.Button(button_frame, text="Add Contact", command=add_contact).grid(row=0, column=0)
ttk.Button(button_frame, text="Search", command=search_contact).grid(row=0, column=1)
ttk.Button(button_frame, text="Update Contact", command=update_contact).grid(row=0, column=2)
ttk.Button(button_frame, text="Delete Contact", command=delete_contact).grid(row=0, column=3)

# Moved the search entry field to a separate row
ttk.Label(frame, text="Search:").grid(row=4, column=0, sticky=tk.W)
search_entry = ttk.Entry(frame)  
search_entry.grid(row=4, column=1)

contact_list = ttk.Treeview(root, columns=("Name", "Phone", "Email", "Address"), show="headings")
contact_list.heading("Name", text="Name")
contact_list.heading("Phone", text="Phone")
contact_list.heading("Email", text="Email")
contact_list.heading("Address", text="Address")
contact_list.grid(row=2, column=0, padx=(20), pady=(10), sticky="nsew")

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=contact_list.yview)
contact_list.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=2, column=1, sticky="ns")

root.grid_rowconfigure(2, weight=1)  
root.grid_columnconfigure(0, weight=1)  

name_entry.focus()

load_contacts_from_file()
display_contacts(show_empty_message=False) 
root.mainloop()
