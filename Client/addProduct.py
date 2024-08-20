from tkinter import *
import tkinter as tk
import json

from sapi import API, ROOTURL
server = API(ROOTURL)

class AddProduct:
    def __init__(self, main, root):
        self.frames = []
        self.main = main

        self.Window = Toplevel(root)
        self.Window.title("Add Product")
        self.Window.geometry("480x460")

        mainFrame = Frame(self.Window)
        ftable = ["Title", "Details", "Price", "Subcate"]
        findex = 0

        for i in ftable:
            iFrame = Frame(mainFrame)
            iLable = Label(iFrame, text=i, width=10, anchor=W, font=('TkDefaultFont', 10))
            iLable.pack(fill=X)

            iField = Entry(iFrame, width=60, font=('TkDefaultFont', 16))
            iField.pack(fill=X)
            iFrame.pack(fill=X, pady=4)

            self.frames.append(iField)
            findex += 1
        mainFrame.pack(side=TOP, fill=BOTH, pady=20, padx=20)

        category = server.getCategory()
        CategoryOptions = []

        for j in category.json(): CategoryOptions.append(j['Title'])

        CategorySelect = StringVar(self.Window)
        CategorySelect.set(CategoryOptions[0])

        CategorySelecter = OptionMenu(self.Window, CategorySelect, *CategoryOptions)
        CategorySelecter.pack(fill=X, padx=20, pady=0)

        self.frames.append(CategorySelect)

        StockFrame = Frame(self.Window)
        for i in ["Quantity", "MinStock", "MaxStock"]:
            iFrame = Frame(StockFrame)
            iLable = Label(iFrame, text=i, anchor=W, font=('TkDefaultFont', 10))
            iLable.pack(side=TOP, fill=Y)

            iField = Entry(iFrame, width=10, font=('TkDefaultFont', 16))
            iField.pack(side=BOTTOM, fill=Y)
            iFrame.pack(side=LEFT, fill=X, pady=4) 

            self.frames.append(iField)
        StockFrame.pack(side=TOP, fill=X, padx=20, pady=6)

        MenuFrame = Frame(self.Window)

        CancelBth = Button(MenuFrame, text='Cancle',width=20, height=2, bd='1', anchor=CENTER, command=self.Window.destroy)
        CancelBth.pack(side=LEFT, fill=Y, padx=20)

        submitBtn = Button(MenuFrame, text='Confirm',width=20, height=2, bd='1', anchor=CENTER, command=self.SubmitUpload)
        submitBtn.pack(side=RIGHT, fill=Y, padx=20)

        MenuFrame.pack(side=BOTTOM, fill=Y,  pady=20, padx=20)

    def SubmitUpload(self):
        # findex = 0
        # fKey = ['Title', 'Details', 'Price', 'Subcate', 'Category']

        # jsonString = ""
        # for i in self.frames:
        #     jsonString += f'"{fKey[findex]}" : "{i.get()}"'
        #     if findex < len(fKey) -1 : jsonString += ','
        #     findex += 1

        # jsonFormat = '{' + jsonString + '}'
        # print(jsonFormat)
        # jsonLoads = json.loads(jsonFormat)

        # print(jsonLoads)

        #  ?1----
        res = server.addProduct(
        self.frames[0].get(), # Title
        self.frames[1].get(), # Details,
        # None, # Price
        self.frames[2].get(), # Price
        self.frames[4].get(), # Category
        self.frames[3].get(), # Subcate

        self.frames[5].get(), # Quantity
        self.frames[6].get(), # MinStock
        self.frames[7].get(), # MaxStock
        )

        if res.status_code == 200:
            self.Window.destroy()
            self.main.refetchTree()
            return 200
