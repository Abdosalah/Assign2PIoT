from database_utils import DatabaseUtils
from datetime import datetime

class Menu:

    db = NotImplemented
    isRunnig = True
    display_menu = "1.Search\n2.Borrow\n3.Return\n4.Logout\n"
    author_menu = "Please enter the name of the Author\n"
    title_menu = "Please enter the Title of the book\n"
    search_type = "1.Search by Author\n2.Search by Title\n"
    selectBook = "Please Select a book to borrow\n"
    searchedBooks = []
    returnDatePromt = "enter return date in the format DD-MM-YYYY\n"
    
    def __init__(self):
        self.db = DatabaseUtils()

        while(self.isRunnig):

            choice = input(self.display_menu)

            if (choice == '1'):
                self.searchForBook()
            elif(choice == '2'):
                print("two")
            elif (choice == '3'):
                print("three")
            elif (choice == '4'):
                self.isRunnig = False
            else:
                print("Invalid Choice")


    def searchByAuthor(self, author):
        for value in self.db.getBookByAuthor(author):
            bookId, title, author, pDate = value
            stringDate = pDate.strftime('%m/%d/%Y')
            self.searchedBooks.append(bookId)
            print(str(bookId)+'\t'+title+'\t'+author+'\t'+stringDate+'\n')
        
        print('\n')

    def selectBookToBorrow(self):
        selectedBook = input(self.selectBook)
        if (int(selectedBook) in self.searchedBooks ):
            for value in self.db.getBookById(int(selectedBook)):
                return value
        else:
            print("Invalid choice in bookToBorrow")

    
    def searchByTitle(self, title):
        for value in self.db.getBookByTitle(title):
            bookId, title, author, pDate = value
            stringDate = pDate.strftime('%m/%d/%Y')
            self.searchedBooks.append(bookId)
            print(str(bookId)+'\t'+title+'\t'+author+'\t'+stringDate+'\n')
        print('\n')

    def borrowBook(self, book):
        bookId, title, author, pDate = book
        #Promt the user for the return date and validate it
        myDate = input(self.returnDatePromt)
        selectedDate = datetime.strptime(myDate, '%d-%m-%Y')
        value = selectedDate.date() - datetime.now().date()
        if (value.days > 7 ):
            #call borrowBook from database_utils.py
            print("Valid return Date")
        else:
            print("Invalid return Date")

    
    def searchForBook(self):
        searchType = input(self.search_type)
        if (searchType == '1'):
            selectedAuthor = input(self.author_menu)
            self.searchByAuthor(selectedAuthor)
            record = self.selectBookToBorrow()
            self.borrowBook(record)
        elif (searchType == '2'):
            selectedTitle = input(self.title_menu)
            self.searchByTitle(selectedTitle)
            record = self.selectBookToBorrow()
            print(record)
        else:
            print("Invalid Choice")
    

start = Menu()
