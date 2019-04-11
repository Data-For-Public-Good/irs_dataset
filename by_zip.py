#!usr/bin/python3

# Takes cleaned CSVs and creates a new CSV containing the following aggregated values per zip code:
# - Number of arts organizations in the zip code
# - Total revenue from these organizations
# - Total compensation
# - Total expenses
# - Total contributions
# - Total program revenue (only from public charities & other organizations)

# Argument: Directory containing CSVs to aggregate over

# Sample usage: $ python3 by_zip.py in_dir

import pandas as pd
import os
from sys import argv

IN_DIR = argv[1]

def aggregate(df):
    NYZIPS = [10001.0, 10002.0, 10003.0, 10004.0, 10005.0, 10006.0, 10007.0, 10009.0,
              10010.0, 10011.0, 10012.0, 10013.0, 10014.0, 10015.0, 10016.0, 10017.0,
              10018.0, 10019.0, 10020.0, 10021.0, 10022.0, 10023.0, 10024.0, 10025.0,
              10026.0, 10027.0, 10028.0, 10029.0, 10030.0, 10031.0, 10032.0, 10033.0,
              10034.0, 10035.0, 10036.0, 10037.0, 10038.0, 10039.0, 10040.0, 10041.0,
              10044.0, 10045.0, 10048.0, 10055.0, 10060.0, 10069.0, 10090.0, 10095.0,
              10098.0, 10099.0, 10103.0, 10104.0, 10105.0, 10106.0, 10107.0, 10110.0,
              10111.0, 10112.0, 10115.0, 10118.0, 10119.0, 10120.0, 10121.0, 10122.0,
              10123.0, 10128.0, 10151.0, 10152.0, 10153.0, 10154.0, 10155.0, 10158.0,
              10161.0, 10162.0, 10165.0, 10166.0, 10167.0, 10168.0, 10169.0, 10170.0,
              10171.0, 10172.0, 10173.0, 10174.0, 10175.0, 10176.0, 10177.0, 10178.0,
              10199.0, 10270.0, 10271.0, 10278.0, 10279.0, 10280.0, 10281.0, 10282.0,
              10301.0, 10302.0, 10303.0, 10304.0, 10305.0, 10306.0, 10307.0, 10308.0,
              10309.0, 10310.0, 10311.0, 10312.0, 10314.0, 10451.0, 10452.0, 10453.0,
              10454.0, 10455.0, 10456.0, 10457.0, 10458.0, 10459.0, 10460.0, 10461.0,
              10462.0, 10463.0, 10464.0, 10465.0, 10466.0, 10467.0, 10468.0, 10469.0,
              10470.0, 10471.0, 10472.0, 10473.0, 10474.0, 10475.0, 11004.0, 11101.0,
              11102.0, 11103.0, 11104.0, 11105.0, 11106.0, 11109.0, 11201.0, 11203.0,
              11204.0, 11205.0, 11206.0, 11207.0, 11208.0, 11209.0, 11210.0, 11211.0,
              11212.0, 11213.0, 11214.0, 11215.0, 11216.0, 11217.0, 11218.0, 11219.0,
              11220.0, 11221.0, 11222.0, 11223.0, 11224.0, 11225.0, 11226.0, 11228.0,
              11229.0, 11230.0, 11231.0, 11232.0, 11233.0, 11234.0, 11235.0, 11236.0,
              11237.0, 11238.0, 11239.0, 11241.0, 11242.0, 11243.0, 11249.0, 11252.0,
              11256.0, 11351.0, 11354.0, 11355.0, 11356.0, 11357.0, 11358.0, 11359.0,
              11360.0, 11361.0, 11362.0, 11363.0, 11364.0, 11365.0, 11366.0, 11367.0,
              11368.0, 11369.0, 11370.0, 11371.0, 11372.0, 11373.0, 11374.0, 11375.0,
              11377.0, 11378.0, 11379.0, 11385.0, 11411.0, 11412.0, 11413.0, 11414.0,
              11415.0, 11416.0, 11417.0, 11418.0, 11419.0, 11420.0, 11421.0, 11422.0,
              11423.0, 11426.0, 11427.0, 11428.0, 11429.0, 11430.0, 11432.0, 11433.0,
              11434.0, 11435.0, 11436.0, 11691.0, 11692.0, 11693.0, 11694.0, 11697.0,
              10008.0, 10101.0, 10108.0, 10113.0, 10116.0, 10125.0, 10129.0, 10150.0,
              10156.0, 10159.0, 10163.0, 10185.0, 10272.0, 10276.0, 11202.0, 11242.0,
              11243.0, 11245.0, 11247.0, 11352.0, 11424.0, 11439.0, 11695.0, 10065.0, 
              10075.0, 10286.0, 11005.0]
    total = pd.DataFrame(columns = ['ZIP', 'LEN', 'REVENUE', 'COMPENSATION', 'EXPENSES', 'CONTRIBUTIONS', 'PROGREVENUE'])
    for zipcode in NYZIPS:
    	subdf = df.loc[df['ZIP5'] == zipcode]
    	length = len(subdf)
    	revenue = subdf.REVENUE.sum()
    	compensation = subdf.COMPENSATION.sum()
    	expenses = subdf.EXPENSES.sum()
    	contributions = subdf.CONTRIBUTIONS.sum()
    	progrevenue = subdf.PROGREVENUE.sum()
    	total = total.append({'ZIP': zipcode, 'LEN': length, 'REVENUE': revenue, 'COMPENSATION': compensation, 
                			  'EXPENSES': expenses, 'CONTRIBUTIONS': contributions, 'PROGREVENUE': progrevenue}, ignore_index = True)
    return total

def main():
    fnames = []
    for f in os.listdir(IN_DIR):
        fnames.append(IN_DIR + '/' + f)
        
    for csv in fnames:
        df = pd.read_csv(csv)
        print("Read file " + csv)
        agg = aggregate(df)
        agg.to_csv(csv[:-3]+'by_zip.csv')
        print("Created file " + csv[:-3] + 'by_zip.csv')

main()
