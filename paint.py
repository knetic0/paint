from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog

import numpy as np
import pyautogui
import cv2

root = Tk()
root.geometry("1920x1080")
root.title("Paint")

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
MAIN_COLOR = 'white'

IMG_WIDTH = WINDOW_WIDTH / 2
IMG_HEIGHT = WINDOW_HEIGHT / 2

canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=MAIN_COLOR)
canvas.place(x=0, y=0)

mainLine = canvas.create_line(0, 150, 1920, 150, width=2, fill='gray')
chooseShapes = Label(root, text="Choose Event", font="Ubuntu, 20", bg='white')
chooseShapes.place(x=0, y=5)


class Menu:
    def __init__(self):

        self.imgCoord = []
        self.im = None
        self.myCanvasPhoto = None
        self.sizeScaleErase = None

        root.bind("<B1-Motion>", lambda event: Menu.motion(self, event))
        root.bind("<ButtonPress-1>", lambda event: Menu.motion(self, event))

        self.PHOTO_IMAGE = None
        self.FOLDER_NAME = None
        self.corList = []
        self.deleteButtonText = None
        self.allTextButton = []
        self.allText = []
        self.text = None
        self.y2 = None
        self.x2 = None
        self.eraseOval = None
        self.eraseMotion = None
        self.y1 = None
        self.x1 = None
        self.eraseButton = None
        self.gui = None
        self.sizeScale = None
        self.allTriangle = None
        self.releaseButton = None
        self.holdButton = None
        self.allOval = None
        self.allLine = None
        self.allRect = None
        self.choose = None
        self.allShapes = []
        self.x, self.y = 0, 0
        self.USER_CHOOSE = str()
        self.sizeScaleSubmit = 25
        self.CHOOSE_COLOR = ['', 'black']

        self.OVAL_BUTTON = ttk.Button(root, text="Oval", command=lambda: Menu.paint(self, "oval"))
        self.OVAL_BUTTON.place(x=25, y=50)

        self.LINE_BUTTON = ttk.Button(root, text="Line", command=lambda: Menu.paint(self, "line"))
        self.LINE_BUTTON.place(x=25, y=100)

        self.RECTANGLE_BUTTON = ttk.Button(root, text="Rectangle", command=lambda: Menu.paint(self, "rectangle"))
        self.RECTANGLE_BUTTON.place(x=120, y=50)

        self.POLYGON_BUTTON = ttk.Button(root, text="Triangle", command=lambda: Menu.paint(self, "triangle"))
        self.POLYGON_BUTTON.place(x=120, y=100)

        self.COLOR_BUTTON = ttk.Button(root, text="Choose Color", command=lambda: Menu.colorChoose(self))
        self.COLOR_BUTTON.place(x=360, y=50)

        self.SIZE = ttk.Button(root, text="Size", command=lambda: Menu.size(self))
        self.SIZE.place(x=360, y=100)

        self.CLEAR_BUTTON = ttk.Button(root, text="Clear", command=lambda: Menu.clear(self))
        self.CLEAR_BUTTON.place(x=1800, y=35)

        self.ERASE_BUTTON = ttk.Button(root, text="Erase", command=lambda: Menu.erase(self))
        self.ERASE_BUTTON.place(x=1800, y=70)

        self.TEXT_BUTTON = ttk.Button(root, text="Textarea", command=lambda: Menu.createText(self))
        self.TEXT_BUTTON.place(x=240, y=50)

        self.IMAGE_BUTTON = ttk.Button(root, text="Choose Image", command=lambda: Menu.image(self))
        self.IMAGE_BUTTON.place(x=240, y=100)

        self.sizeScaleErase = Scale(root, from_=25, to=150, showvalue=True, bg="white", orient=HORIZONTAL)
        self.sizeScaleErase.place(x=1520, y=60, width=250)

        self.SAVE_BUTTON = ttk.Button(root, text="Save File", command=lambda: Menu.saveFile(self))
        self.SAVE_BUTTON.place(x=480, y=50)

    def paint(self, choose):
        self.choose = choose
        root.bind("<B1-Motion>", lambda event: Menu.motion(self, event))
        root.bind("<ButtonPress-1>", lambda event: Menu.motion(self, event))

    def motion(self, event):
        self.holdButton = True
        self.x, self.y = event.x, event.y
        print(self.x, self.y)

        while self.holdButton:
            if self.x > 0 and self.y > 150:
                if self.choose == "oval":
                    self.allOval = canvas.create_oval(self.x, self.y, (self.x + self.sizeScaleSubmit),
                                                      (self.y + self.sizeScaleSubmit),
                                                      fill=self.CHOOSE_COLOR[1], outline=self.CHOOSE_COLOR[1])
                    self.USER_CHOOSE = "oval"
                    self.allShapes.append(self.allOval)

                elif self.choose == "line":
                    self.allLine = canvas.create_line(self.x, self.y, (self.x + 50), self.y,
                                                      fill=self.CHOOSE_COLOR[1])
                    self.USER_CHOOSE = "line"
                    self.allShapes.append(self.allLine)

                elif self.choose == "rectangle":
                    self.allRect = canvas.create_rectangle(self.x, self.y, (self.x + 50), (self.y + 50),
                                                           fill=self.CHOOSE_COLOR[1])
                    self.USER_CHOOSE = "rectangle"
                    self.allShapes.append(self.allRect)

                elif self.choose == "triangle":
                    self.allTriangle = canvas.create_polygon(self.x, self.y, (self.x - 50), (self.y + 50),
                                                             (self.x + 100), (self.y + 50), fill=self.CHOOSE_COLOR[1])
                    self.USER_CHOOSE = "triangle"
                    self.allShapes.append(self.allTriangle)

            self.releaseButton = root.bind("<ButtonRelease-1>", Menu.releaseButton(self))

    def clear(self):
        for i in range(len(self.allShapes)):
            canvas.delete(self.allShapes[i])

    def releaseButton(self):
        self.holdButton = False
        self.eraseButton = False

    def colorChoose(self):
        self.CHOOSE_COLOR = colorchooser.askcolor()

    def size(self):
        self.gui = Tk()
        self.gui.geometry("420x420")
        self.gui.title("Size")
        self.sizeScale = Scale(self.gui, from_=25, to=150, showvalue=True)
        self.sizeScale.place(x=50, y=0, height=400)
        submitButton = ttk.Button(self.gui, text="Submit", command=lambda: Menu.submit(self))
        submitButton.place(x=150, y=200)

    def submit(self):
        self.sizeScaleSubmit = self.sizeScale.get()
        self.gui.destroy()

    def erase(self):
        root.bind("<B1-Motion>", lambda event: Menu.eraseMotion(self, event))
        root.bind("<ButtonPress-1>", lambda event: Menu.eraseMotion(self, event))

    def eraseMotion(self, event):
        self.eraseButton = True
        self.x1, self.y1 = event.x, event.y
        while self.eraseButton:
            if self.x1 > 0 and self.y1 > 150:
                self.eraseOval = canvas.create_oval(self.x1, self.y1, (self.x1 + self.sizeScaleErase.get()),
                                                    (self.y1 + self.sizeScaleErase.get()),
                                                    fill="white", outline="white")

            self.releaseButton = root.bind("<ButtonRelease-1>", Menu.releaseButton(self))

    def createText(self):
        root.bind("<ButtonPress-1>", lambda event: Menu.textArea(self, event))

    def textArea(self, event):
        self.x2, self.y2 = event.x, event.y
        print(self.x2, self.y2)
        if self.x2 > 0 and self.y2 > 150:
            self.text = Text(root)
            self.text.place(x=self.x2, y=self.y2, width=100, height=100)
            self.deleteButtonText = ttk.Button(root, text="X", width=1, command=lambda: deleteText(self.x2, self.y2))
            self.deleteButtonText.place(x=(self.x2 + 100), y=self.y2)
            self.corList.append(self.x2 + 100)
            self.corList.append(self.y2)
            self.allText.append(self.text)
            self.allTextButton.append(self.deleteButtonText)

            def deleteText(corx, cory):
                for i in range(len(self.allText)):
                    if abs(self.corList[i] - corx) < 1920 and abs(self.corList[i + 1] - cory) < 1080:
                        index = len(self.allText) - (i + 1)
                        self.allText[index].destroy()
                        self.allTextButton[index].destroy()
                        self.corList.pop(index)
                        self.corList.pop(index)
                        self.allText.pop(index)
                        self.allTextButton.pop(index)
                        break

    def image(self):
        self.FOLDER_NAME = filedialog.askopenfilename()
        self.PHOTO_IMAGE = PhotoImage(file=self.FOLDER_NAME)
        if len(self.FOLDER_NAME) > 1:
            self.myCanvasPhoto = canvas.create_image(250, 250, anchor=NW, image=self.PHOTO_IMAGE)
            self.imgCoord = canvas.coords(self.myCanvasPhoto)
            print(self.imgCoord)

            def left(event):
                self.imgCoord = canvas.coords(self.myCanvasPhoto)
                if self.imgCoord[0] > -10:
                    x = -20
                    y = 0
                    canvas.move(self.myCanvasPhoto, x, y)

            def right(event):
                self.imgCoord = canvas.coords(self.myCanvasPhoto)
                if self.imgCoord[0] < 1130:
                    x = 20
                    y = 0
                    canvas.move(self.myCanvasPhoto, x, y)

            def up(event):
                self.imgCoord = canvas.coords(self.myCanvasPhoto)
                if self.imgCoord[1] > 110:
                    x = 0
                    y = -20
                    canvas.move(self.myCanvasPhoto, x, y)

            def down(event):
                self.imgCoord = canvas.coords(self.myCanvasPhoto)
                if self.imgCoord[1] < 380:
                    x = 0
                    y = 20
                    canvas.move(self.myCanvasPhoto, x, y)

            root.bind("<Left>", lambda event: left(event))
            root.bind("<Right>", lambda event: right(event))
            root.bind("<Up>", lambda event: up(event))
            root.bind("<Down>", lambda event: down(event))

    def saveFile(self):
        self.im = pyautogui.screenshot(region=(0, 185, 1920, 1080))
        self.im = cv2.cvtColor(np.array(self.im), cv2.COLOR_RGB2BGR)
        cv2.imwrite("file.png", self.im)


Menu()
root.mainloop()
