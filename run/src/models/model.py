#!/usr/bin/env python3

import sqlite3
import time
import jsonify

from datetime import date
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
        self.position = row.get('position')
        self.headshot = row.get('headshot')
        self.twitter = row.get('twitter')
        self.current_team = row.get('current_team')
        self.age = row.get('age')
        self.weight = row.get('weight')
        self.height = row.get('height')
        self.jersey_num = row.get('jersey_num')
        self.pbr_link = row.get('pbr_link')
        self.user_pk = row.get('user_pk')
    
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

    def add_player(self, clip={}, user_pk=''):
        with OpenCursor() as cur:
            SQL = """ INSERT INTO players(
                first_name,last_name,team_id,years_pro,college_name,
                country,player_id,birth_date,start_nba,position,
                twitter,headshot,age, weight, height, current_team, 
                jersey_num, pbr_link, user_pk
                ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); """
            val = (
                clip['firstName'],
                clip['lastName'],
                clip['stats']['team_id'],
                clip['yearsPro'],
                clip['collegeName'],
                clip['country'],
                clip['playerId'],
                clip['dateOfBirth'],
                clip['startNba'],
                clip['stats']['pos'],
                clip['twitter'],
                clip['headshot'],
                clip['stats']['age'],
                clip['profile']['weight'],
                clip['profile']['height'],
                clip['profile']['current_team'],
                clip['profile']['jersey_number'],
                clip['pbr_link'],
                user_pk
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
            print(current_player.pk)
            current_season = Stats(current_player.pk)
            profile = {
                'first_name': current_player.first_name,
                'last_name': current_player.last_name,
                'pos': current_player.position,
                'number': current_player.jersey_num,
                'team': current_player.team_id,
                'headshot': current_player.headshot,
                'twitter': current_player.twitter,
                'pts': current_season.pts_per_g,
                'reb': current_season.trb_per_g,
                'ast': current_season.ast_per_g,
                'tpm': current_season.fg3_per_g,
                'stl': current_season.stl_per_g,
                'blk': current_season.blk_per_g
            }
            player_list.append(profile)


        
        return player_list
    
    def add_season_stats(self,player_id,clip={}):
        today = date.today()
        d = today.strftime("%m/%d/%y")
        p = self.access_player(player_id)
        print('Successfully accessed '+p.first_name)
        clip['player_pk'] = p.pk
        clip['date_recorded'] = d
        seed = Stats().add_player_season_stat(clip=clip)
        print('Successfully added '+p.first_name+' season stats.')

    def access_player(self, player_id):
        p = Players(p_id=player_id)
        return p

    def get_all_tracked_teams(self):
        pass

    def get_last_nights_games(self, teams):
        #teams = self.get_all_tracked_teams
        #return ;ast night's games
        pass
    
    def get_player_stats(self, player_id):
        #return season avgs
        pass


class Stats():

    def __init__(self,player_pk='',row={}):
        if player_pk:
            self.fetch_lastest_season_stats(player_pk)
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
        self.date_recorded = row.get('date_recorded')
        self.season = row.get('season')
        self.mp_per_g = row.get('mp_per_g')
        self.fg_per_g = row.get('fg_per_g')
        self.fga_per_g  = row.get('fga_per_g ')
        self.fg_pct = row.get('fg_pct')
        self.fg3_per_g = row.get('fg3_per_g')
        self.fg3a_per_g = row.get('fg3a_per_g')
        self.fg3_pct = row.get('fg3_pct')
        self.fg2_per_g = row.get('fg2_per_g')
        self.fg2a_per_g  = row.get('fg2a_per_g ')
        self.fg2_pct = row.get('fg2_pct')
        self.efg_pct = row.get('efg_pct')
        self.ft_per_g = row.get('ft_per_g')
        self.fta_per_g = row.get('fta_per_g')
        self.ft_pct = row.get('ft_pct')
        self.orb_per_g = row.get('orb_per_g')
        self.drb_per_g = row.get('drb_per_g')
        self.trb_per_g = row.get('trb_per_g')
        self.ast_per_g = row.get('ast_per_g')
        self.stl_per_g  = row.get('stl_per_g')
        self.blk_per_g = row.get('blk_per_g')
        self.tov_per_g = row.get('tov_per_g')
        self.pf_per_g = row.get('pf_per_g')
        self.pts_per_g = row.get('pts_per_g')
        self.player_pk = row.get('player_pk')
    
    def fetch_lastest_season_stats(self,player_pk):
        with OpenCursor() as cur:
            SQL = """SELECT * FROM stats WHERE player_pk=? 
            ORDER BY pk DESC LIMIT 1"""
            val = (player_pk,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            print('found player row')
            self.row_set(row)
        else:
            print('Nothing found')
            self.row_set({})

    
    def add_player_season_stat(self, clip={}):
        with OpenCursor() as cur:
            SQL = """ INSERT INTO stats(
                date_recorded,
                season,
                mp_per_g,
                fg_per_g,
                fga_per_g,
                fg_pct,
                fg3_per_g,
                fg3a_per_g,
                fg3_pct,
                fg2_per_g,
                fg2a_per_g,
                fg2_pct,
                efg_pct,
                ft_per_g,
                fta_per_g,
                ft_pct,
                orb_per_g,
                drb_per_g,
                trb_per_g,
                ast_per_g,
                stl_per_g,
                blk_per_g,
                tov_per_g,
                pf_per_g,
                pts_per_g,
                player_pk
                ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?); """
            val = (
                clip['date_recorded'],
                clip['season'],
                clip['mp_per_g'],
                clip['fg_per_g'],
                clip['fga_per_g'],
                clip['fg_pct'],
                clip['fg3_per_g'],
                clip['fg3a_per_g'],
                clip['fg3_pct'],
                clip['fg2_per_g'],
                clip['fg2a_per_g'],
                clip['fg2_pct'],
                clip['efg_pct'],
                clip['ft_per_g'],
                clip['fta_per_g'],
                clip['ft_pct'],
                clip['orb_per_g'],
                clip['drb_per_g'],
                clip['trb_per_g'],
                clip['ast_per_g'],
                clip['stl_per_g'],
                clip['blk_per_g'],
                clip['tov_per_g'],
                clip['pf_per_g'],
                clip['pts_per_g'],
                clip['player_pk']
                )
            cur.execute(SQL,val)