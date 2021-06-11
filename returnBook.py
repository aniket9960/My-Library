from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from aifc import Error

con = sqlite3.connect('library.db')
cur = con.cursor()




class ReturnBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x400+40+20")
        self.title("Return Book")
        self.resizable(False, False)

        query = "SELECT * FROM borrows"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(book[1])
        book_list.sort()

        #######################Frames#######################

        # Top Frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)
        # Bottom Frame
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)
        # heading, image
        self.top_image = PhotoImage(file='icons\\addperson.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text='  Return Book ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        ###########################################Entries and Labels########################3

        # book name
        global Book_name
        Book_name= StringVar()
        self.lbl_name = Label(self.bottomFrame, text='Book: ', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=Book_name)
        self.combo_name['values'] = book_list
        self.combo_name.place(x=150, y=45)

        self.lbl_phone = Label(self.bottomFrame, text='Member: ', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.memberName = Label(self.bottomFrame, font='arial 15 bold', fg='white',
                                bg='#fcc324')
        self.memberName.place(x=150, y=85)

        self.combo_name.bind("<<ComboboxSelected>>", self.disp_member)

        # Button
        button = Button(self.bottomFrame, text='Return Book', command=self.return_book)
        button.place(x=220, y=120)

    def disp_member(self, arg):
        self.book = Book_name.get()
        print(self.book)
        borrower = ""
        memberName = cur.execute("SELECT * FROM borrows")
        for mn in memberName:
            if self.book == mn[1]:
                borrower = mn[2]
                break
        self.memberName.configure(text=borrower)

    def return_book(self):

        book_id = self.book.split('-')[0]
        print(book_id," ",self.book)
        if self.book !="":
            try:
                query = "DELETE from borrows where bbook_id='"+self.book+"'"
                cur.execute(query)
                con.commit()
                messagebox.showinfo("Success", "Successfully Updated!", icon='info')
                cur.execute("UPDATE books SET book_status = ? WHERE book_id = ?", (0, book_id))
                con.commit()
                self.destroy()
            except Error:
                print(Error)
                messagebox.showerror("Error", "Cant update the data", icon='warning')

        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')
            self.destroy()

