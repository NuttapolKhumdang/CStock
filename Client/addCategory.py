from tkinter import *
from tkinter.messagebox import askyesno
import tkinter as tk

from sapi import API, ROOTURL
server = API(ROOTURL)

class AddCategory:
    def __init__(self, main, root):
        self.frames = []
        self.main = main

        self.Window = Toplevel(root)
        self.Window.title("New Category")
        self.Window.geometry("480x460")

        mainFrame = Frame(self.Window)

        iFrame = Frame(mainFrame)
        iLable = Label(iFrame, text="New Category Title", width=10, anchor=W, font=('TkDefaultFont', 10))
        iLable.pack(fill=X)

        self.iField = Entry(iFrame, width=60, font=('TkDefaultFont', 16))
        self.iField.pack(fill=X)
        iFrame.pack(fill=X, pady=4)
        mainFrame.pack(side=TOP, fill=BOTH, pady=20, padx=20)

        MenuFrame = Frame(self.Window)
        CancelBth = Button(MenuFrame, text='Cancle',width=20, height=2, bd='1', anchor=CENTER, command=self.Window.destroy)
        CancelBth.pack(side=LEFT, fill=Y, padx=20)

        submitBtn = Button(MenuFrame, text='Add',width=20, height=2, bd='1', anchor=CENTER, command=self.SubmitUpload)
        submitBtn.pack(side=RIGHT, fill=Y, padx=20)

        MenuFrame.pack(side=BOTTOM, fill=Y,  pady=20, padx=20)

    def SubmitUpload(self):
        res = server.newCategory(self.iField.get())
        if res.status_code == 200: self.WindowExit()

    def WindowExit(self):
        self.Window.destroy()
        self.main.refetchTree()
        return 200