import yaml
from pathlib import Path
from tkinter import messagebox
import tkinter as tk

#Hent varer fra fil
def get_varer():
    yaml_file = Path("varer.yml")
    if not yaml_file.exists():
        return []
    with yaml_file.open('r') as file:
        varer = yaml.safe_load(file)
    return varer

#API funktion til at tilføje en vare
def add_vare(vare):
    varer = get_varer()
    if not varer:
        varer = []
    for existing_vare in varer:
        if existing_vare["navn"] == vare["navn"]:
            return "Varenavn er i systemet"
    vare_id = len(varer) + 1
    vare["id"] = vare_id
    varer.append(vare)
    yaml_file = Path("varer.yml")
    with yaml_file.open('w', encoding='utf-8') as file:
        yaml.dump(varer, file, allow_unicode=True)
    return "Vare tilføjet"

#vinduet til at tilføje en ny vare
def open_add_vare_window():
    def submit_vare():
        #Hent data fra input felterne
        navn = navn_entry.get()
        pris = pris_entry.get()
        lager = lager_entry.get()
        rabat = rabat_entry.get()
        #Tjek om pris og rabat er tal
        if not pris.isdigit() or not rabat.isdigit():
            messagebox.showerror("Fejl", "Pris og rabat skal være tal.")
            return
        #Opret dictionary med varedata
        vare = {"navn": navn, "pris": int(pris), "lager": int(lager), "rabat": int(rabat)}
        result = add_vare(vare)
        messagebox.showinfo("Info", result)
        vare_window.destroy()
#Opretter vinduet til at tilføje en vare
    vare_window = tk.Toplevel()
    vare_window.title("Tilføj Vare")

    tk.Label(vare_window, text="Navn:").grid(row=0, column=0)
    navn_entry = tk.Entry(vare_window)
    navn_entry.grid(row=0, column=1)

    tk.Label(vare_window, text="Pris:").grid(row=1, column=0)
    pris_entry = tk.Entry(vare_window)
    pris_entry.grid(row=1, column=1)

    tk.Label(vare_window, text="Lager:").grid(row=2, column=0)
    lager_entry = tk.Entry(vare_window)
    lager_entry.grid(row=2, column=1)

    tk.Label(vare_window, text="Rabat:").grid(row=3, column=0)
    rabat_entry = tk.Entry(vare_window)
    rabat_entry.grid(row=3, column=1)

    tk.Button(vare_window, text="Tilføj Vare", command=submit_vare).grid(row=4, columnspan=2)
#Fjern en fra lageret af en vare
def fjern_vare(vare):
    varer = get_varer()
    for existing_vare in varer:
        #Hvis varen findes, fjernes en fra lageret
        if existing_vare["navn"] == vare:
            for existing_vare in varer:
                if existing_vare["navn"] == vare:
                    existing_vare['lager'] -= 1
                    yaml_file = Path("varer.yml")
                    with yaml_file.open('w', encoding='utf-8') as file:
                        yaml.safe_dump(varer, file)
                    return "Vare fjernet"
            return "Vare ikke fundet"
#Tilføj en til lageret af en vare
def tilføj_vare(vare):
    varer = get_varer()
    for existing_vare in varer:
        #Hvis varen findes, tilføjes en til lageret
        if existing_vare["navn"] == vare:
            existing_vare['lager'] += 1
            yaml_file = Path("varer.yml")
            with yaml_file.open('w', encoding='utf-8') as file:
                yaml.safe_dump(varer, file)
            return "Vare tilføjet"
    return "Vare ikke fundet"

#Tjek om en vare er på lager
def på_lager(vare):
    varer = get_varer()
    for existing_vare in varer:
        if existing_vare["navn"] == vare:
            lager = existing_vare["lager"]
            if int(existing_vare["lager"]) > 0:
                return True
            else:
                return False
    return