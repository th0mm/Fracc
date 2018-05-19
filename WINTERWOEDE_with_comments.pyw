from tkinter import *

window = Tk()
window.title("OwO")
window.geometry('220x30')

lbl = Label(window, text="Distance:")
lbl.grid(column=0, row=0)

txt = Entry(window, width=14)
txt.grid(column=2, row=0)

def legalAnswer(s):
    try:
        s = float(s)
        if(s > 0.0 and s < 1.0):
            return True
    except ValueError:
        return False

def clicked():
    if legalAnswer(txt.get()):
        REQUIEM = open("TEXT\\requiem.txt", "w")
        REQUIEM.write(txt.get())
        REQUIEM.close()
        window.destroy()
    else:
        txt.delete(0,END)
        txt.insert(0, "ERROR: fill in a number between 0 and 1")

btn = Button(window, text="OK MASTER", command=clicked)
btn.grid(column=3, row=0)

window.mainloop()
