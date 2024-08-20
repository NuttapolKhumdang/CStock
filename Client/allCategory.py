from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
import tkinter as tk

from sapi import API, ROOTURL
server = API(ROOTURL)

class AllCategory:
    def __init__(self, main, root):
        self.frames = []
        self.main = main

        self.Window = Toplevel(root)
        self.Window.title("Config Category")
        self.Window.geometry("480x460")

        iFrame = Frame(self.Window)
        self.entryText = StringVar()
        self.iField = Entry(iFrame, width=20, font=('TkDefaultFont', 16), textvariable=self.entryText)
        self.iField.pack(side=LEFT, fill=BOTH, expand=1)

        addBtn = Button(iFrame, text='Add',width=8, height=2, bd='1', anchor=CENTER, command=self.SubmitUpload)
        addBtn.pack(side=LEFT, fill=Y, expand=0)

        addBtn = Button(iFrame, text='Update',width=8, height=2, bd='1', anchor=CENTER, command=self.updateCategory)
        addBtn.pack(side=LEFT, fill=Y, expand=0)

        removeBtn = Button(iFrame, text='Remove',width=8, height=2, bd='1', anchor=CENTER, command=self.removeCategory)
        removeBtn.pack(side=LEFT, fill=Y, expand=0)

        iFrame.pack(side=TOP, fill=X)

        columns = ('id', 'title', 'qty')

        self.tree = ttk.Treeview(self.Window, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: \
                            self.treeview_sort_column(self.tree, _col, False))

        self.tree.column('id', width=160, anchor=W)
        self.tree.column('title', width=140)
        self.tree.column('qty', width=40, anchor=CENTER)

        # define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title', anchor=W)
        self.tree.heading('qty', text='Quatity')

        # add data to the treeview
        self.refetchTree()

        def editContent(event):
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                record = item['values']
                EditCategory(self, self.Window, record[0])

        def selectingRow(event):
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                record = item['values']
                self.seletingId = record[0]
                self.entryText.set(record[1])


        self.tree.bind('<<TreeviewSelect>>', selectingRow)
        self.tree.bind('<Double-1>', editContent)

        # self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.pack(side=LEFT,fill=BOTH, expand=1)

    def updateCategory(self):
        res = server.updateCategory(self.seletingId, self.iField.get())

        if res.status_code == 200: 
            self.entryText.set("")
            self.refetchTree()

    def SubmitUpload(self):
        res = server.newCategory(self.iField.get())
        if res.status_code == 200: 
            self.entryText.set("")
            self.refetchTree()

    def refetchTree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i in server.getCategory().json():
            product = (i['_id'], i['Title'], i['Quantity'])
            self.tree.insert('', tk.END, values=product)
    
    def removeCategory(self):
        res = server.deleteDocument("Category", self.seletingId)

        if res.status_code == 200: 
            self.entryText.set("")
            self.refetchTree()

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, text=col.capitalize(), command=lambda _col=col: \
                    self.treeview_sort_column(tv, _col, not reverse))

    def WindowExit(self):
        self.Window.destroy()
        self.main.refetchTree()
        return 200