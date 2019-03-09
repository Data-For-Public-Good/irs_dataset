# Download and search on dictionaries


One of the things the data team is doing is checking the variables available in the datasets by year. We decided to work with the NCCS core files, which are separated in three groups (Public Charities, Private Foundations and Other organizations). Each of this three categories has a text file dictionary for every single year, from 1989 to 2013, which means a total of 75 files. With this amount, even the simpler tasks like downloading can become long, boring and overwhelming. 

## Downloading dictionaries

This is not the most efficient way, but here is how I did: I went to the [NCCS core data dictionary page](https://nccs-data.urban.org/showDD.php?ds=core) and copied one link of each group. After quickly checking that the link addresses were consistent, only changing the year number on the name file, I pasted each of the links and changed their year numbers, to have a list of all the links in [one file](download_links).


With the list of links, it was quite easy to download them all with a single command. In the command line (if you use Linux or Mac it should come installed on your bash. If you use windows, you need to [download and install](https://eternallybored.org/misc/wget/)). 

To download from a link in your command line, all you need to do is run `wget link`. In our case, since we want to download a list of links from a file, we need to add the argument "-i": `wget -i download_links`. Notice that this will download to your current directory. If you want to save it to another directory, you can do it adding `-P directory_path`. 

The process took 6 minutes in the wifi I was using, but at least it was processing time, not programmer time, and that is a trade that usually pays off.

## downloading everything with wget

After doing that way, I realized that I lost too much time in changing the files one by one. A better way to do it would be to simply download everything with wget, and deleting the files that don't matter for us

`wget -r -l 1 -nd https://nccs-data.urban.org/showDD.php?ds=core`

`-r` for recursive, means to download the address itself and the links on it. 
`-l` tells the number of levels, meaning links inside links inside links. In our case, we only want the links who are in the page itself, so we do `-l 1`
`-nd` as in "non directory", to save all the files in place and not as a structure of directories.
When I was about to try this option, I notice that the website was not responding, neither through terminal or through the browser. Need to test it later.

## Querying from dictionaries

Once you have all the dictionaries, it becomes easy to check for expressions in all of them.

Download the [script](search_script.sh) and save it on the same folder that you have your dictionaries

Now run in your command line `chmod u+x search_script.sh` to allow the file to be executable.

Now, to use the search script, run `bash search_script.sh EXPS` to search for the term EXPS (that is the variable name for total expenses) in all the file in the folder. Try it. To search other words, just substitute if for EXPS. If everything ran ok, you now should have a new folder named "queries" with a text file called "EXPS.txt" with the all the search results.

The explanation of the script is in the script file.
