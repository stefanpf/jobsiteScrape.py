#! python3

# jobsiteScrape.py - scrapes a number of German job websites for
# placements,  selects the interesting ones based on some hard-coded
# criteria, and saves  the results in an easy to read spreadsheet.
#
# v0.3 - 2018-11-06

import os
import datetime
import time
import re
import requests
import bs4
import openpyxl

# Define functions.
#
# Site 1, berlinstartupjobs.com
#
# Currently scrapes links from the first page of categories passed as
# an argument.


def scrape_bsj(category):

    print("Scraping berlinstartupjobs.com/%s/ for links..." % category)
    res = requests.get('http://berlinstartupjobs.com/%s/' % category,
                       headers=header)
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

            res = requests.get(link_URL, headers=header)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features="lxml")

            title_elem = soup.select('.bsj-h1')[0].getText()
            job_title = job_title_regex.search(title_elem).group()
            company = company_regex.search(title_elem).group()
            job_desc = soup.select('.job-details')[0].getText()
            date_posted = soup.select('.product-listing-date')[0].getText()

            results[job_title] = {}
            results[job_title]['company'] = company
            results[job_title]['link'] = link_URL
            results[job_title]['desc'] = job_desc
            results[job_title]['date'] = date_posted

    print("Finished scraping berlinstartupjobs.com/%s/" % category)

    if results:
        print("Writing results to spreadsheet...")
        write_to_XLS(results)
    else:
        print("No results found.")


def scrape_stepstone(search_string):
    print("Scraping stepstone.de for links...")
    res = requests.get('http://www.stepstone.de/%s' % search_string,
                       headers=header)
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

            res = requests.get(link_URL, headers=header)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features="lxml")

            job_title = soup.select('.listing__job-title')[0].getText()
            company = soup.select('.listing__company-name')[0].getText().strip()
            job_desc = soup.select('.offer__content')[1].getText()
            date_posted = soup.select('.date-time-ago')[0].get('data-date')

            results[job_title] = {}
            results[job_title]['company'] = company
            results[job_title]['link'] = link_URL
            results[job_title]['desc'] = job_desc
            results[job_title]['date'] = date_posted

    print("Finished scraping stepstone.de")

    if results:
        print("Writing results to spreadsheet...")
        write_to_XLS(results)
    else:
        print("No results found.")


# Write results to a spreadsheet for easy digestion.
#
# Results should come as a nested dictionary like so:
# {<jobTitle> : {
#		<company> : value,
#		<desc> : value,
#		<link> : value,
#		<date> : value}}


def write_to_XLS(data_dictionary):

    try:
        wb = openpyxl.load_workbook('Results %s.xlsx'
                                    % datetime.datetime.today()
                                    .strftime('%Y-%m-%d'))
        sheet = wb.active
        print("Workbook opened.")

    except FileNotFoundError:
        print("Workbook not found, creating a new workbook...")
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.column_dimensions['A'].width = 30
        sheet.column_dimensions['B'].width = 30
        sheet.column_dimensions['C'].width = 20
        sheet.column_dimensions['D'].width = 30
        sheet.column_dimensions['E'].width = 30
        from openpyxl.styles import Font
        top_row_font_obj = Font(name='Arial', bold=True, size=12)
        sheet['A1'].font = top_row_font_obj
        sheet['B1'].font = top_row_font_obj
        sheet['C1'].font = top_row_font_obj
        sheet['D1'].font = top_row_font_obj
        sheet['E1'].font = top_row_font_obj
        sheet['A1'].value = "Job Title"
        sheet['B1'].value = "Company"
        sheet['C1'].value = "Date"
        sheet['D1'].value = "Description"
        sheet['E1'].value = "Link"
        wb.save('Results %s.xlsx'
                % datetime.datetime.today().strftime('%Y-%m-%d'))
        print("New workbook created.")
        wb = openpyxl.load_workbook('Results %s.xlsx'
                                    % datetime.datetime.today()
                                    .strftime('%Y-%m-%d'))
        sheet = wb.active
        print("Workbook opened.")

    row_num = 2
    for row in range(1, sheet.max_row):
        if sheet.cell(row=row, column=1):
            row_num += 1

    for key, value in data_dictionary.items():
        sheet.cell(row=row_num, column=1).value = key
        sheet.cell(row=row_num, column=2).value = value['company']
        sheet.cell(row=row_num, column=3).value = value['date']
        sheet.cell(row=row_num, column=4).value = value['desc']
        sheet.cell(row=row_num, column=5).value = value['link']
        row_num += 1

    wb.save('Results %s.xlsx' % datetime.datetime.today().strftime('%Y-%m-%d'))
    print("Workbook saved and closed.")

    return True

if __name__ == "__main__":

    # Start time to calculate and print elapsed time at the end
    start_run_time = time.time()

    # Make sure that our working directory is the directory
    # our .py file is located in:
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    os.chdir(directory_name)

    # Do run time logging.
    try:
        old_time_log = open('runlog.txt', 'r')
        content = old_time_log.readlines()
        old_time_log.close()
        last_line = content[len(content) - 1].rstrip()

        print("Script last ran at: " + last_line)

        old_time = datetime.datetime.strptime(last_line, '%Y-%m-%d %H:%M:%S')

    except FileNotFoundError:
        print("runlog.txt not found.\nHow many days back should I start scraping?")
        start_time_input = int(input())
        start_time = datetime.datetime.strptime(datetime.datetime.now()
                                                .strftime("%Y-%m-%d %H:%M:%S"),
                                                '%Y-%m-%d %H:%M:%S')
        old_time = (start_time - datetime.timedelta(days=start_time_input))

    current_time = datetime.datetime.now()
    new_time_log = open('runlog.txt', 'a')
    new_time_log.write(current_time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    new_time_log.close()

    # Define arguments and call scraping functions.
    header = {'User-Agent': 'Mozilla/5.0'}
    bsj_category = ['operations', 'engineering'] #, 'marketing', 'other']

    for i in range(len(bsj_category)):
        scrape_bsj(bsj_category[i])

    # This is a test string taken from the URL based on a number
    # of selected search criteria.
    stepstone_search_string = ("5/ergebnisliste.html"
                               "?ws=Berlin"
                               "&fu=6000000%2C1000000%2C7002000%2C7006000"
                               "&li=10&of=0" # no. of search results to display
                               "&fci=419239&an=facets&fu=7008000"
                               "&fid=7008000&fn=categories&fa=select")
    scrape_stepstone(stepstone_search_string)

    # Print elapsed time.
    elapsed_run_time = time.time() - start_run_time
    print("All done.\nTime elapsed: " + time.strftime("%H:%M:%S",
                                                      time
                                                      .gmtime(elapsed_run_time)
                                                      ))
