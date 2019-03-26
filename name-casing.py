#!usr.bin/python3

# Accepts a .csv file (or list of tiles) and does the following:
# - Adds column TITLE_NAME, which contains organizations' names
#   in title case with special cases addressed (special cases 
#   are outlined in function documentation and are easily edited)
# - Writes new dataframe back to .csv of same name

# Sample invocation: python3 name-casing.py path/to/file1.csv path/to/file2.csv path/to/file3.csv

import pandas as pd
from sys import argv

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

IN_FILES = argv[1:]
for curr_file in IN_FILES:
    df = pd.read_csv(curr_file)
    title_case_name(df)
    df.to_csv(curr_file)

