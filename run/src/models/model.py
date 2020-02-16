#!/usr/bin/env python3

import sqlite3
import time

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

class Players:

    def __init__(self, p_id='', row={}):
        if p_id:
            self.check_for_player(pid)
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
        self.team_id = row.get('team_id ')
        self.years_pro = row.get('years_pro')
        self.college_name = row.get('college_name')
        self.country = row.get('country')
        self.player_id = row.get('player_id')
        self.birth_date = row.get('birth_date')
        self.start_nba = row.get('start_nba ')
        self.standard_number = row.get('standard_number')
        self.position = row.get('position')
    
    def check_for_player(self,p_id):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM clips WHERE
                  player_id=?; """
            val = (p_id,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            self.row_set(row)
        else:
            self.row_set({})

    #FIXME Save
    def save_player(self, clip={}):
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