from tkinter import *
from tkinter import ttk
import time
from threading import Thread

wire = []

def burn():
    print("burn")
    time.sleep(1)
    #random change here 
    for w in wire:
        w.config(text="Burning")
        time.sleep(2)

    for w in wire:
        w.config(text="Done")
        time.sleep(2)


root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()

for i in range(1,8):
    name = "Wire #{}".format(i)
    w = ttk.Button(frame, text=name)
    w.grid(column=0, row=i)
    wire.append(w)

thread = Thread(target=burn)
thread.start()

root.mainloop()                
# never returns
