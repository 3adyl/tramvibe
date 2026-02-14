from dane import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
import threading
import time


def utworz_okno():

    def toggle_fullscreen(event=None):
        is_fullscreen = root.attributes('-fullscreen')
        root.attributes('-fullscreen', not is_fullscreen)

    def aktualizuj(nowe_dane):
        for item in tabela.get_children():
            tabela.delete(item)
        for wiersz in nowe_dane[:8]:
            tabela.insert('', 'end', values=wiersz)

    def dane():
        while True:
            szukany = Przystanek(pr, r)
            dane_rozkladu = szukany.rozklad_wyswietlacz_now()
            czas.set(f"github.com/3adyl/tramvibe\t\t\tŹródło danych: Miasto Stołeczne Warszawa (http://api.um.warszawa.pl). Data pozyskania informacji publicznej: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            del szukany
            root.after(0, aktualizuj, dane_rozkladu)
            time.sleep(30)


    root = tk.Tk()
    root.state("zoomed")
    root.bind("<F11>", toggle_fullscreen)
    root.iconbitmap(default='tramvibe.ico')
    root.title("Tramvibe")
    root.configure(background='black')

    wysokosc = int((root.winfo_screenheight()-36)/9)
    czas = StringVar()

    pr = 'Dw. Centralny 01'
    r = requests.get(
        f"https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey={config['API_KEY']}")

    style = ttk.Style(root)
    style.configure('Emergency.TButton', font='helvetica 70', foreground='orange', padding=10, rowheight=wysokosc,
                    background="black")

    container = tk.Frame(root, height=wysokosc, background="black")
    container.pack_propagate(False)
    container.pack(fill='both', expand=True)
    name = Label(container, text=pr, font='helvetica 70 bold', anchor='center', foreground='orange', background="black")
    name.pack(fill='both', expand=True)

    kolumny = ('linia', 'kierunek', 'czas')

    container3 = tk.Frame(root, height=8*wysokosc, background="black")
    container3.pack_propagate(False)
    container3.pack(fill='both', expand=True)
    tabela = ttk.Treeview(container3, columns=kolumny, show='', selectmode='none', style="Emergency.TButton")

    tabela.heading('linia', text='Linia')
    tabela.heading('kierunek', text='Kierunek')
    tabela.heading('czas', text='Czas odjazdu')

    tabela.column('linia', width=250, anchor='center')
    tabela.column('kierunek', width=1150, anchor='w')
    tabela.column('czas', width=400, anchor='center')
    tabela.pack(fill='both', expand=True)

    for i in range(8):
        tabela.insert('', 'end', values= ('','',''))

    container2 = tk.Frame(root, height=36, background="black")
    container2.pack_propagate(False)
    container2.pack(fill='both', expand=True)
    stopka = Label(container2, textvariable=czas, font='helvetica 16', anchor='center', foreground='orange',
                   background="black")
    stopka.pack(fill='both', expand=True)

    watek = threading.Thread(target=dane, daemon=True)
    watek.start()
    root.mainloop()


if __name__ == "__main__":
    utworz_okno()
