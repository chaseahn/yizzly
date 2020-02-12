import sqlite3


def run(dbname='winik.db'):

    CON = sqlite3.connect(dbname)
    CUR = CON.cursor()

    """ USERS TABLE """
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

    """ CLIPS TABLE """
    CUR.execute("""DROP TABLE IF EXISTS clips;""")
    # create USER table FOR LOGIN AND SESSION
    CUR.execute("""CREATE TABLE clips(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id VARCHAR,
        home_team VARCHAR,
        away_team VARCHAR,
        game_date VARCHAR,
        rating VARCHAR,
        type VARCHAR,
        includes VARCHAR,
        players VARCHAR,
        description VARCHAR,
        quarter VARCHAR,
        time VARCHAR
    );""")
    

    CON.commit()
    CUR.close()
    CON.close()

if __name__ == '__main__':
    run()