#!/usr/bin/env python3
import MySQLdb
from datetime import datetime


class DatabaseUtils:
    HOST = "35.244.118.23"
    USER = "root"
    PASSWORD = "abdosalah"
    DATABASE = "test_db"

    def __init__(self, connection=None):
        if(connection is None):
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

    def getBorrowedBooks(self, username):
        userId = self.getUserId(username)
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select BookID from BookBorrowed Where LmsUserID = %s and Status = 'borrowed'", (userId,))
            return cursor.fetchall()

    def getBookByAuthor(self, bookAuthor):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select * from Book Where Author = %s", (bookAuthor,))
            return cursor.fetchall()

    def borrowBook(self, username, bookId, returnDate):
        userId = self.getUserId(username)
        borrowedDate = datetime.now().strftime('%Y-%m-%d')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "insert into BookBorrowed (LmsUserID, BookID, BorrowedDate, ReturnedDate, Status) values (%s, %s, %s, %s, %s)",
                (userId, bookId, borrowedDate, returnDate, 'borrowed',))
            self.connection.commit()

    # Returns True if the book is Borrowed and False otherwise
    def isBookBorrowed(self, username, bookId):
        userId = self.getUserId(username)
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select Status from BookBorrowed Where BookID= %s and LmsUserID = %s ", (bookId, userId, )
            )
            if ( cursor.rowcount > 0 ):
                for status in cursor.fetchall():
                    if (status == ('borrowed',)):
                        return True
            return False

    # Changes the status of the Book to returned
    def returnBook(self, username, bookId):
        userId = self.getUserId(username)
        with self.connection.cursor() as cursor:
            cursor.execute(
                "update BookBorrowed set Status = 'returned' Where BookID= %s and LmsUserID = %s and Status = 'borrowed'", (
                    bookId, userId, )
            )
            self.connection.commit()

    def getUserId(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "select LmsUserID from LmsUser where UserName = %s", (username,))
            for row in cursor.fetchall():
                return(row[0])
