from tkinter import *
from tkinter.messagebox import askyesno
import tkinter as tk
import json

from sapi import API, ROOTURL
server = API(ROOTURL)

class EditProduct:
    def __init__(self, main, root, _id):
        self.frames = []
        self._id = _id
        self.main = main

        res = server.getProduct(_id)
        product = res.json()

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

            entryText = StringVar()
            iField = Entry(iFrame, width=60, font=('TkDefaultFont', 16), textvariable=entryText)
            entryText.set(product[i])

            iField.pack(fill=X)
            iFrame.pack(fill=X, pady=4)

            self.frames.append(iField)
            findex += 1

        mainFrame.pack(side=TOP, fill=BOTH, pady=20, padx=20)

        category = server.getCategory()
        CategoryOptions = []

        for j in category.json(): CategoryOptions.append(j['Title'])

        CategorySelect = StringVar(self.Window)
        CategorySelect.set(self.main.searchCategory(product['Category']))

        CategorySelecter = OptionMenu(self.Window, CategorySelect, *CategoryOptions)
        CategorySelecter.pack(fill=X, padx=20, pady=0)

        self.frames.append(CategorySelect)

        StockFrame = Frame(self.Window)
        for i in ["Quantity", "MinStock", "MaxStock"]:
            iFrame = Frame(StockFrame)
            iLable = Label(iFrame, text=i, anchor=W, font=('TkDefaultFont', 10))
            iLable.pack(side=TOP, fill=Y)

            entryText = StringVar()
            iField = Entry(iFrame, width=10, font=('TkDefaultFont', 16), textvariable=entryText)
            entryText.set(product[i])

            iField.pack(side=TOP, fill=Y)
            iFrame.pack(side=LEFT, fill=X, pady=4) 
            
            self.frames.append(iField)
        StockFrame.pack(side=TOP, fill=X, padx=20, pady=6)

        MenuFrame = Frame(self.Window)

        removeBth = Button(MenuFrame, text='Remove',width=14, height=2, bd='1', anchor=CENTER, command=self.removeProduct)
        removeBth.pack(side=LEFT, fill=Y, padx=20)

        cancelBth = Button(MenuFrame, text='Cancle',width=14, height=2, bd='1', anchor=CENTER, command=self.Window.destroy)
        cancelBth.pack(side=LEFT, fill=Y, padx=20)

        submitBtn = Button(MenuFrame, text='Confirm',width=14, height=2, bd='1', anchor=CENTER, command=self.SubmitUpload)
        submitBtn.pack(side=RIGHT, fill=Y, padx=20)

        MenuFrame.pack(side=BOTTOM, fill=Y,  pady=20, padx=20)

    def SubmitUpload(self):
        res = server.updateProduct(
            self._id,
            self.frames[0].get(), # Title
            self.frames[1].get(), # Details,

            self.frames[2].get(), # Price
            self.frames[4].get(), # Category
            self.frames[3].get(), # Subcate

            self.frames[5].get(), # Quantity
            self.frames[6].get(), # MinStock
            self.frames[7].get(), # MaxStock
        )

        if res.status_code == 200: self.WindowExit()

    def removeProduct(self):
        awns = askyesno(title="Remove Product?", message="Are you sure to remove?")

        if awns:
            res = server.deleteDocument("Product", self._id)
            if res.status_code == 200: self.WindowExit()

    def WindowExit(self):
        self.Window.destroy()
        self.main.refetchTree()
        return 200