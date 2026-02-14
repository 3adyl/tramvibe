from dane import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *

def utworz_okno():
    root = tk.Tk()
    root.state("zoomed")
    root.attributes("-fullscreen", True)
    # root.wm_attributes("-zoomed", True)
    root.title("Tablica Odjazdów")
    root.geometry("600x400")



    pr = StringVar()
    # name = ttk.Entry(root, textvariable=pr)
    # name.pack()
    # button = ttk.Button(root, text='Okay')
    # button.pack(side=tk.TOP)

    pr = 'Dw. Centralny 02'
    r = requests.get(
        f"https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey={config['API_KEY']}")
    szukany = Przystanek(pr, r)
    dane_rozkladu = szukany.rozklad_wyswietlacz_now()


    kolumny = ('linia', 'kierunek', 'czas')

    style = ttk.Style(root)
    style.configure('Emergency.TButton', font='helvetica 70 bold', foreground='orange', padding=10, rowheight=120, background="black")

    tabela = ttk.Treeview(root, columns=kolumny, show='', selectmode='none', style="Emergency.TButton")


    # style.configure("Treeview.Column", background="PowderBlue", font=(None, 100))

    tabela.heading('linia', text='Linia')
    tabela.heading('kierunek', text='Kierunek')
    tabela.heading('czas', text='Czas odjazdu')

    tabela.column('linia', width=200, anchor='center')
    tabela.column('kierunek', width=1200, anchor='w')
    tabela.column('czas', width=400, anchor='center')

    for wiersz in dane_rozkladu[:9]:
        tabela.insert('', 'end', values=wiersz)

    # scrollbar = ttk.Scrollbar(root, command=tabela.yview)
    # tabela.configure(yscroll=scrollbar.set)
    # scrollbar.pack(side='right', fill=tk.Y)

    tabela.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    utworz_okno()