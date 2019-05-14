from database_utils import DatabaseUtils

class Menu:

    db = NotImplemented
    isRunnig = True
    display_menu = "1.Search\n2.Borrow\n3.Return\n4.Logout\n"
    author_menu = "Please enter the name of the Author\n"
    title_menu = "Please enter the Title of the book\n"
    search_type = "1.Search by Author\n2.Search by Title\n"
    
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
            print(title+'\t'+author+'\t'+stringDate)
        print('\n')
    
    def searchByTitle(self, title):
        for value in self.db.getBookByTitle(title):
            bookId, title, author, pDate = value
            stringDate = pDate.strftime('%m/%d/%Y')
            print(title+'\t'+author+'\t'+stringDate)
        print('\n')
    
    def searchForBook(self):
        searchType = input(self.search_type)
        if (searchType == '1'):
            selectedAuthor = input(self.author_menu)
            self.searchByAuthor(selectedAuthor)
        elif (searchType == '2'):
            selectedTitle = input(self.title_menu)
            self.searchByTitle(selectedTitle)
        else:
            print("Invalid Choice")
    

start = Menu()
