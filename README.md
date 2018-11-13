# jobsiteScrape.py
Scrapes a number of German job sites and dumps the scraped job offers into a XLSX spreadsheet.

It will:

* Log the time when it runs to a log file.
* Scrape job offers back until the time when it last ran. Alternatively, if there is no last run time logged, it will ask the user how many days back it should scrape.
* Scrape the following websites: berlinstartupjobs.com, stepstone.de
* Clean up scraped results where necessary (i.e. strip superfluous white space)
* Write the scraped results to an XLSX spreadsheet.
* Display the elapsed time.

## Installation and requirements

Install python modules:

    pip install -r requirements.txt

Choose what offers to scrape:

For *berlinstartupjobs.com*: 

In jobsiteScrape.py, add or subtract the categories you are interested in from line 130:

    bsj_categories = ['operations', 'engineering']

This will scrape the categories "Operations" and "IT".

For *stepstone.de*:

Go to stepstone.de, run a search and apply filters you are interested in. Then copy the search URL and add the parameters to the search string in jobsiteScrape.py, line 142:

    stepstone_search_string = ("5/ergebnisliste.html"
                                ...)

Note: you may want to leave out the "suid" (presumably search user ID) parameter.
