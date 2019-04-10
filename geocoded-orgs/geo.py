#!usr/bin/python3
'''
Accepts a CSV with a FULL_ADDRESSS column and geocodes each address, 
writing the result back to the same file

Sample use: python3 geo.py in_dir
'''

import geocoder
import pandas as pd
import numpy as np
from sys import argv
import os
import time

IN_FILE = argv[1]

def geocode(df):
    LAT = []
    LONG = []
    count = 0
    for address in df.FULL_ADDRESS:
        if pd.isnull(address):
            count += 1
            LAT.append(None)
            LONG.append(None)
            print(str(count) + '/' + str(len(df)) + " Org skipped - not valid address")
            continue
        g = geocoder.osm(address)
        if g.latlng == None:
            count += 1
            LAT.append(None)
            LONG.append(None)
            print(str(count) + '/' + str(len(df)) + " Org skipped - unable to geocode")
        else:
            count += 1
            LAT.append(g.latlng[0])
            LONG.append(g.latlng[1])
            print(str(count) + '/' + str(len(df)) + " Address geocoded")
        time.sleep(1) # For maximum of 1 request per second
    df['LAT'] = LAT
    df['LONG'] = LONG
    return df

df = pd.read_csv(IN_FILE)
df = geocode(df)
df.to_csv(IN_FILE)