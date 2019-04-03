#!/usr/bin/python3

"""
Cleaning script for IRS data

Accepts CSVs from a given directory and aggregates them into a new CSV 
containing all organizations in that year (PC, PF, and other)

Sample invocation: python3 clean_orgs.py directory-path destination.csv

"""

import os
import pandas as pd
from sys import argv
import geocoder

DIR_PATH = argv[1]
DEST_PATH = argv[2]

def get_ny(df):
    # Retain only organizations whose ZIP code is in NYC
    NYZIPS = [10453.0, 10457.0, 10460.0, 10458.0, 10467.0, 10468.0, 
              10451.0, 10452.0, 10456.0, 10454.0, 10455.0, 10459.0, 
              10474.0, 10463.0, 10471.0, 10466.0, 10469.0, 10470.0, 
              10475.0, 10461.0, 10462.0, 10464.0, 10465.0, 10472.0, 
              10473.0, 11212.0, 11213.0, 11216.0, 11233.0, 11238.0, 
              11209.0, 11214.0, 11228.0, 11204.0, 11218.0, 11219.0, 
              11230.0, 11234.0, 11236.0, 11239.0, 11223.0, 11224.0, 
              11229.0, 11235.0, 11201.0, 11205.0, 11215.0, 11217.0, 
              11231.0, 11203.0, 11210.0, 11225.0, 11226.0, 11207.0, 
              11208.0, 11211.0, 11222.0, 11220.0, 11232.0, 11206.0, 
              11221.0, 11237.0, 10026.0, 10027.0, 10030.0, 10037.0, 
              10039.0, 10001.0, 10011.0, 10018.0, 10019.0, 10020.0, 
              10036.0, 10029.0, 10035.0, 10010.0, 10016.0, 10017.0, 
              10022.0, 10012.0, 10013.0, 10014.0, 10004.0, 10005.0, 
              10006.0, 10007.0, 10038.0, 10280.0, 10002.0, 10003.0, 
              10009.0, 10021.0, 10028.0, 10044.0, 10065.0, 10075.0, 
              10128.0, 10023.0, 10024.0, 10025.0, 10031.0, 10032.0, 
              10033.0, 10034.0, 10040.0, 11361.0, 11362.0, 11363.0, 
              11364.0, 11354.0, 11355.0, 11356.0, 11357.0, 11358.0, 
              11359.0, 11360.0, 11365.0, 11366.0, 11367.0, 11412.0, 
              11423.0, 11432.0, 11433.0, 11434.0, 11435.0, 11436.0, 
              11101.0, 11102.0, 11103.0, 11104.0, 11105.0, 11106.0, 
              11374.0, 11375.0, 11379.0, 11385.0, 11691.0, 11692.0, 
              11693.0, 11694.0, 11695.0, 11697.0, 11004.0, 11005.0, 
              11411.0, 11413.0, 11422.0, 11426.0, 11427.0, 11428.0, 
              11429.0, 11414.0, 11415.0, 11416.0, 11417.0, 11418.0, 
              11419.0, 11420.0, 11421.0, 11368.0, 11369.0, 11370.0, 
              11372.0, 11373.0, 11377.0, 11378.0, 10302.0, 10303.0, 
              10310.0, 10306.0, 10307.0, 10308.0, 10309.0, 10312.0, 
              10301.0, 10304.0, 10305.0, 10314.0, 10119.0, 11249.0, 
              10008.0, 10279.0, 10271.0, 10041.0, 10163.0, 10107.0, 
              10108.0, 10113.0, 10123.0, 11351.0, 10115.0, 10276.0, 
              10150.0, 11439.0, 11451.0, 11202.0, 10170.0, 11424.0, 
              10185.0, 10122.0, 11690.0, 11242.0, 11352.0, 10116.0, 
              10167.0, 10282.0, 11247.0, 10278.0, 10121.0, 10155.0, 
              10168.0, 10281.0, 10118.0, 10110.0, 10158.0, 10159.0, 
              10165.0, 11241.0, 10156.0, 10178.0, 10120.0, 10105.0, 
              10104.0, 10175.0, 10101.0, 10153.0, 10268.0, 10173.0, 
              10111.0, 10311.0, 10166.0, 10069.0, 10272.0, 10112.0, 
              10176.0, 10162.0, 10174.0, 10177.0, 10151.0, 11430.0, 
              11386.0, 10106.0, 10169.0, 10154.0, 11109.0, 11380.0, 
              10129.0, 10103.0, 10045.0, 10171.0, 10286.0, 11371.0, 
              11120.0, 11431.0, 10274.0, 11243.0, 11240.0, 10015.0, 
              10048.0, 10249.0, 10285.0, 10152.0, 10270.0, 10102.0, 
              10043.0, 10172.0, 10109.0, 10081.0, 11252.0, 10055.0, 
              10313.0, 11251.0, 10125.0, 10133.0, 10117.0, 10138.0, 
              10164.0, 10292.0, 10260.0, 10072.0, 10080.0, 10179.0, 
              10130.0, 11381.0, 10114.0, 11245.0, 11256.0, 11425.0, 
              10046.0, 10199.0, 10021, 10065, 11219, 10022, 10003, 
              10028, 10122, 11217, 10459, 11435, 10281, 10034, 11102,
              10017, 11361, 10013, 10004, 10005, 10001, 10168, 10016, 
              11210, 10031, 11223, 10036, 10018, 11211, 10024, 10019, 
              10119, 11204, 10023, 10128, 11106, 11234, 11120, 11375, 
              10008, 10274, 11694, 10165, 10025, 11249, 10173, 10158, 
              10471, 10309, 10312, 11427, 10014, 10010, 11230, 10170, 
              11205, 11215, 10177, 11201, 10020, 11238, 11231, 10111, 
              10461, 10150, 10306, 11214, 10007, 11224, 10118, 10153, 
              10110, 10012, 10163, 11218, 11373, 10107, 11367, 11220, 
              10032, 10075, 10115, 11235, 10011, 11415, 10027, 10463, 
              10002, 10026, 11101, 10120, 10103, 10055, 10039, 10123, 
              10009, 11378, 11229, 10006, 10038, 10155, 11364, 11418, 
              10279, 10470, 10468, 11241, 10310, 10467, 11434, 11372, 
              10314, 10272, 10048, 10116, 11228, 10308, 10462, 10307, 
              10304, 11430, 11358, 11209, 11374, 11354, 11377, 11421, 
              10286, 11232, 11245, 10469, 10176, 11385, 10044]
    NYFIPS = [36005.0, 36047.0, 36061.0, 36081.0, 36085.0,
             36005, 36047, 36061, 36081, 36085,
             '36005', '36047', '36061', '36081', '36085']
    
    # Test that both ZIP and FIP are in NYC
    new_df = df[df.ZIP5.isin(NYZIPS) | df.FIPS.isin(NYFIPS)]
    return new_df

def get_arts(df):
    # Retain only the organizations whose NTEE primary purpose
    # or 'final' NTEE code is in the list used by DataArts
    codes = ['A01', 'A02', 'A03', 'A12', 'A25', 'A6E', 'A51', 'A20',
            'A23', 'A24', 'A25', 'A6E', 'A51', 'A20', 'A23', 'A24',
            'A26', 'A27', 'A40', 'A62', 'A63', 'A68', 'A6B', 'A6C',
            'A6A', 'A61', 'A69', 'A65', 'A50', 'A52', 'A54', 'A56',
            'A57', 'A60']
    
    new_df = df[df.NTEECC.isin(codes)]
    # CO files also have nteeFinal column, which we can also check.
    if 'nteeFinal' in df.columns:
        new_df = new_df[new_df.nteeFinal.isin(codes)]
    
    return new_df

def mapping_columns(df):
    # Retain only the columns to be used for mapping 
    
    desc = ['NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'ZIP5', 'EIN', 'FIPS', 'Level1', 'NTEECC', 'nteeFinal']
    cont = ['CONT', 'P1TCONT', 'p1tcont']
    exps = ['EXPS', 'P1TOTEXP', 'p1totexp']
    comp = ['COMPENS', 'OTHSAL', 'P1OFCOMP']
    rev = ['P1TOTREV', 'p1totrev', 'TOTREV']
    prev = ['PROGREV', 'DUES']
    pull_cols = desc + cont + exps + comp + rev + prev
    temp_df = df.filter(pull_cols)
    
    # Make master columns
    for curr in temp_df.columns:
        if curr in cont: temp_df['CONTRIBUTIONS'] = temp_df[curr]
        if curr in exps: temp_df['EXPENSES'] = temp_df[curr]
        if curr == 'P1OFCOMP': temp_df['COMPENSATION'] = temp_df[curr]
        if curr in ['COMPENS', 'OTHSAL']: temp_df['COMPENSATION'] = temp_df.COMPENS + temp_df.OTHSAL
        if curr in rev: temp_df['REVENUE'] = temp_df[curr]
        if curr in prev: 
            if 'DUES' in temp_df.columns: temp_df['PROGREVENUE'] = temp_df.PROGREV + temp_df.DUES
            else: temp_df['PROGREVENUE'] = temp_df.PROGREV
            
    keep_cols = desc + ['CONTRIBUTIONS', 'EXPENSES', 'COMPENSATION', 'REVENUE', 'PROGREVENUE']
    new_df = temp_df.filter(keep_cols)
    return new_df

def get_subdiscipline(df):
    d_dict = {'A01': 'Alliances & Advocacy', 
              'A02': 'Management & Technical Assistance', 
              'A03': 'Professional Societies & Associations', 
              'A12': 'Fund Raising & Fund Distribution', 
              'A25': 'Arts Education', 
              'A6E': 'Performing Arts Schools', 
              'A51': 'Art Museums', 
              'A20': 'Arts & Culture', 
              'A23': 'Cultural & Ethnic Awareness', 
              'A24': 'Folk Arts', 
              'A26': 'Arts & Humanities Councils & Agencies', 
              'A27': 'Community Celebrations', 
              'A40': 'Visual Arts', 
              'A62': 'Dance', 
              'A63': 'Ballet', 
              'A68': 'Music', 
              'A6B': 'Singing & Choral Groups', 
              'A6C': 'Bands & Ensembles', 
              'A6A': 'Opera', 
              'A61': 'Performing Arts Centers', 
              'A69': 'Symphony Orchestras', 
              'A65': 'Theater', 
              'A50': 'Museums', 
              'A52': "Children's Museums", 
              'A54': 'History Museums', 
              'A56': 'Natural History & Natural Science Museums', 
              'A57': 'Science & Technology Museums', 
              'A60': 'Performing Arts'}
    sub = []
    for item in df.NTEECC:
        sub.append(d_dict[item])

    df['SUBDISCIPLINE'] = sub
    return df

def strip_address(df):
    # Adds a new column to dataframe df containing the street address 
    # of the organization minus the suite, apartment, or floor number 
    # (basically, making the address geocodable). We'll check for PO 
    # boxes here too.
    
    stop = ['STE', 'SUITE', 'FLOOR', 'FLR', 'RM', 'ROOM', 'FL', 'APT', 'F']
    
    address = []
    for item in df.ADDRESS:
        curr_add = None
        if type(item) != str: curr_add = None
        elif "PO BOX" in item: curr_add = None
        else:
            parts = item.split()
            snip = len(parts)
            if (any(char.isdigit() for char in parts[-1]) and any(char.isalpha() for char in parts[-1])):
                # Anything like B11 or 11B
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
            if curr_add.strip() == '': curr_add = None
        address.append(curr_add)
    df['STREET_ADDRESS'] = address
    return df

def full_address(df):
    # Adds a new column to dataframe df containing the full address - returns None if any value is missing
    
    address = []
    add = list(df.STREET_ADDRESS)
    city = list(df.CITY)
    state = list(df.STATE)
    zip_code = list(df.ZIP)
    
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

def title_case_name(df):
    t_name = []
    conj = ['a', 'an', 'and', 'at', 'by', 'for',
            'from', 'in', 'of', 'on', 'the', 'to']
    # List of words which, when found in the middle
    # of an org's name, should be lowercased

    abbrev = ['co', 'corp', 'inc']
    # List of abbreviations that should be kept 
    # abbreviated and followed by a period

    expand = {'amer': 'American', 'assoc': 'Association', 
            'cncl': 'Council', 'ctr': 'Center', 
            'fnd': 'Foundation', 'inst': 'Institute', 
            'soc': 'Society'}
    # Dictionary of abbreviations we want to expand

    caps = ['llc', 'ny', 'nyc', 'us', 'usa']
    # List of abbreviations to keep capitalized

    for item in df.NAME:
        temp = item.lower().split()
        new = []
        for wd in temp:
            if wd in conj:
                new.append(wd)
                continue
            if wd in abbrev:
                new.append(wd.title() + '.')
                continue
            if wd in expand.keys():
                new.append(expand[wd])
                continue
            if wd in caps:
                new.append(wd.upper())
                continue
            new.append(wd.title())

        t_name.append(" ".join(new))

    df['TITLE_NAME'] = t_name
    return df

def main():

    ls = []
    for filename in os.listdir(DIR_PATH):
        ls.append(DIR_PATH + '/' + filename)

    done = pd.DataFrame()

    for f in ls:
    	df = pd.read_csv(f, encoding = 'iso-8859-1')
    	df = get_ny(df)
    	df = get_arts(df)
    	df = mapping_columns(df)
      df = get_subdiscipline(df)
    	df = strip_address(df)
    	df = full_address(df)

    	done = done.append(df)

    done.to_csv(DEST_PATH)

main()
