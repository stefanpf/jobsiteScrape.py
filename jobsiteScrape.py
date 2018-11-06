#! python3

# jobsiteScrape.py - scrapes a number of German job websites for placements, 
# selects the interesting ones based on some hard-coded criteria, and saves 
# the results in an easy to read spreadsheet.
# v0.2 - 2018-11-05


import os, datetime, time, requests, bs4, re, openpyxl

startRunTime = time.time()			# start time to calculate and print elapsed time at the end

# Step 0: Make sure that our working directory is the directory our .py file is located in:

absolutePath = os.path.abspath(__file__)
directoryName = os.path.dirname(absolutePath)
os.chdir(directoryName)

# Step 1, Logging: open runlog file and read last line to know when
# the script was last run. Capture the datetime when the program is run and store that
# in the runlog file.

# Step 1a: open the runlog file from the working directory and grab the last line to know when
# the script was last run. If there is  no log file, ask the user how many days back they 
# want to scrape and establish that as pseudo time of last run.
# There is currently no error handling for non-integer inputs in the except clause.
# The times currently do not take into account daylight savings time.

try:
	oldTimeLog = open('runlog.txt', 'r')
	content = oldTimeLog.readlines()
	oldTimeLog.close()
	lastLine = content[len(content) - 1].rstrip()

	print('Script last ran at: ' + lastLine)

	oldTime = datetime.datetime.strptime(lastLine, '%Y-%m-%d %H:%M:%S')

except FileNotFoundError:
	print('runlog.txt not found.\nHow many days back should I start scraping?')
	startTimeInput = int(input())
	startTime = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
	oldTime = (startTime - datetime.timedelta(days=startTimeInput))

# Step 1b: append the current time to the runlog file.

currentTime = datetime.datetime.now()
newTimeLog = open('runlog.txt', 'a')
newTimeLog.write(currentTime.strftime("%Y-%m-%d %H:%M:%S") + '\n')
newTimeLog.close()

# Step 2, Scraping: scrape various job websites for ads posted since the script last ran.
# Select by hard-coded criteria and save selected results to a dictionary.

header = {'User-Agent': 'Mozilla/5.0'}		# Header for requests.get

# Site 1, berlinstartupjobs.com
# Currently scrapes links from the first page of categories passed as an argument
# TODO: scrape links not only from first page but also from next page until timedelta <= 0

def scrapeBsj(category):

	print('Scraping berlinstartupjobs.com/%s/ for links...' % category)
	res = requests.get('http://berlinstartupjobs.com/%s/' % category, headers=header)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text, features="lxml")

	linkElems = soup.select('.product-listing-h2 a')
	postElems = soup.select('.product-listing-item')
	postDateElems = soup.select('.product-listing-date')

	results = {}

	for i in range(len(postElems)):

		postDate = datetime.datetime.strptime(postDateElems[i].getText(), '%B %d, %Y')
		
		if (postDate - oldTime) <= datetime.timedelta(seconds=0):
			continue

		else:

			linkUrl = linkElems[i].get('href')

			jobTitleRegex = re.compile(r'.+?(?=.\/\/.)')			# Regex to match the job title from the h1
			companyRegex = re.compile(r'(?<=.\/\/.).+')				# Regex to match the company name from the h1
			
			res = requests.get(linkUrl, headers=header)
			res.raise_for_status()

			soup = bs4.BeautifulSoup(res.text, features="lxml")

			titleElem = soup.select('.bsj-h1')[0].getText()
			jobTitle = jobTitleRegex.search(titleElem).group()
			company = companyRegex.search(titleElem).group()

			jobDesc = soup.select('.job-details')[0].getText()

			datePosted = soup.select('.product-listing-date')[0].getText()

			results[jobTitle] = {}
			results[jobTitle]['company'] = company
			results[jobTitle]['link'] = linkUrl
			results[jobTitle]['desc'] = jobDesc
			results[jobTitle]['date'] = datePosted

	print('Finished scraping berlinstartupjobs.com/%s/' % category)

	if results:
		print('Writing results to spreadsheet...')
		writeToXls(results)
	else:
		print('No results found.')

# TODO Site 2, stepstone.de

def scrapeStepstone():

# TODO Site 3, indeed.de

def scrapeIndeed():

# TODO Site 4, monster.de

def scrapeMonster():
	
# Step 3, Results: write results to a spreadsheet for easy digestion.
# Results should come as a nested dictionary like so:
# {<jobTitle> : {
#		<company> : value,
#		<desc> : value,
#		<link> : value,
#		<date> : value}}
# TODO: check for duplicates based on job title and company name
# TODO: prettify output, especially job description because holy info dump.

def writeToXls(dataDictionary):

	try:
		wb = openpyxl.load_workbook('Results %s.xlsx' % datetime.datetime.today().strftime('%Y-%m-%d'))
		sheet = wb.active
		print('Workbook opened.')

	except FileNotFoundError:
		print('Workbook not found, creating a new workbook...')
		wb = openpyxl.Workbook()
		sheet = wb.active
		sheet.column_dimensions['A'].width = 30
		sheet.column_dimensions['B'].width = 30
		sheet.column_dimensions['C'].width = 20
		sheet.column_dimensions['D'].width = 30
		sheet.column_dimensions['E'].width = 30
		from openpyxl.styles import Font
		topRowFontObj = Font(name='Arial', bold=True, size=12)
		sheet['A1'].font = topRowFontObj
		sheet['B1'].font = topRowFontObj
		sheet['C1'].font = topRowFontObj
		sheet['D1'].font = topRowFontObj
		sheet['E1'].font = topRowFontObj
		sheet['A1'].value = 'Job Title'
		sheet['B1'].value = 'Company'
		sheet['C1'].value = 'Date'
		sheet['D1'].value = 'Description'
		sheet['E1'].value = 'Link'
		wb.save('Results %s.xlsx' % datetime.datetime.today().strftime('%Y-%m-%d'))
		print('New workbook created.')
		wb = openpyxl.load_workbook('Results %s.xlsx' % datetime.datetime.today().strftime('%Y-%m-%d'))
		sheet = wb.active
		print('Workbook opened.')


	rowNum = 2

	for row in range(1, sheet.max_row):
		if sheet.cell(row=row, column=1):
			rowNum += 1

	for key, value in dataDictionary.items():
		sheet.cell(row=rowNum, column=1).value = key
		sheet.cell(row=rowNum, column=2).value = value['company']
		sheet.cell(row=rowNum, column=3).value = value['date']
		sheet.cell(row=rowNum, column=4).value = value['desc']
		sheet.cell(row=rowNum, column=5).value = value['link']
		rowNum += 1

	wb.save('Results %s.xlsx' % datetime.datetime.today().strftime('%Y-%m-%d'))
	print('Workbook saved and closed.')

	return True


# TODO: Step 4, Call the scraping functions.

bsjCategory = ['operations', 'engineering'] #, 'marketing', 'other']

for i in range(len(bsjCategory)):
	scrapeBsj(bsjCategory[i])

elapsedRunTime = time.time() - startRunTime

print('All done.\nTime elapsed: ' + time.strftime("%H:%M:%S", time.gmtime(elapsedRunTime)))