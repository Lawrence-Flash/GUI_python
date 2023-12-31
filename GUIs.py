import tkinter as tk
from tkinter import ttk

parent = tk.Tk()

tvar = tk.StringVar()
def swaptext():
    if tvar.get() == 'HI':
        tvar.set('there')
    else:
        tvar.set('Hi')
        
my_button = ttk.Button(parent, textvariable=tvar, command=swaptext)
my_button.pack()
parent.mainloop()