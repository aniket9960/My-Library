import sqlite3
from aifc import Error
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import addBook
import addMember
import giveBook
import returnBook

con = sqlite3.connect('library.db')
cur = con.cursor()


class Main(object):
    def __init__(self, master):
        self.master = master

        def displayStatistics(evt):
            count_books = cur.execute("SELECT count(book_id) FROM books").fetchall()
            count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchall()
            self.lbl_book_count.config(text='Total :' + str(count_books[0][0]) + " books in library")
            self.lbl_member_count.config(text='Total member :' + str(count_members[0][0]))
            self.lbl_borrowed_count.config(text='Taken books :' + str(taken_books[0][0]))
            displayBooks(self)

        def displayBooks(self):
            books = cur.execute("SELECT * FROM books").fetchall()
            count = 0
            self.list_books.delete(0, END)
            for book in books:
                self.list_books.insert(count, (str(book[0]) + "-" + book[1]))
                count += 1

            def bookInfo(evt):
                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('-')[0]
                book = cur.execute("SELECT * FROM books WHERE book_id=?", (id,))
                book_info = book.fetchall()

                self.list_details.delete(0, END)
                self.list_details.insert(0, "Book Name :" + book_info[0][1])
                self.list_details.insert(1, "Book Author :" + book_info[0][2])
                self.list_details.insert(2, "Book Page :" + book_info[0][3])
                self.list_details.insert(3, "Book Language :" + book_info[0][4])
                if book_info[0][5] == 0:
                    self.list_details.insert(4, "Status : Avaiable")
                else:
                    self.list_details.insert(4, "Status : Not Avaiable")

            def doubleClick(evt):
                global given_id
                value = str(self.list_books.get(self.list_books.curselection()))
                given_id = value.split('-')[0]
                give_book = GiveBook()

            self.list_books.bind('<<ListboxSelect>>', bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>', displayStatistics)
            self.list_books.bind('<Double-Button-1>', doubleClick)

        ############################################ Frames ############################################################
        mainFrame = Frame(self.master)
        mainFrame.pack()

        ############################################# Top Frame ########################################################
        topFrame = Frame(mainFrame, width=1350, height=70, bg='#f8f8f8', padx=20, relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP, fill=X)

        ############################################# Center Frame #####################################################
        centerFrame = Frame(mainFrame, width=1350, height=680, relief=RIDGE, bg='#e0f0f0')
        centerFrame.pack(side=TOP)

        ############################################# Center Left Frame ################################################
        centerLeftFrame = Frame(centerFrame, width=900, height=700, bg='#e0f0f0', borderwidth=2, relief=SUNKEN)
        centerLeftFrame.pack(side=LEFT)

        ############################################# Center Right Frame ###############################################
        centerRightFrame = Frame(centerFrame, width=450, height=700, bg='#e0f0f0', borderwidth=2, relief=SUNKEN)
        centerRightFrame.pack()

        ############################################# Search Bar #######################################################
        searchBar = LabelFrame(centerRightFrame, width=440, height=175, text='Search Box', bg='#9bc9ff')
        searchBar.pack(fill=BOTH)
        self.lbl_search = Label(searchBar, text='Search :', font='arial 12 bold', bg='#9bc9ff', fg='white')
        self.lbl_search.grid(row=0, column=0, padx=20, pady=10)
        self.entry_search = Entry(searchBar, width=30, bd=10)
        self.entry_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
        self.btn_search = Button(searchBar, text='Search', font='arial 12 bold', bg='#fcc324', fg='white',
                                 command=self.searchBooks)
        self.btn_search.grid(row=0, column=4, padx=20, pady=10)

        ############################################# List bar #########################################################
        listBar = LabelFrame(centerRightFrame, width=440, height=75, text='List Box', bg='#fcc324')
        listBar.pack(fill=BOTH)
        lbl_list = Label(listBar, text='Sort By', font='times 16 bold', fg='#2488ff', bg='#fcc324')
        lbl_list.grid(row=0, column=2)
        self.listChoice = IntVar()
        rb1 = Radiobutton(listBar, text='All Books', var=self.listChoice, value=1, bg='#fcc324')
        rb2 = Radiobutton(listBar, text='In Library', var=self.listChoice, value=2, bg='#fcc324')
        rb3 = Radiobutton(listBar, text='Borrowed', var=self.listChoice, value=3, bg='#fcc324')
        rb1.grid(row=1, column=0)
        rb2.grid(row=1, column=1)
        rb3.grid(row=1, column=2)
        btn_list = Button(listBar, text='List Books', bg='#2488ff', fg='white', font='arial 12', command=self.listBooks)
        btn_list.grid(row=1, column=3, padx=40, pady=10)

        ############################################# Title and Image ##################################################
        image_bar = Frame(centerRightFrame, width=440, height=350)
        image_bar.pack(fill=BOTH)
        self.title_right = Label(image_bar, text='Welcome to our Library', font='arial 16 bold')
        self.title_right.grid(row=0)
        self.image_library = PhotoImage(file='icons\\library.png')
        self.lblImg = Label(image_bar, image=self.image_library)
        self.lblImg.grid(row=1)

        ############################################# Add Book #########################################################
        self.iconbook = PhotoImage(file='icons\\add_book.png')
        self.btnbook = Button(topFrame, text='Add Book', image=self.iconbook, compound=LEFT, font='arial 12 bold',
                              command=self.addBook)
        self.btnbook.pack(side=LEFT, padx=10)

        ############################################# Add Member #######################################################
        self.iconmember = PhotoImage(file='icons\\users.png')
        self.btnmember = Button(topFrame, text='Add Member', font='arial 12 bold', command=self.addMember)
        self.btnmember.configure(image=self.iconmember, compound=LEFT, padx=10)
        self.btnmember.pack(side=LEFT)

        ############################################# Give Book ########################################################
        self.icongivebook = PhotoImage(file='icons\\givebook.png')
        self.btngivebook = Button(topFrame, text='Give Book', font='arial 12 bold', padx=10, image=self.icongivebook,
                                  compound=LEFT, command=self.giveBook)
        self.btngivebook.pack(side=LEFT)
        ############################################# Return Book ######################################################
        self.icon_rtrnBook = PhotoImage(file='icons\\return_books.png')
        self.btnreturnBook = Button(topFrame, text='Return Book', font='arial 12 bold', padx=10, image=self.icon_rtrnBook, compound=LEFT, command=self.return_book)
        self.btnreturnBook.pack(side=LEFT)

        ############################################# Tabs #############################################################

        ############################ Tab 1 ############################
        self.tabs = ttk.Notebook(centerLeftFrame, width=900, height=660)
        self.tabs.pack()
        self.tab1_icon = PhotoImage(file='icons\\books.png')
        self.tab2_icon = PhotoImage(file='icons\\members.png')
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text='Library Management', image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text='Statistics', image=self.tab2_icon, compound=LEFT)

        ############################ Tab 2 ############################
        # Statistics tab
        self.lbl_book_count = Label(self.tab2, text='', pady=20, font='verdana 14 bold')
        self.lbl_book_count.grid(row=0, sticky=W)
        self.lbl_member_count = Label(self.tab2, text='', pady=20, font='verdana 14 bold')
        self.lbl_member_count.grid(row=1, sticky=W)
        self.lbl_borrowed_count = Label(self.tab2, text='', pady=20, font='verdana 14 bold')
        self.lbl_borrowed_count.grid(row=3, sticky=W)

        ############################################# List Books #######################################################
        self.list_books = Listbox(self.tab1, width=40, height=30, bd=5, font='times 12 bold')
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.list_books.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=0, sticky=N + S + E)

        ############################################# List Details #####################################################
        self.list_details = Listbox(self.tab1, width=80, height=30, bd=5, font='times 12 bold')
        self.list_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)

        # functions
        displayBooks(self)
        displayStatistics(self)

    def addBook(self):
        add = addBook.AddBook()

    def addMember(self):
        member = addMember.AddMember()

    def searchBooks(self):
        value = self.entry_search.get()
        search = cur.execute("SELECT * FROM books WHERE book_name LIKE ?", ('%' + value + '%',)).fetchall()
        self.list_books.delete(0, END)
        count = 0
        for book in search:
            self.list_books.insert(count, (str(book[0]) + "-" + book[1]))
            count += 1

    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allBooks = cur.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0, END)
            count = 0
            for book in allBooks:
                self.list_books.insert(count, (str(book[0]) + "-" + book[1]))
                count += 1
        elif value == 2:
            books_in_library = cur.execute("SELECT * FROM books WHERE book_status=?", (0,)).fetchall()
            self.list_books.delete(0, END)
            count = 0
            for book in books_in_library:
                self.list_books.insert(count, (str(book[0]) + "-" + book[1]))
                count += 1
        else:
            taken_books = cur.execute("SELECT * FROM books WHERE book_status=?", (1,)).fetchall()
            self.list_books.delete(0, END)
            count = 0
            for book in taken_books:
                self.list_books.insert(count, (str(book[0]) + "-" + book[1]))
                count += 1

    def giveBook(self):
        give_book = giveBook.GiveBook()

    def return_book(self):
        rtn_book = returnBook.ReturnBook()

class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x400+40+20")
        self.title('Lend Book')
        self.resizable(False, False)
        global given_id
        self.book_id = int(given_id)
        query = "SELECT * FROM books"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append((str(book[0])) + "-" + book[1])

        query2 = "SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append((str(member[0])) + "-" + member[1])

        ############################### Frames ###############################

        ############################### TOP Frame ############################
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        ############################### Bottom Frame ###############################
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        ############################### Heading, Image ###############################
        self.topImg = PhotoImage(file='icons\\addperson.png')
        top_img_lbl = Label(self.topFrame, image=self.topImg, bg='white')
        top_img_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text=' Lend Book ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        ############################### Entries and Labels ###############################
        # name
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text='Book Name :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combo_name['values'] = book_list
        self.combo_name.current(self.book_id - 1)
        self.combo_name.place(x=195, y=45)

        # member name
        self.member_name = StringVar()
        self.lbl_mem_name = Label(self.bottomFrame, text='Member Name :', font='arial 15 bold', fg='white',
                                  bg='#fcc324')
        self.lbl_mem_name.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member['values'] = member_list
        self.combo_member.place(x=195, y=85)

        # Button
        button = Button(self.bottomFrame, text='Lend Book', command=self.lendBook)
        button.place(x=270, y=120)

    def lendBook(self):
        book_name = self.book_name.get()
        member_name = self.member_name.get()
        if (book_name and member_name != ""):
            try:
                query = "INSERT INTO 'borrows'(bbook_id,bmember_id) VALUES(?,?)"
                cur.execute(query, (book_name, member_name))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database", icon='info')
                cur.execute("UPDATE books SET book_status =? WHERE book_id=?", (1, self.book_id))
                con.commit()

            except Error:

                messagebox.showerror("Error", "Cant add to database", icon='warning')

        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')



def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1350x750+50+25")
    root.iconbitmap('icons\\icon.ico')
    root.mainloop()


if __name__ == '__main__':
    main()
