from tkinter import *
from tkinter import ttk


fenetre = Tk()

pizza = PhotoImage(file="pizza_time.png")
canvas = Canvas(fenetre,width = 1920,height = 1080)
canvas.create_image(0,0,anchor = NW,image = pizza)
canvas.pack()

fenetre.mainloop()
