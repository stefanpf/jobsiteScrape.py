# -*- coding: utf-8 -*-

import requests
import datetime
import re
import bs4


def scrape_stepstone(search_string, old_time):
    print("Scraping stepstone.de for links...")
    res = requests.get('http://www.stepstone.de/%s' % search_string,
                       headers={'User-Agent': 'Mozilla/5.0'})
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features="lxml")

    link_elems = soup.select('.job-element__url')
    post_date_elems = soup.select('.date-time-ago')

    results = {}

    for i in range(len(link_elems)):

        post_date = datetime.datetime.strptime(post_date_elems[i]
                                               .get('data-date'),
                                               '%Y-%m-%d %H:%M:%S')

        if (post_date - old_time) <= datetime.timedelta(seconds=0):
            continue

        else:
            link_URL_regex = re.compile(r'.+?(?=\?)')
            link_URL = link_URL_regex.search(link_elems[i].get('href')).group()

            res = requests.get(link_URL, headers={'User-Agent': 'Mozilla/5.0'})
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features="lxml")

            job_title = soup.select('.listing__job-title')[0].getText()
            company = soup.select('.listing__company-name')[0].getText().strip()
            try:
                job_desc = soup.select('.offer__content')[1].getText().strip()
            except IndexError:
                job_desc = "IndexError"
                print('IndexError. Skipping job description.')
            date_posted = soup.select('.date-time-ago')[0].get('data-date')

            results[job_title] = {}
            results[job_title]['company'] = company
            results[job_title]['link'] = link_URL
            results[job_title]['desc'] = job_desc
            results[job_title]['date'] = date_posted

    print("Finished scraping stepstone.de")

    if results:
        print("Returning results...")
        return results
    else:
        print("No results found.")
        return None
