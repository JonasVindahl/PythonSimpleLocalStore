import tkinter as tk
from collections import Counter
from varer import get_varer,fjern_vare,tilføj_vare,på_lager
import yaml
from pathlib import Path

Kurv = []
#Åbner start butiksvinduet
def open_shop_window():
    global Kurv
    Kurv = get_kurv()
    shop_window = tk.Tk()
    shop_window.title("Shop")
    tk.Label(shop_window, text="Shop").pack()
    tk.Button(shop_window, text="Varer", command=open_varer_window).pack()
    tk.Button(shop_window, text="Kurv", command=open_kurv_window).pack()
    shop_window.mainloop()

#Gemmer kurven i en yaml fil
def save_kurv():
    from menu import bruger
    yaml_file = Path("kurve.yml")
#Hent eksisterende kurve
    kurve = get_kurve()  
    for kurv in kurve:
        #Hvis brugeren allerede har en kurv, opdateres den
        if kurv["kunde"] == bruger:
            kurv["kurv"] = Kurv
            break
    #Hvis brugeren ikke har en kurv, oprettes en ny
    else:
        kurve.append({"kunde": bruger, "kurv": Kurv})

    with yaml_file.open('w',encoding='utf-8') as file:
        yaml.safe_dump(kurve, file)
#Tilføj en vare til kurven
def tilføj_til_kurv(vare):
    global Kurv
    if på_lager(vare):
        Kurv.append(vare)
        fjern_vare(vare)
        save_kurv()
        print(Kurv)
    #Opdaterer vinduet med varer
        update_varer_window()  
    else:
        print("Varen er udsolgt")
#Fjern en vare fra kurven
def open_varer_window():
    global varer_window
    varer_window = tk.Toplevel()
    varer_window.title("Varer")
    #Opretter et label til varer
    tk.Label(varer_window, text="Varer").pack()
    
    varer = get_varer()
    
    #Sorterer varerne alfabetisk baseret på navn
    varer = sorted(varer, key=lambda x: x['navn'].lower())
    
#Opretter en ramme (frame) til hver vare
    for vare in varer:
        frame = tk.Frame(varer_window)
        frame.pack(pady=5, fill=tk.X)
#Opretter et label til hver vare
        vare_info = f"{vare['navn']} - {vare['pris']} kr. - {vare['lager']} på lager - {vare['rabat']}% rabat"
        tk.Label(frame, text=vare_info).pack(side=tk.LEFT, padx=10)
#Opretter en knap til at tilføje varen til kurven
        add_button = tk.Button(frame, text="Tilføj til Kurv", command=lambda v=vare['navn']: tilføj_til_kurv(v))
        add_button.pack(side=tk.RIGHT)

    tk.Button(varer_window, text="Tilbage", command=varer_window.destroy).pack()
#Opdaterer vinduet med varer
def update_varer_window():
    varer = get_varer()
    
    # Sorterer varerne alfabetisk baseret på navn
    varer = sorted(varer, key=lambda x: x['navn'].lower())
    
#Rydder eksisterende widgets i varervinduet for at opdatere det med nye oplysninger
    for widget in varer_window.winfo_children():
        widget.destroy()
    tk.Label(varer_window, text="Varer").pack()
#Opretter en ramme (frame) til hver vare
    for vare in varer:
        frame = tk.Frame(varer_window)
        frame.pack(pady=5, fill=tk.X)
        vare_info = f"{vare['navn']} - {vare['pris']} kr. - {vare['lager']} på lager - {vare['rabat']}% rabat"
        tk.Label(frame, text=vare_info).pack(side=tk.LEFT, padx=10)

        add_button = tk.Button(frame, text="Tilføj til Kurv", command=lambda v=vare['navn']: tilføj_til_kurv(v))
        add_button.pack(side=tk.RIGHT)

    tk.Button(varer_window, text="Tilbage", command=varer_window.destroy).pack()

#Henter kurven fra en yaml fil
def get_kurve():
    yaml_file = Path("kurve.yml")
    if not yaml_file.exists():
        #Hvis filen ikke findes, returneres en tom liste
        return []
    with yaml_file.open('r',encoding='utf-8') as file:
        try:
            kurve = yaml.safe_load(file)
            if kurve is None:
                #Hvis filen er tom, returneres en tom liste
                return []
            if not isinstance(kurve, list):
                raise ValueError("Data i 'kurve.yml' skal være en liste af dictionaries.")
            #Returnerer listen af kurve
            return kurve
        #Håndterer fejl ved indlæsning af yaml
        except yaml.YAMLError as e:
            print(f"Fejl ved indlæsning af YAML: {e}")
            return []
        #Håndterer fejl ved indlæsning af data
        except ValueError as e:
            print(f"Fejl: {e}")
            return []
#Henter kurven for brugeren
def get_kurv():
    from menu import bruger
    #Henter alle kurve og finder den korrekte kurv for brugeren
    kurve = get_kurve()
    for kurv in kurve:
        if kurv["kunde"] == bruger:
            return kurv["kurv"]
    return []

#Fjern en af en vare fra kurven
def fjern_en_vare(vare, frame, item_counts, kurv_window):
    global Kurv
    if vare in Kurv:
        Kurv.remove(vare)

        item_counts[vare] -= 1
        if item_counts[vare] == 0:
            # Fjern vare helt fra kurven, hvis antallet er 0
            frame.destroy()
            del item_counts[vare]

        #hvis kurven er tom, skifter titlen til "Tom Kurv"
        if not Kurv:
            kurv_window.title("Tom Kurv")
            for widget in kurv_window.winfo_children():
                widget.destroy()
            tk.Label(kurv_window, text="Kurven er tom.").pack()
            return

        opdater_kurv(kurv_window)
    tilføj_vare(vare)
    save_kurv()
    print("Kurv:", Kurv)
#Opdaterer kurven
def opdater_kurv(kurv_window):
    # Tæller antallet af hver vare i kurven
    item_counts = Counter(Kurv)
    
    # Beregner den samlede pris
    pris = 0
    for item, count in item_counts.items():
        for vare in get_varer():
            if item == vare["navn"]:
                pris += vare["pris"] * (1 - vare["rabat"] / 100) * count
    
    # Rydder eksisterende widgets i kurvvinduet for at opdatere det med nye oplysninger
    for widget in kurv_window.winfo_children():
        widget.destroy()
    
    # Opdaterer eller tilføjer vareoplysninger og pris
    if not Kurv:
        tk.Label(kurv_window, text="Kurven er tom.").pack()
    else:
        # Sorterer kurvens indhold alfabetisk baseret på vare-navn
        sorted_items = sorted(item_counts.items(), key=lambda x: x[0].lower())
        
        for vare, count in sorted_items:
            frame = tk.Frame(kurv_window)
            frame.pack(pady=5, fill=tk.X)
            item_text = f"{vare}: {count} stk"
            tk.Label(frame, text=item_text).pack(side=tk.LEFT, padx=10)
            tk.Button(frame, text="Fjern en", command=lambda v=vare, f=frame: fjern_en_vare(v, f, item_counts, kurv_window)).pack(side=tk.RIGHT, padx=10)
    
        # Tilføj prislinjen i bunden af kurven
        tk.Label(kurv_window, text=f"Pris: {pris:.2f} kr.").pack(side=tk.LEFT, padx=10)
        tk.Button(kurv_window, text="Tilbage", command=kurv_window.destroy).pack()

    # Gemmer den opdaterede kurv
    save_kurv()

    # Debugging: Udskriver indholdet af Kurv i konsollen
    print("Kurv:", Kurv)

#Åbner vinduet til at se ens kurv
def open_kurv_window():
    kurv_window = tk.Toplevel()
    tk.Label(kurv_window, text="Kurv").pack()
#Tæller antallet af hver vare i kurven
    item_counts = Counter(Kurv)

    if not Kurv:
        kurv_window.title("Tom Kurv")
        tk.Label(kurv_window, text="Kurven er tom.").pack()
        tk.Button(kurv_window, text="Tilbage", command=kurv_window.destroy).pack()
    else:
        kurv_window.title("Kurv")
        #Sorterer kurvens indhold alfabetisk baseret på vares navn
        opdater_kurv(kurv_window)  

    print("Kurv:", Kurv)
    
if __name__ == "__main__":
    open_shop_window()
