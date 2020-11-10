import tkinter as tk
from tkinter import ttk
windowframe = tk.Tk()
tree = ttk.Treeview(windowframe)

tree["columns"]=("Datentyp","Kommentar")

tree.column("#0", width=100, minwidth=100, stretch=tk.NO)
tree.column("Datentyp", width=100, minwidth=100, stretch=tk.NO)
tree.column("Kommentar", width=100, minwidth=100, stretch=tk.NO)

tree.heading("#0", text="Name",anchor=tk.W)
tree.heading("Datentyp", text="Datentyp",anchor=tk.W)
tree.heading("Kommentar", text="Kommentar",anchor=tk.W)

# Level 1
V1 = tree.insert("",index=0, text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
V2 = tree.insert("",index=1, text="Folder 2", values=("23-Jun-17 11:05","File folder",""))

# Level 2
tree.insert(V1, "end", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
for x in range(0,100):
    tree.insert(V1, "end", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))


vsb = ttk.Scrollbar(windowframe, orient="vertical", command=tree.yview)
vsb.place(x=30+200+2, y=95, height=200+20)

vsb1 = ttk.Scrollbar(windowframe, orient="horizontal", command=tree.xview)
vsb1.place(x=60+100, y=150, width=200+20)

tree.configure(yscrollcommand=vsb.set)
tree.configure(xscrollcommand=vsb1.set)

tree.place(x=0, y=0)
