import sqlite3


def run(dbname='winik.db'):

    CON = sqlite3.connect(dbname)
    CUR = CON.cursor()

    CUR.execute("""DROP TABLE IF EXISTS user;""")
    # create USER table FOR LOGIN AND SESSION
    CUR.execute("""CREATE TABLE user(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR,
        password VARCHAR,
        email VARCHAR,
        CONSTRAINT unique_username UNIQUE(username),
        CONSTRAINT unique_email UNIQUE(email)
    );""")

    CON.commit()
    CUR.close()
    CON.close()

if __name__ == '__main__':
    run()