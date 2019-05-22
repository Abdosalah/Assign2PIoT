#!/usr/bin/env python3
import MySQLdb
from datetime import datetime

class DatabaseUtils:
    HOST = "35.244.118.23"
    USER = "root"
    PASSWORD = "abdosalah"
    DATABASE = "test_db"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def insertBook(self, name, author, publishedDate):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "insert into Book (Title, Author, PublishedDate) values (%s, %s, %s)", (name, author, publishedDate,))
        self.connection.commit()

        return cursor.rowcount == 1

    def insertUser(self, username, name):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "insert into LmsUser (UserName, name) values (%s, %s)", (username, name,))
        self.connection.commit()

    def getBookByTitle(self, bookTitle):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select * from Book Where Title = %s", (bookTitle,))
            return cursor.fetchall()

    def getBookById(self, bookId):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select * from Book Where BookID = %s", (bookId,))
            return cursor.fetchall()

    def getBorrowedBooks(self, userId):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select BookID from BookBorrowed Where LmsUserID = %s and Status = 'borrowed'", (userId,))
            return cursor.fetchall()

    def getBookByAuthor(self, bookAuthor):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select * from Book Where Author = %s", (bookAuthor,))
            return cursor.fetchall()

    def borrowBook(self, userId, bookId, returnDate):
        borrowedDate = datetime.now().strftime('%Y-%m-%d')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "insert into BookBorrowed (LmsUserID, BookID, BorrowedDate, ReturnedDate, Status) values (%s, %s, %s, %s, %s)",
                (userId, bookId, borrowedDate, returnDate, 'borrowed',))
            self.connection.commit()

    #Returns True if the book is Borrowed and False otherwise
    def isBookBorrowed(self, userId, bookId):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select Status from BookBorrowed Where BookID= %s and LmsUserID = %s ", (bookId, userId, )
            )
            if ( cursor.rowcount > 0 ):
                for status in cursor.fetchall():
                    if (status == ('borrowed',)):
                        return True
            return False

    #Changes the status of the Book to returned
    def returnBook(self, userId, bookId):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "update BookBorrowed set Status = 'returned' Where BookID= %s and LmsUserID = %s and Status = 'borrowed'", (
                    bookId, userId, )
            )
            self.connection.commit()


    # def deletePerson(self, personID):
    #     with self.connection.cursor() as cursor:
    #         # Note there is an intentionally placed bug here: != should be =
    #         cursor.execute("delete from Person where PersonID = %s", (personID,))
    #     self.connection.commit()
            


# myDb = DatabaseUtils()

# print(myDb.getBorrowedBooks(2))

# print(myDb.isBookBorrowed(3,5))

# myDb.returnBook(2, 3)

# print(myDb.isBookBorrowed(3))

# myDb.insertUser('Mahtab95', 'Mahtab')
# myDb.insertUser('Irfan123', 'Irfan')
# myDb.insertUser('abdo1', 'ABDO1')
# myDb.insertUser('abdo2', 'ABDO2')
# myDb.insertUser('abdo3', 'ABDO3')
# myDb.insertUser('abdo4', 'ABDO4')
# myDb.insertUser('abdo5', 'ABDO5')
# myDb.insertUser('abdo6', 'ABDO6')
# myDb.insertUser('abdo7', 'ABDO7')
# myDb.borrowBook('1', '20')
# myDb.borrowBook('1', '3')
# myDb.borrowBook('1', '5')




# myDb.insertBook('The Shock Doctrine', 'Naomi Klein', '2007-02-18')
# myDb.insertBook('The Prince', 'Niccoló Machiavelli', '1532-11-08')
# myDb.insertBook('The Winds of Winter', 'GRRM', '2019-01-25')
# myDb.insertBook('A Clash of Kings', 'GRRM', '1999-02-15')
# myDb.insertBook('A Game of Thrones', 'GRRM', '1996-08-28')
# myDb.insertBook('A Feast for Crows', 'GRRM', '2005-11-24')
# myDb.insertBook('A Dance with Drangons', 'GRRM', '2011-07-20')
# myDb.insertBook('Homage to Catalonia', 'George Orwell', '1938-04-25')
# myDb.insertBook('Frankenstein', 'Mary Shelley', '1823-07-20')
# myDb.insertBook('The Belonging Kind', 'William Gibson', '1981-07-20')
# myDb.insertBook('The Gernsback Continuum', 'William Gibson', '1981-07-20')
# myDb.insertBook('The War of the Worlds', 'H.G.Wells', '1898-07-20')
# myDb.insertBook('The Lord of the Rings', 'J.R.R.Tolkien', '1954-07-29')
# myDb.insertBook('1984', 'George Orwell', '1949-06-08')

