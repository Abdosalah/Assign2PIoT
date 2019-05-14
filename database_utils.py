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

    # def insertUser(self, username, name):
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(
    #             "insert into LmsUser (UserName, name) values (%s, %s)", (username, name,))
    #     self.connection.commit()

    def getBookByTitle(self, bookTitle):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select * from Book Where Title = %s", (bookTitle,))
            return cursor.fetchall()

    def getBookByAuthor(self, bookAuthor):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select * from Book Where Author = %s", (bookAuthor,))
            return cursor.fetchall()

    def borrowBook(self, userId, bookId):
        borrowedDate = datetime.now().strftime('%Y-%m-%d')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "insert into BookBorrowed (LmsUserID, BookID, BorrowedDate, Status) values (%s, %s, %s, %s)", 
                (userId, bookId, borrowedDate, 'borrowed',))
            self.connection.commit()
    # def deletePerson(self, personID):
    #     with self.connection.cursor() as cursor:
    #         # Note there is an intentionally placed bug here: != should be =
    #         cursor.execute("delete from Person where PersonID = %s", (personID,))
    #     self.connection.commit()
            


# myDb = DatabaseUtils()

# myDb.insertUser('AbdoSalah', 'Abdulrhman')
# myDb.borrowBook('1', '3')




# myDb.insertBook('The Shock Doctrine', 'Naomi Klein', '2007-02-18')
# myDb.insertBook('The Prince', 'Niccoló Machiavelli', '1532-11-08')
# myDb.insertBook('The Winds of Winter', 'GRRM', '2019-01-25')
# myDb.insertBook('A Clash of Kings', 'GRRM', '1999-02-15')
# myDb.insertBook('A Game of Thrones', 'GRRM', '1996-08-28')
# myDb.insertBook('A Feast for Crows', 'GRRM', '2005-11-24')
# myDb.insertBook('A Dance with Drangons', 'GRRM', '2011-07-20')

