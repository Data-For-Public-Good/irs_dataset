#!usr/bin/python3

# Accepts a .csv file (or list of files) and does the following:
# - Adds column STREET_ADDRESS, which attempts to remove apartment & suite numbers that will stop geocoding
# - Adds column FULL_ADDRESS to be sent to geocoder
# - Adds columns LAT and LONG with geographic coordinates
# - Writes new dataframe back to .csv of same name

# Sample invocation: python3 geocoding.py path/to/file1.csv path/to/file2.csv path/to/file3.csv

# **** Requires installation of python module geocoder, installable with pip. Documented at https://geocoder.readthedocs.io/

import geocoder
import pandas as pd
import os
from sys import argv

def strip_address(df):
    # Adds a new column to dataframe df containing the street address 
    # of the organization minus the suite, apartment, or floor number 
    # (basically, making the address geocodable). We'll check for PO 
    # boxes here too.
    
    stop = ['STE', 'SUITE', 'FLOOR', 'FLR', 'RM', 'ROOM', 'FL', 'APT', 'F']
    
    address = []
    for item in df.ADDRESS:
        curr_add = ''
        if type(item) != str: curr_add = None
        elif "PO BOX" in item: curr_add = None
        else:
            parts = item.split()
            snip = len(parts)
            if (any(char.isdigit() for char in parts[-1]) and any(char.isalpha() for char in parts[-1])):
                snip = len(parts) - 1
            if parts[-1].isdigit(): snip = len(parts) - 1
            for i in range(len(parts)):
                # We want to split everything AFTER an apartment abbreviation, and
                # check the previous token to see if it's a street abbreviation or
                # something like an apartment number (to catch both FL 9 and 9TH FL)
                if parts[i] in stop:
                    if any(char.isdigit() for char in parts[i-1]): 
                        snip = i-1
                    else: 
                        snip = i
            curr_add = " ".join(parts[:snip])
        address.append(curr_add)
    df['STREET_ADDRESS'] = address
    return df

def full_address(df):
    # Adds a new column to dataframe df containing the full address - returns None if any value is missing
    
    address = []
    add = df.STREET_ADDRESS
    city = df.CITY
    state = df.STATE
    zip_code = df.ZIP
    for i in range(len(add)):
        a = isinstance(add[i], str)
        b = isinstance(city[i], str)
        c = isinstance(state[i], str)
        d = isinstance(zip_code[i], str)
        if (a & b & c & d): 
            curr_address = " ".join([add[i], city[i], state[i], zip_code[i]])
        else: curr_address = None 
        address.append(curr_address)
        
    df['FULL_ADDRESS'] = address
    return df

def geocode_df(df):
    # Adds two new columns to dataframe df: latitude and longitude. Adds None if no address or if geocoding fails
    LAT = []
    LONG = []
    for address in df.FULL_ADDRESS:
        g = geocoder.osm(address)
        if g.latlng == None: 
            LAT.append(None)
            LONG.append(None)
        else:
            LAT.append(g.latlng[0])
            LONG.append(g.latlng[1])
    
    df['LAT'] = LAT
    df['LONG'] = LONG
    return df

IN_FILES = argv[1:]

for curr_file in IN_FILES:
	df = pd.read_csv(curr_file)
	strip_address(df)
	full_address(df)
	geocode_df(df)
	df.to_csv(curr_file)
