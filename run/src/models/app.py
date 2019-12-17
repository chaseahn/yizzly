#!/usr/bin/env python3

import os


def DMMLogger(s):

    # isolate date,teams, type of clip, gameid, players involved, gametime
    # Period, Away score, home score, Description, 
    s = s.replace('\n',' ')
    print(type(s))
    print(s)
    return s