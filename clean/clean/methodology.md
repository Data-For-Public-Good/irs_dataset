Methodology for cleaning IRS data

Files containing tax forms for nonprofits (990s) were downloaded for years 2005-2015 from https://nccs-data.urban.org/data.php?ds=core.
all_orgs.py and clean_orgs.py were run on the downloaded CSVs as follows:

- An argument for all_orgs is a 'master' directory that contains several subdirectories. clean_orgs.py is run on all subdirectories in the master directory. 
- To create one CSV for each year containing all organizations, subdirectories should contain the Public Charities, Private Foundations, and Other organizations CSVs for each year.

clean_orgs.py:

Argument: directory containing all CSVs to be aggregated

Result: CSV containing aggregated information from the argument directory
Pipeline:
- Read CSV into a pandas dataframe
- Isolated organizations in NYC using a list of zip codes
- Isolated organizations with subdisciplines we're interested in (list included in script)
- Retained columns to be used in mapping - in this case, columns relevant to the arts vibrancy index. Using information in the NCCS data dictionaries, we identified columns that encoded the same information in each large CSV. 
	- Columns used in vibrancy index:
	
			Contributed revenue
			Total revenue
			Expenses
			Compensation
		These columns, as well as descriptive information (EINs, addresses, names, subdisciplines, etc.) were isolated and moved to a new, smaller dataframe
- Added the 'names' of the organizations' subdisciplines (rather than codes) to the datagrame
- Removed apartment, suite, floor, or room numbers from organizations' addresses (to make geocoding possible)
- Created a 'full address' column: street address, city, state, and zip (to make geocoding possible)

This pipeline is run on each CSV in the directory and the resulting dataframes are appended together and saved to a new CSV.

all_orgs.py:

Argument: directory containing subdirectories on which clean_orgs.py should be run

Result: directory containing aggregated CSVs created by clean_orgs.py

- Uses subprocess to run clean_orgs.py on each subdirectory in the master directory indicated in the argument to the script.
