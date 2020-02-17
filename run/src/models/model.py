#!/usr/bin/env python3

import sqlite3
import time
import jsonify

from datetime import datetime
from flask import session
from random import randint
from time import gmtime, strftime, sleep

from ..mappers.opencursor import OpenCursor
from ..extension.security import hasher

class User:
    def __init__(self, row={}, username='', password=''):
        if username:
            self.check_cred(username,password)
        else:
            self.row_set(row)

    def __enter__(self):
        return self

    def __exit__(self,exception_type,exception_value,exception_traceback):
        sleep(randint(10,10000)/10000)

    def row_set(self,row={}):
        row           = dict(row)
        self.pk       = row.get('pk')
        self.username = row.get('username')
        self.password = row.get('password')

    def create_user(self,username,password,email):
        #FIXME check this later with row set above
        self.username = username
        self.password = password
        self.email = email
        with OpenCursor() as cur:
            SQL = """ INSERT INTO user(
                username,password,email) VALUES (
                ?,?,?); """
            val = (self.username,self.password,self.email)
            cur.execute(SQL,val)
            print('user created')
    
    def login(self,password):
        with OpenCursor() as cur:
            cur.execute('SELECT password FROM user WHERE username=?;',(self.username,))
            if password == cur.fetchone()['password']:
                return True
            else:
                return False
    
    def check_cred(self,username,password):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM user WHERE
                  username=? and password=?; """
            val = (username,password)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            self.row_set(row)
        else:
            self.row_set({})

    def exists(self, username):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM user WHERE
                  username=?; """
            val = (username,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            return True
        else:
            return False


class Clips:

    def __init__(self, row={}, pk=''):
        if pk:
            self.check_for_clip(pk)
        else:
            self.row_set(row)
    
    def __bool__(self):
        return bool(self.pk)

    def __enter__(self):
        return self

    def __exit__(self,exception_type,exception_value,exception_traceback):
        sleep(randint(10,10000)/10000)

    def row_set(self,row={}):
        row = dict(row)
        self.pk = row.get('pk')
        self.game_id = row.get('game_id')
        self.home_team = row.get('home_team')
        self.away_team = row.get('away_team')
        self.game_date = row.get('game_date')
        self.rating = row.get('rating ')
        self.type = row.get('type')
        self.includes = row.get('includes')
        self.players = row.get('players')
        self.quarter = row.get('quarter')
        self.time = row.get('time')
        self.description = row.get('description')
    
    def save_clip(self, clip={}):
        print(clip)
        with OpenCursor() as cur:
            SQL = """ INSERT INTO clips(
                game_id,home_team,away_team,game_date,rating,type,
                includes,players,quarter,time,description) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?); """
            val = (
                clip['game_id'],
                clip['home_team'],
                clip['away_team'],
                clip['game_date'],
                clip['rating'],
                clip['type'],
                clip['includes'],
                clip['players'],
                clip['quarter'],
                clip['time'],
                clip['description']
                )
            cur.execute(SQL,val)
            print('clip saved')

    def check_for_clip(self,pk):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM clips WHERE
                  pk=?; """
            val = (pk,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            self.row_set(row)
        else:
            self.row_set({})
    
    def search_for(self,player_id,type,includes,rating):
        pass

class Players:

    def __init__(self, p_id='', row={}):
        if p_id:
            self.check_for_player(p_id)
        else:
            self.row_set(row)
    
    def __bool__(self):
        return bool(self.pk)

    def __enter__(self):
        return self

    def __exit__(self,exception_type,exception_value,exception_traceback):
        sleep(randint(10,10000)/10000)
    
    def row_set(self,row={}):
        row = dict(row)
        self.pk = row.get('pk')
        self.first_name = row.get('first_name')
        self.last_name = row.get('last_name')
        self.team_id = row.get('team_id')
        self.years_pro = row.get('years_pro')
        self.college_name = row.get('college_name')
        self.country = row.get('country')
        self.player_id = row.get('player_id')
        self.birth_date = row.get('birth_date')
        self.start_nba = row.get('start_nba')
        self.number = row.get('number')
        self.position = row.get('position')
        self.headshot = row.get('headshot')
        self.twitter = row.get('twitter')
    
    def check_for_player(self,p_id):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM players WHERE
                  player_id=?; """
            val = (p_id,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            self.row_set(row)
        else:
            self.row_set({})

    def add_player(self, clip={}):
        with OpenCursor() as cur:
            SQL = """ INSERT INTO players(
                first_name,last_name,team_id,years_pro,college_name,country,
                player_id,birth_date,start_nba,number,position,twitter,headshot
                ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?); """
            val = (
                clip['firstName'],
                clip['lastName'],
                clip['teamId'],
                clip['yearsPro'],
                clip['collegeName'],
                clip['country'],
                clip['playerId'],
                clip['dateOfBirth'],
                clip['startNba'],
                clip['leagues']['standard']['jersey'],
                clip['leagues']['standard']['pos'],
                clip['twitter'],
                clip['headshot']
                )
            cur.execute(SQL,val)

    def return_all_saved_player_ids(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM players; """
            cur.execute(SQL,)
            players = cur.fetchall()
        if players:
            id_list = []
            for player in players:
                id_list.append(player['player_id'])
            return id_list
        else:
            return []

    def remove_player(self, player_id):
        with OpenCursor() as cur:
            SQL = """ DELETE * FROM players WHERE
                  player_id=?; """
            val = (player_id,)
            cur.execute(SQL,val)
        print('deleted')
    
    def return_tracking_profiles(self):

        tracked_ids = self.return_all_saved_player_ids()
        player_list = []
        
        for num in tracked_ids:
            current_player = Players(p_id=num)
            profile = {
                'first_name': current_player.first_name,
                'last_name': current_player.last_name,
                'pos': current_player.position,
                'number': current_player.number,
                'team': current_player.team_id,
                'headshot': current_player.headshot,
                'twitter': current_player.twitter
            }
            player_list.append(profile)
        
        return player_list
 





    
    def get_all_tracked_teams(self):
        pass

    def get_last_nights_games(self, teams):
        #teams = self.get_all_tracked_teams
        #return ;ast night's games
        pass
    
    def get_player_stats(self, player_id):
        #return season avgs
        pass

    