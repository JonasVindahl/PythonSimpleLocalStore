import yaml
import hashlib
from pathlib import Path
from tkinter import messagebox
import tkinter as tk

#hash kodeordet
def hash_pass(password):
    return hashlib.md5(password.encode()).hexdigest()

#Hent kunder fra fil
def get_kunder():
    #definerer stien til filen
    yaml_file = Path("kunder.yml")
    if not yaml_file.exists():
        return []
    with yaml_file.open('r') as file:
        kunder = yaml.safe_load(file)
    return kunder

#Hent usertype for en kunde fra filen
def get_usertype(kunde):
    kunder = get_kunder()
    for existing_kunde in kunder:
        if existing_kunde["kunde"] == kunde:
            return existing_kunde["usertype"]
    return None

#function til at tilføje en kunde til filen
def add_kunde(kunde, password,user_type):
    if not user_type:
        user_type = "kunde"
    kunder = get_kunder()
    #hvis der ikke er nogle kunder, oprettes en tom liste
    if not kunder:
        kunder = []
    for existing_kunde in kunder:
        #hvis kunden allerede eksisterer, returneres en fejlbesked
        if existing_kunde["kunde"] == kunde:
            return "Kundenavn er taget"
    kunde_id = len(kunder) + 1
    kunder.append({"id": kunde_id, "kunde": kunde, "password": hash_pass(password), "usertype": user_type})
    yaml_file = Path("kunder.yml")
    #gemmer kunden i filen
    with yaml_file.open('w') as file:
        yaml.dump(kunder, file)
    return "Kunde tilføjet"

#Åbner vinduet til at tilføje en kunde
def open_add_kunde_window():
    def submit_kunde():
        username = username_entry.get()
        password = password_entry.get()
        user_type = user_type_entry.get()
#tjekker om brugernavn og password er gyldige
        if " " in username:
            messagebox.showerror("Fejl", "Brugernavn må ikke indeholde mellemrum.")
            return

        if len(password) < 8:
            messagebox.showerror("Fejl", "Adgangskoden skal være mindst 8 tegn.")
            return

        result = add_kunde(username, password, user_type)
        messagebox.showinfo("Info", result)
        kunde_window.destroy()

    kunde_window = tk.Toplevel()
    kunde_window.title("Tilføj Kunde")

    tk.Label(kunde_window, text="Brugernavn:").grid(row=0, column=0)
    username_entry = tk.Entry(kunde_window)
    username_entry.grid(row=0, column=1)

    tk.Label(kunde_window, text="Adgangskode:").grid(row=1, column=0)
    password_entry = tk.Entry(kunde_window, show="*")
    password_entry.grid(row=1, column=1)
    
    tk.Label(kunde_window, text="User Type:").grid(row=2, column=0)
    user_type_entry = tk.Entry(kunde_window)
    user_type_entry.grid(row=2, column=1)

    tk.Button(kunde_window, text="Tilføj Kunde", command=submit_kunde).grid(row=3, columnspan=2)
