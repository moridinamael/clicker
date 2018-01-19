# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 08:33:50 2018

@author: mfreeman
"""

# mattclicker.py

import datetime

lgmep_produced = 0.0  # liquid_golden_manna_experience_points
lgmep_clicked = 0.0


assetfile = open("assets.csv","r")
assetcontents = assetfile.readlines()
assetfile.close()
assetfile = open("assets.csv","a")

class meditation():
    def __init__(self, minutes, birthday=datetime.datetime.now()):
        if(type(birthday) == type("foo")):
            birthday = datetime.datetime.strptime(birthday.strip(),'%Y-%m-%d %H:%M:%S.%f')
        self._birthday = birthday
        self._minutes = float(minutes)
    def evaluate(self):
        return self._minutes*(datetime.datetime.now() - self._birthday).seconds

class pushups():
    def __init__(self, count,birthday=datetime.datetime.now()):
        if(type(birthday) == type("foo")):
            birthday = datetime.datetime.strptime(birthday.strip(),'%Y-%m-%d %H:%M:%S.%f')
        self._birthday = birthday
        self._count = float(count)
    def evaluate(self):
        return self._count*(datetime.datetime.now() - self._birthday).seconds

class athleanx():
    def __init__(self, count, birthday=datetime.datetime.now()):
        if(type(birthday) == type("foo")):
            birthday = datetime.datetime.strptime(birthday.strip(),'%Y-%m-%d %H:%M:%S.%f')
        self._birthday = birthday
        self._count = float(count)
    def evaluate(self):
        return self._count*(datetime.datetime.now() - self._birthday).seconds*100

def streak_check(assetlist,thiskey):
    past = []
    for asset in assetlist:
        if(asset.__class__.__name__ == thiskey):
            ay,am,ad = asset._birthday.year, asset._birthday.month, asset._birthday.day
            past.append([ay,am,ad])

    dt_past = []
    # turn into datetime
    for entry in past:
        dt_past.append(datetime.datetime(entry[0],entry[1],entry[2]))

    # remove duplicates
    past_cleaned = []
    for entry in dt_past:
        if(entry in past_cleaned):
            pass
        else:
            past_cleaned.append(entry)

    past_cleaned_sorted = sorted(past_cleaned)

    now = datetime.datetime.now()


    streak = look_back(now, past_cleaned_sorted) + 1
    return streak

def look_back(now,past,streak=0):
    for entry in past:
        if( (now-entry).days == 1):
            prior_day = entry
            streak += 1
            streak = look_back(prior_day,past,streak)
            break
    return streak


key = {"meditation":meditation,
       "pushups":pushups,
       "athleanx":athleanx}

assets = []
for line in assetcontents:
    a,b,c = line.split(",")
    assets.append(key[a.strip()](b,c))

while True:
    token = raw_input("What did you accomplish?")
    if(token == ''):
        lgmep_clicked += 1

    lgmep_produced = 0.0
    for asset in assets:
        value = asset.evaluate()
        lgmep_produced += value

    if(":" in token):
        a,b = token.split(":")
        if(a not in key):
            print "That is not a valid activity."
        else:
            streak = streak_check(assets,a)
            print streak, " day streak! Keep at it."
            new_asset = key[a](b)
            assets.append(new_asset)
            print >> assetfile, a,",",b,",",new_asset._birthday
    print lgmep_produced + lgmep_clicked #, assets

    if(token == "x"):
        break

assetfile.close()