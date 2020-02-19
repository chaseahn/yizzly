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

    """ PLAYERS TABLE """
    CUR.execute("""DROP TABLE IF EXISTS players;""")
    # create USER table FOR LOGIN AND SESSION
    CUR.execute("""CREATE TABLE players(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR,
        last_name VARCHAR,
        team_id VARCHAR,
        years_pro VARCHAR,
        college_name VARCHAR,
        country VARCHAR,
        player_id VARCHAR,
        birth_date VARCHAR,
        start_nba VARCHAR,
        position VARCHAR,
        twitter VARCHAR,
        headshot VARCHAR,
        age INTEGER,
        weight VARCHAR,
        height VARCHAR,
        current_team VARCHAR,
        jersey_num VARCHAR,
        pbr_link VARCHAR,
        user_pk INTEGER,
        FOREIGN KEY(user_pk) REFERENCES user(pk)
    );""")

    """ STATS TABLE """
    CUR.execute("""DROP TABLE IF EXISTS stats;""")
    # create USER table FOR LOGIN AND SESSION
    CUR.execute("""CREATE TABLE stats(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        date_recorded VARCHAR,
        season VARCHAR,
        mp_per_g INTEGER, 
        fg_per_g INTEGER, 
        fga_per_g INTEGER, 
        fg_pct INTEGER, 
        fg3_per_g INTEGER, 
        fg3a_per_g INTEGER, 
        fg3_pct INTEGER, 
        fg2_per_g INTEGER, 
        fg2a_per_g INTEGER, 
        fg2_pct INTEGER, 
        efg_pct INTEGER, 
        ft_per_g INTEGER, 
        fta_per_g INTEGER, 
        ft_pct INTEGER, 
        orb_per_g INTEGER, 
        drb_per_g INTEGER,  
        trb_per_g INTEGER, 
        ast_per_g INTEGER, 
        stl_per_g INTEGER, 
        blk_per_g INTEGER, 
        tov_per_g INTEGER, 
        pf_per_g INTEGER, 
        pts_per_g INTEGER,
        player_pk INTEGER,
        FOREIGN KEY(player_pk) REFERENCES player(pk)
    );""")

    CON.commit()
    CUR.close()
    CON.close()

if __name__ == '__main__':
    run()