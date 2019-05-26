from database_utils import DatabaseUtils
from datetime import datetime
import socket, json, sys
sys.path.append('./receptionPI')
import socket_utils
sys.path.append('./google_calendar')
from add_event import createGoogleEvent
from voiceRecognition import speechTranslation

class Menu:

    userName = NotImplemented
    db = NotImplemented
    isRunnig = True
    display_menu = "1.Search\n2.Borrow\n3.Return\n4.Logout\n"
    author_menu = "Please enter the name of the Author\n"
    title_menu = "Please enter the Title of the book\n"
    search_type = "1.Search by Author\n2.Search by Title\n"
    selectBookPromt = "Please Select a book by ID\n"
    selectActionPromt = "1.Borrow Book\n2.Return Book\n"
    voice_promt = "1.User voice Recognition \n2.Normal text search\n"
    searchedBooks = []
    borrowedBooks = []
    returnDatePromt = "enter return date in the format DD-MM-YYYY\n"
    HOST = '0.0.0.0'
    PORT = 63000  # Port to listen on (non-privileged ports are > 1023).
    ADDRESS = (HOST, PORT)
    
    def __init__(self):
        self.db = DatabaseUtils()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRESS)
            s.listen()

            print("Listening on {}...".format(self.ADDRESS))
            while True:
                print("Waiting for Reception Pi...")
                conn, addr = s.accept()
                with conn:
                    print("Connected to {}".format(addr))
                    print()

                    #recieving information from the reception pi
                    user = socket_utils.recvJson(conn)
                    self.userName = user
                    #HERE IS WHERE OUR MENU WILL BE PLACED
                    self.startTheMenu()

                    #closing the connection by sending logout = True
                    socket_utils.sendJson(conn, {"logout": True})



    def startTheMenu(self):
        print("Welcome {}".format(self.userName))
        while(self.isRunnig):

            choice = input(self.display_menu)

            if (choice == '1'):
                self.searchForBook('search')
            elif(choice == '2'):
                self.searchForBook('borrow')
            elif (choice == '3'):
                self.findBorrowedBooks()
                book = self.selectBook(self.borrowedBooks)
                if (book):
                    self.db.returnBook(self.userName, book[0])
                    print("The Book was successfully returned!\n")
                else:
                    print("Book selected isnt part of the list\n")
            elif (choice == '4'):
                self.isRunnig = False
            else:
                print("Invalid Choice")

    #Searches through the db using the Author's name
    def searchByAuthor(self, author):
        for value in self.db.getBookByAuthor(author):
            bookId, title, author, pDate = value
            stringDate = pDate.strftime('%m/%d/%Y')
            #Add the results to the searchedBooks Array
            self.searchedBooks.append(bookId)
            print(str(bookId)+'\t'+title+'\t'+author+'\t'+stringDate+'\n')
        
        print('\n')
    
    #Promts the user for an ID and then checks it against the selected Array
    def selectBook(self, myArray):
        selectedBook = input(self.selectBookPromt)
        if (int(selectedBook) in myArray):
            for value in self.db.getBookById(int(selectedBook)):
                bookId, title, author, pDate = value
                stringDate = pDate.strftime('%m/%d/%Y')
                print(str(bookId)+'\t'+title+'\t'+author+'\t'+stringDate+'\n')
                return value
        else:
            return False

    #Searches through the db using the Book's Title
    def searchByTitle(self, title):
        for value in self.db.getBookByTitle(title):
            bookId, title, author, pDate = value
            stringDate = pDate.strftime('%m/%d/%Y')
            #Add the results to the searchedBooks Array
            self.searchedBooks.append(bookId)
            print(str(bookId)+'\t'+title+'\t'+author+'\t'+stringDate+'\n')
        print('\n')

    #Handles the logic of Borrowing a book
    def borrowBook(self, book):
        #Promt the user for the return date and validate it
        myDate = input(self.returnDatePromt)
        selectedDate = datetime.strptime(myDate, '%d-%m-%Y')
        value = selectedDate.date() - datetime.now().date()
        if (value.days > 7 ):
            self.db.borrowBook(self.userName, book[0], selectedDate.date())
            self.createReturnEvent(selectedDate, book[1])
        else:
            print("Invalid return Date")



    def createReturnEvent(self, returnDate, bookName):
        newEvent = createGoogleEvent()
        newEvent.insert(self.userName, returnDate, bookName)




    def findBorrowedBooks(self):
        for value in self.db.getBorrowedBooks(self.userName):
            book = self.db.getBookById(value[0])
            bookId, title, author, pDate = book[0]
            stringDate = pDate.strftime('%m/%d/%Y')
            #Add the results to the borrowedBooks Array
            self.borrowedBooks.append(bookId)
            print(str(bookId)+'\t'+title+'\t'+author+'\t'+stringDate+'\n')

        print('\n')


    def textOrSpeech(self):

        userChoice = input(self.voice_promt)

        if (userChoice == '1'):
            mySpeech = speechTranslation()
            return mySpeech.translateSpeech()
        else:
            selectedText = input(self.author_menu)
            return selectedText







    #Promts the user for a Search type, either by Author's name or Book Title    
    def searchForBook(self, chosenOption):
        searchType = input(self.search_type)
        #Search by Author
        if (searchType == '1'):
            selectedAuthor = self.textOrSpeech()
            self.searchByAuthor(selectedAuthor)
            book = self.selectBook(self.searchedBooks)
            #checks if a valid choice was selected
            if (book):
                self.borrowOrReturn(book)
            else:
                print("Invalid Choice")
        #Search by Title
        elif (searchType == '2'):
            selectedTitle = self.textOrSpeech()
            self.searchByTitle(selectedTitle)
            book = self.selectBook(self.searchedBooks)
            #checks if a valid choice was selected
            if (book):
                self.borrowOrReturn(book)
        else:
            print("Invalid Choice")

    #TODO
    # def handleLogic(self, book, chosenOption):
    #     if (chosenOption == 'search'):
    #         self.borrowOrReturn(book)
    #     print()

    def borrowOrReturn(self, book):
        desiredAction = input(self.selectActionPromt)
        #Borrow book
        if (desiredAction == '1'):
            #cheking if the book is not borrowed
            if (not self.db.isBookBorrowed(self.userName, book[0])):
                #allow borrowing
                self.borrowBook(book)
                print("The Book was successfully borrowed!\n")
            else:
                print("The chosen book is already Borrowed\n")
        #Return book
        elif (desiredAction == '2'):
            #Checking if the book is borrowed
            if (self.db.isBookBorrowed(self.userName, book[0])):
                #allow return
                self.db.returnBook(self.userName, book[0])
                print("The Book was successfully returned!\n")
            else:
                print("The chosen book is not Borrowed\n")
        else:
            print("Invalid Choice")

    

start = Menu()
