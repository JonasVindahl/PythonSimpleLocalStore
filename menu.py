#masse import
import tkinter as tk
from tkinter import messagebox
from kunder import open_add_kunde_window, hash_pass, get_kunder
from butik import open_shop_window
from varer import open_add_vare_window

#Verificer at brugern eksisterer og at password er korrekt
def check_login(username, password):
    # Hash brugerens input-password for at matche det med det gemte password
    hashed_password = hash_pass(password)
    
    # Hent alle kunder
    kunder = get_kunder()
    #find brugeren i listen af kunder
    for kunde in kunder:
        if kunde["kunde"] == username and kunde["password"] == hashed_password:
            #Gem brugernavnet i en global variabel, så vi kan bruge det i andre funktioner
            global bruger
            bruger = username
            #Returner brugerens usertype (kunde eller admin)
            return kunde["usertype"]
    
    return None


#hvis brugeren er admin, åbnes admin vinduet
def open_admin_window():
    admin_window = tk.Tk()
    admin_window.title("Admin Panel")
    tk.Label(admin_window, text="Admin Panel").pack()
    tk.Button(admin_window, text="Tilføj Kunde", command=open_add_kunde_window).pack()
    tk.Button(admin_window, text="Tilføj varer", command=open_add_vare_window).pack()

#Login funktion
def login():
    username = username_entry.get()
    password = password_entry.get()
    #definerer usertype som returneres fra check_login
    usertype = check_login(username, password)
    
    if usertype is None:
        #Hvis brugernavn eller password er forkert, vises en fejlmeddelelse
        messagebox.showerror("Fejl", "Forkert brugernavn eller adgangskode.")
    else:
        messagebox.showinfo("Velkommen", f"Velkommen {username}, du er logget ind som {usertype}.")
        root.destroy()
        
        if usertype == "admin":
            open_admin_window()
            print("admin")
        else:
            open_shop_window()  
#Opretter hovedvinduet, hvor man starter
def main_window():
    global username_entry, password_entry, root

    # Opret hovedvindue for login
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Brugernavn:").grid(row=0, column=0)
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1)

    tk.Label(root, text="Adgangskode:").grid(row=1, column=0)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(root, text="Login", command=login).grid(row=2, columnspan=2)

    # Tilføj en knap til at oprette en ny bruger
    tk.Button(root, text="Add User", command=open_add_kunde_window).grid(row=3, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main_window()
