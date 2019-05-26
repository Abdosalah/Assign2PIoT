#credits for the hashing fucntions https://www.vitoshacademy.com/hashing-passwords-in-python/
import sqlite3 as lite
import re
import hashlib
import binascii
import os
from recognise import facialRecognition

class LocalUser:
    __userName = NotImplemented
    __password = NotImplemented
    __firstName = NotImplemented
    __lastName = NotImplemented
    __email = NotImplemented
    __db = NotImplemented
    __myFacialRecognition = None

    def __init__(self, dbName):
        
        
        self.__db = lite.connect(dbName)
        

    def registerUser(self, userName, password, firstName, lastName, email):
       
        if ( self.isLengthValid(userName, 4) and not self.isUsernameUsed(userName)):
            self.__userName = userName
        else:
            print("--Invalid Username")
            return False
        
        if (self.isLengthValid(password, 5)):
            self.__password = self.hash_password(password)
        else:
            print("--Invalid Length of Password")
            return False
        
        if (self.isLengthValid(firstName, 3)):
            self.__firstName = firstName
        else:
            print("--Invalid Length of Firstname")
            return False
        
        if (self.isLengthValid(lastName, 3)):
            self.__lastName = lastName
        else:
            print("--Invalid Length of Lastname")
            return False

        if ( self.isEmailValid(email) ):
            self.__email = email
        else:
            print("--Invalid Email")
            return False

        record = (self.__userName, self.__password, self.__firstName, self.__lastName, self.__email)
        
        cur = self.__db.cursor()
        cur.execute(
        "INSERT INTO library_data VALUES (?,?,?,?,?)", record)

        self.__db.commit()

        return True


    def loginUsingCredentials(self, userName, password):
        cur = self.__db.cursor()
        data = cur.execute("SELECT userName, password FROM library_data WHERE userName = ?",
                           (userName,))

        for row in data:
            if (self.verify_password(row[1], password)):
                return True

        return False

    def loginUsingFR(self):
        self.__myFacialRecognition = facialRecognition()
        userName = self.__myFacialRecognition.startRecognizing()

        if( userName is False):
            return False

        cur = self.__db.cursor()
        data = cur.execute("SELECT userName, password FROM library_data WHERE userName = ?",
                           (userName,))

        for row in data:
            print("User found: {}".format(row[0]))
            return True

        return False


    def isUsernameUsed(self, userName):
        cur = self.__db.cursor()
        data = cur.execute("SELECT userName FROM library_data WHERE userName = ?",
                   (userName,))

        for row in data:
            return True

        return False

    def isLengthValid(self, variable, minLength):
        if (variable.__len__() >= minLength):
            return True
        return False

    def isEmailValid(self, email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else:
            return False

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')


    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                    provided_password.encode('utf-8'),
                                    salt.encode('ascii'),
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password



# myDb = DbUser('UsersRP.db')

# print(myDb.loginUsingFR())

# myDb.loginUsingCredentials('abdo', 'abdosalah')

# myDb.registerUser('Abdo', '12345678', 'Abdo', 'Salah', 'wtv1@gmail.com')
# myDb.registerUser('Mahtab', '87654321', 'Abdo', 'Salah', 'wtv2@gmail.com')
# myDb.registerUser('Wtv1234', '1234567890', 'Abdo', 'Salah', 'wtv3@gmail.com')

# hashedPass = myDb.hash_password('mypassword')

# print(myDb.verify_password(hashedPass, 'mypassword'))
