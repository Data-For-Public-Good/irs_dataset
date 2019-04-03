#!usr/bin/python3

# Runs clean_orgs.py on each subdirectory in a specified directory and creates all resulting CSVs in out_dir

# Sample usage: python3 all_orgs.py in_dir out_dir

import os
import subprocess
from sys import argv

IN_DIR = argv[1]
OUT_DIR = argv[2]

for subdir in os.listdir(IN_DIR):
    subprocess.call(['python3', 'clean_orgs.py', IN_DIR+'/'+subdir, OUT_DIR+'/'+subdir+'.csv'])
    print("Processed directory " + subdir)
