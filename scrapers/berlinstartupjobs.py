# -*- coding: utf-8 -*-

import requests
import datetime
import re
import bs4


def scrape_bsj(category, old_time):

    print("Scraping berlinstartupjobs.com/%s/ for links..." % category)
    res = requests.get('http://berlinstartupjobs.com/%s/' % category,
                       headers={'User-Agent': 'Mozilla/5.0'})
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features="lxml")

    link_elems = soup.select('.product-listing-h2 a')
    post_elems = soup.select('.product-listing-item')
    post_date_elems = soup.select('.product-listing-date')

    results = {}

    for i in range(len(post_elems)):

        post_date = datetime.datetime.strptime(post_date_elems[i].getText(),
                                               '%B %d, %Y')

        if (post_date - old_time) <= datetime.timedelta(seconds=0):
            continue

        else:

            link_URL = link_elems[i].get('href')

            # Regex to match the job title and company name from h1.
            job_title_regex = re.compile(r'.+?(?=.\/\/.)')
            company_regex = re.compile(r'(?<=.\/\/.).+')

            res = requests.get(link_URL, headers={'User-Agent': 'Mozilla/5.0'})
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features="lxml")

            title_elem = soup.select('.bsj-h1')[0].getText()
            job_title = job_title_regex.search(title_elem).group()
            company = company_regex.search(title_elem).group()
            job_desc = soup.select('.job-details')[0].getText().strip()
            date_posted = soup.select('.product-listing-date')[0].getText()

            results[job_title] = {}
            results[job_title]['company'] = company
            results[job_title]['link'] = link_URL
            results[job_title]['desc'] = job_desc
            results[job_title]['date'] = date_posted

    print("Finished scraping berlinstartupjobs.com/%s/" % category)

    if results:
        print("Returning results...")
        return results
    else:
        print("No results found.")
        return None
