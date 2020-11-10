import tkinter as tk


class Icon:  # Creates Object from Picture without Background
    def __init__(self, master, image, posx, posy):
        self.root = master
        self.image = image
        self.offsetx = 0
        self.offsety = 0
        self.logo = tk.PhotoImage(file=self.image)
        self.ID = self.root.create_image(posx, posy, anchor="nw",
                                         image=self.logo)

    def update(self, offsetx=0, offsety=0):
        differenzx = offsetx - self.offsetx
        differenzy = offsety - self.offsety
        self.offsetx = self.offsetx + differenzx
        self.offsety = self.offsety + differenzy
        self.root.move(self.ID, differenzx, differenzy)


class Led:  # LED with color, color changes by String
    def __init__(self, master, posx, posy, diameter, framewidth,
                 framecolor, ledcolor):
        self.root = master
        self.ledcolor = ledcolor
        self.framecolor = framecolor
        self.diameter = diameter
        self.framewidth = framewidth
        self.offsetx = 0
        self.offsety = 0
        self.led = self.root.create_oval(
            posx, posy, posx + self.diameter, posy + self.diameter,
            width=self.framewidth, fill=self.ledcolor, outline=self.framecolor)

    def update(self, offsetx=0, offsety=0):
        differenzx = offsetx - self.offsetx
        differenzy = offsety - self.offsety
        self.offsetx = self.offsetx + differenzx
        self.offsety = self.offsety + differenzy
        self.root.move(self.led, differenzx, differenzy)

    def colorchange(self, ledcolor="yellow", framecolor="black"):
        self.ledcolor = ledcolor
        self.framecolor = framecolor
        self.root.itemconfig(self.led,
                             fill=self.ledcolor,
                             outline=self.framecolor)