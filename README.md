A team Python project for a 2nd level module.

Authors: Nathan Blades, Angus Ireland, Masha Nedjakova

We analysed a dataset of GPS data collected from taxis in San Francisco.

"Specification.pdf" - A description of what we were asked to do

"Report.pdf" - What we accomplished

"Analysis-Report.pdf" - Our results

First navigate into "taxis"

There first must be a dataset in the datasets folder. By default the program will look for the '\_cabs.txt' file in 'cabspottingdata' folder.

But if the data was in a different folder you could provide a command line argument to change the folder. 

To run the program do

    python2 Main.py

Optionally you can add command line arguments, for example

    python2 Main.py -d cabspottingdata -f _cabs.txt

But the two arguments I provided are set to those values by default.

Once in our program:

You can use 'help' to see a list of all options.

'quit' to exit the program.

'dataset' to change the dataset (-d) value

'file' to change the file (-f) value

Before you can do anything else you must first 'load' the data. For the entire dataset of 536 cabs this can take a few minutes. Use a different file if this is a problem.

Instead of 'load' you can also do 'subseti\_ids' or 'subset\_startend' to load a subset of the file instead.

Here are three example subset commands.

subset\_startend 2008-06-04T19:00:00 2008-06-04T20:00:00

subset\_startend 2008-06-04T00:00:00 2008-06-08T13:00:00

subset\_ids abboip abcoij abdremlu

Once loaded, statistic <statistic> can be used to print out a statistic to the console.

generate <graph> can be used to draw a graph onto the Tkinter window.
