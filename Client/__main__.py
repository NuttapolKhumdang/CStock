from tkinter import *
from tkinter import ttk
import tkinter as tk

from sapi import API, ROOTURL
server = API(ROOTURL)

from addCategory import AddCategory
from allCategory import AllCategory

from addProduct import AddProduct
from editProduct import EditProduct

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('CStore pyClient')
        self.root.geometry('1080x400')
        self.seletingId = 0

        self.Category = server.getCategory().json()

        mastermenu = Menu(self.root)
        self.root.config(menu=mastermenu)

        fileMenu = Menu(mastermenu, tearoff=False)
        mastermenu.add_cascade(label="File", menu=fileMenu)

        ProductMenu = Menu(mastermenu, tearoff=False)
        mastermenu.add_cascade(label="Product", menu=ProductMenu)

        fileMenu.add_command(label="Refetch Database", command=self.refetchTree)
        fileMenu.add_command(label="Quit", command=self.root.destroy)

        ProductMenu.add_command(label="Add Product", command=lambda: AddProduct(self, self.root))
        ProductMenu.add_command(label="Edit Product", command=lambda: EditProduct(self, self.root, self.seletingId))
        ProductMenu.add_separator()
        ProductMenu.add_command(label="Refetch Category", command=self.refetchAll)
        ProductMenu.add_command(label="Config Category", command=lambda: AllCategory(self, self.root))

        # define columns
        columns = ('id', 'title', 'details', 'price', 'category', 'quantity', 'status')

        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: \
                            self.treeview_sort_column(self.tree, _col, False))

        self.tree.column('id', width=200, anchor=W)
        self.tree.column('title', width=140)
        self.tree.column('details', width=240, anchor=W)
        self.tree.column('price', width=80, anchor=E)
        self.tree.column('category', width=180, anchor=W)
        self.tree.column('quantity', width=80, anchor=CENTER)
        self.tree.column('status', width=80, anchor=CENTER)

        # define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title', anchor=W)
        self.tree.heading('details', text='Details', anchor=W)
        self.tree.heading('price', text='Price')
        self.tree.heading('category', text='Category')
        self.tree.heading('quantity', text='Quantity')
        self.tree.heading('status', text='Stock Status')

        # add data to the treeview
        self.refetchTree()

        def editContent(event):
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                record = item['values']
                EditProduct(self, self.root, record[0])

        def selectingRow(event):
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                record = item['values']
                self.seletingId = record[0]

        self.tree.bind('<<TreeviewSelect>>', selectingRow)
        self.tree.bind('<Double-1>', editContent)

        # self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.pack(side=LEFT,fill=BOTH, expand=1)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=LEFT, fill=BOTH, expand=0)

    def refetchTree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i in server.getProduct().json():
            skey = ["OUT", 'MIN', 'OK', 'MAX', 'OVER']
            status = ''

            if i['Quantity'] == 0: status = skey[0]
            elif i['Quantity'] <= i['MinStock']: status = skey[1]
            elif i['Quantity'] > i['MinStock'] and i['Quantity'] < i['MaxStock'] : status = skey[2]
            elif i['Quantity'] == i['MaxStock'] : status = skey[3]
            elif i['Quantity'] > i['MaxStock'] : status = skey[4]
            else: status = None

            product = (i['_id'], i['Title'],i['Details'] if 'Details' in i else "", i['Price'], self.searchCategory(i['Category']), i['Quantity'], status)
            self.tree.insert('', tk.END, values=product)

    def refetchCategory(self):
        self.Category = server.getCategory().json()

    def refetchAll(self):
        self.refetchCategory()
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
    
    def searchCategory(self, _id):
        for i in self.Category:
            if i["_id"] == _id:
                return i["Title"]
                break

if __name__ == '__main__':
    # searchCategory()
    app = App()
    app.root.mainloop()
