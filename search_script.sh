#!/bin/bash

# Don't forget to run the command in the line below, which allows the execution of script file

# chmod u+x search_script

mkdir -p queries
# mkdir creates a directory called "queries". The -p option avoids an error message if the directory already exists. This prevents errors when doing following searches.

grep -A 4 -B 4 "$1" --directories=skip * > queries/"$1".txt 

: '  
Let's go part by part:

`grep` searches for an expression and prints it.
`-A 4` and `-B 4` to print 4 lines before and 4 lines after the expression, in order to give us more context and details
`"EXPS"` is the expression we are looking for. That is the variable name for total expenses.

`*` is the location where to search. Means all files. `--directories=skip` is needed to ignore the subdirectories.

`>` tells it to write the results to a file to the following path

And now we have a new file with all the results, so we can check which datasets have that particular variable, and the details about it.

'
