TODO as of 2018-11-06:

NECESSARY:

- scrapeBsj(): scrape pages past the main category page (.../page/2/, .../page/3/). Could apply to other Wordpress based pages. Not sure how. Maybe a while loop over the pages and scraping all link elems that satisfy the time requirement and putting those into a list which can then be iterated over?

- writeToXls(): prettify output, especially column D. Deduplicate results.

- scrapeStepstone()

- scrapeIndeed()

- scrapeMonster()


NICE TO HAVE:

- Runtime logging: get rid of need for runlog.txt and store the runtime maybe in the respective .xlsx file.

THINK ABOUT:

- argparse: not sure if this makes a lot sense for my personal use case but could be useful for others.

- style: look into Python style guide for conventions

- add abstraction layer for site parsers

- write to Google Docs to implement an API