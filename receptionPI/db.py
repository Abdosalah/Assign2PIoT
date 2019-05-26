import sqlite3 as lite

con = lite.connect('UsersRP.db')
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS library_data")
cur.execute(
    "CREATE TABLE library_data(userName text, password text, firstName text, lastName text, email text)")


con.commit()
con.close()