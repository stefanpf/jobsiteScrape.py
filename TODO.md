TODO as of 2018-11-06:

NECESSARY:

- scrape_bsj(): scrape pages past the main category page (.../page/2/, .../page/3/). Could apply to other Wordpress based pages. Not sure how. Maybe a while loop over the pages and scraping all link elems that satisfy the time requirement and putting those into a list which can then be iterated over?

- write_to_XLS(): prettify output, especially column D. Deduplicate results.

- scrape_stepstone()

- scrape_indeed()

- scrape_monster()


NICE TO HAVE:

- Runtime logging: get rid of need for runlog.txt and store the runtime maybe in the respective .xlsx file.

- Add some more functions for repetitive tasks.

THINK ABOUT:

- argparse: not sure if this makes a lot sense for my personal use case.

- add abstraction layer for site parsers

- write to Google Docs to implement an API