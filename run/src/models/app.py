#!/usr/bin/env python3

import os
import csv

from edl import Parser

def DMMLogger(s):

    # isolate date,teams, type of clip, gameid, players involved, gametime
    # Period, Away score, home score, Description, 
    s = s.replace('\n',' ')
    print(type(s))
    print(s)
    return s


class EDL():

    def __init__(self, path=path, name=name):
        self.path = path
        self.name = name

    def parser(self):
        events = []

        # Accepted framerates
        # 60, 59.94, 50, 30, 29.97, 25, 24, 23.98
        parser = Parser('59.94')

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

        try:
            with open(CSV_NAME, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in events:
                    writer.writerow(data)
        except IOError as e:
            print("I/O error: "+ str(e))    

            
    
    def execute(self):
        self.converter(self.parser())



if __name__ == "__main__":
    edl = EDL()
    edl.execute()
