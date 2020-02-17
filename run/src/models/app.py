#!/usr/bin/env python3

import os
import csv
import string
import requests
import json
import jsonify

from edl import Parser
from flask import current_app

from ..extension.security import *


class EDL():
    
    # App One: DML Model will parse an EDL file
    # Parser returns { events } and Converter returns a CSV
    # Execute() runs it in one motion

    def __init__(self, path='', name='', frame_rate=''):
        self.path = path
        self.name = name
        self.frame_rate = frame_rate
        self.upload_folder = current_app.config['UPLOAD_FOLDER']

    def parser(self):
        events = []

        # Accepted framerates
        # 60, 59.94, 50, 30, 29.97, 25, 24, 23.98
        parser = Parser(self.frame_rate)

        with open(self.path) as f:
            edl = parser.parse(f)
            for event in edl.events:

                clip = {
                    "event_number": str(event.num),
                    "clip_name": str(event.clip_name),
                    "start": str(event.rec_start_tc),
                    "end": str(event.rec_end_tc)
                }

                events.append(clip)

        return events

    def converter(self, events):

        csv_columns = events[0].keys()
        file_name = self.name.split('.')[0]+'.csv'
        print(self.upload_folder+file_name)

        try:
            with open(self.upload_folder+'/'+file_name, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in events:
                    writer.writerow(data)
        except IOError as e:
            print("I/O error: "+ str(e))    

    def execute(self):
        print("Converting User File")
        self.converter(self.parser())
        print("File Converted")
        #TODO delete the original file



class DMMLogger():

    def __init__(self, log_input=''):
        if log_input:
            self.log_input = ' '.join(log_input.split())
        return None
    
    def create_clip_object(self):
        
        # Sort Input from list to look for:
        # Home Team / Away Team / Final Score / Date / Game ID
        # Type of Play /  Players Tagged / Time of Play + H/A Score
        # Play Rating / Description

        input_list = self.log_input.split()

        game_info = input_list[:input_list.index("ID:")+2]
        clip_info = input_list[input_list.index("ID:")+2:]

        clip_object = {}
        if game_info[1] == 'Trail':
            i=1
        else:
            i = 0
        clip_object['description'] = None
        clip_object['away_team'] = game_info[1+i] 
        clip_object['home_team'] = game_info[4+i]
        clip_object['home_score'] = game_info[2+i]
        clip_object['away_score'] = game_info[5+i]
        clip_object['game_date'] = game_info[6+i]
        clip_object['game_id'] = game_info[game_info.index("ID:")+1]
        clip_object['clip_type'] = ' '.join(
            game_info[7:game_info.index("ID:")-1]
            )

        print(game_info)

        # account for missing Run Score or Empty Players
        #TODO account for no description
        for index in range(len(clip_info)-1):
            
            if clip_info[index] == "Players:":
                if clip_info[index+1] == "Game":
                    clip_object['players'] = None
                else:
                    clip_object['players'] = ' '.join(clip_info[index+1:clip_info.index("Time:")-1])
            elif clip_info[index] == "Time:":
                if clip_info[index+1] == "Run":
                    clip_object['time'] = "N/A"
                elif clip_info[index+1] == "Period:":
                    clip_object['time'] = "N/A"
                else:
                    clip_object['time'] = clip_info[index+1]
            elif clip_info[index] == "Period:":
                clip_object['period'] = clip_info[index+1]
            elif clip_info[index] == "Away":
                clip_object['away_run_score'] = clip_info[index+1]
            elif clip_info[index] == "Home":
                clip_object['home_run_score'] = clip_info[index+1]
            elif clip_info[index] == "Rating:":
                clip_object['rating'] = clip_info[index+1]
            elif clip_info[index] == "Description:":
                clip_object['description'] = ' '.join(clip_info[index+1:len(clip_info)])       
        
        return clip_object
    

class CueSheet():

    def __init__(self, user_input='', name=''):
        if user_input:
            clean_user_input = user_input.replace('\r','')
        self.name = name
        self.user_input = clean_user_input.split('\n')
        self.upload_folder = current_app.config['UPLOAD_FOLDER']


    def parse_input(self):

        cue_list = self.user_input
        track_list, events = [], []

        for index in range(len(cue_list)):

            if cue_list[index].isdigit():

                try:
                    current_index = cue_list.index(cue_list[index])
                    next_digit = str(int(cue_list[index])+1)
                    next_digit_index = cue_list.index(next_digit)
                    current_track = cue_list[current_index:next_digit_index]
                    track_list.append(current_track)

                except ValueError:

                    current_index = cue_list.index(cue_list[index])
                    last_track = cue_list[current_index:len(cue_list)-1]
                    track_list.append(last_track)

        for track in track_list:
            
            composer_index = track.index('Composer:')
            publisher_index = track.index('Publisher:')

            title = track[1]
            
            if track[3] == 'Composer:':
                timing = 0
            else:
                timing = track[composer_index+1]
            
            composers = track[composer_index+1:publisher_index]
            publishers = track[publisher_index+1:]

            track_info = {
                'title': title,
                'timing': timing, 
                'composers': ' '.join(composers),
                'publishers': ' '.join(publishers)
            }
            
            events.append(track_info)

        print(events)
        return events

    def convert_cues_to_csv(self):

        events = self.parse_input()
        csv_columns = events[0].keys()
        file_name = self.name+'.csv'

        try:
            with open(self.upload_folder+'/'+file_name, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in events:
                    writer.writerow(data)
        except IOError:
            print("I/O error") 

class NBAapi():

    def __init__(self):
        self.url = "https://api-nba-v1.p.rapidapi.com/"
        self.headers = {
            'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
            'x-rapidapi-key': NBA_API_KEY
            }
    
    def check_response_for_200(self, res):
        if res == 200:
            return True
        return False
    
    def find_matching_players(self, fname='', lname=''):
        # Request all players with matching input
        # Results can show more than one
        # No matches returns NONE
        if fname:
            player_url = self.url + f'players/firstName/{fname}'
            res = requests.request(
                "GET", player_url, headers=self.headers
                ).json()['api']
            if self.check_response_for_200(res['status']):
                if res['results']==0:
                    return [{}]
                elif res['results']==1:
                    print(res['players'])
                    return res['players']
                else:
                    #erase any bad match
                    #can return multiple of same name
                    for player in res['players']:
                        if player['lastName'] != lname:
                            res['players'].remove(player)
                    print(res['players'])
                    return res['players']
            else:
                print('404 Error: Something went wrong.')
        else:
            pass