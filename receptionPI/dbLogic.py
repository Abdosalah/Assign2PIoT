import sqlite3 as lite


class DbUser:
    __userName = NotImplemented
    __password = NotImplemented
    __firstName = NotImplemented
    __lastName = NotImplemented
    __email = NotImplemented
    __db = NotImplemented

    def __init__(self, dbName):
        
        
        self.__db = lite.connect(dbName)
        

    def registerUser(self, userName, password, firstName, lastName, email):
       
        self.__userName = userName
        self.__password = password
        self.__firstName = firstName
        self.__lastName = lastName
        self.__email = email

        record = (self.__userName, self.__password, self.__firstName, self.__lastName, self.__email)
        
        cur = self.__db.cursor()
        cur.execute(
        "INSERT INTO library_data VALUES (?,?,?,?,?)", record)

        self.__db.commit()

    def isUsernameUsed(self, userName):
        cur = self.__db.cursor()
        data = cur.execute("SELECT userName FROM library_data WHERE userName = ?",
                   (userName,))

        for row in data:
            return True

        return False


myDb = DbUser('library.db')

print(myDb.isUsernameUsed('Abdo'))