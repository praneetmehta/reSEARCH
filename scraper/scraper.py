from __future__ import division
import urllib2
import requests
from bs4 import BeautifulSoup as bs
import os
import sys
import time
import re
import random
reload(sys)
sys.setdefaultencoding('utf8')
error_count = 0
num = 0

class Writer:
	''' Class for creating a writer object to write the
		files in multiple forders regarding a research article'''
	def __init__(self, abs_id):
		global filenumber, num, skip, MAX, SHOW_COUNT
		self.filename = str(filenumber)+'.txt'
		self.folder = 'Unstructured_'
		filenumber += 1
		self.abs_id = abs_id+'.txt'
		status = int((num+1)/min(MAX-skip, SHOW_COUNT)*100)
		print('Writing file\t->\t{}\t{:02d}%\r'.format(self.abs_id, status)),
		num = num+1

	def write(self,folder, data):
		if not os.path.exists(folder):
		    try:
		        os.makedirs(folder)
		    except OSError as exc: #handle the overspeeding error
		        if exc.errno != errno.EEXIST:
		            raise	
		with open(os.path.join(folder, self.abs_id), 'w+') as file:
			file.write(data)
		sys.stdout.flush()

def writetofile(dom, prev_sibling, HEADERS):
	'''Function to create a writer object and invoke the write method
		to write the various files to their respective folders'''
	global URL, PARSER, REATTEMPTS, error_count
	try:
		title = dom.find('div',{'class':'list-title'}).text
		subject = dom.find('div', {'class':'list-subjects'}).text
		authors = dom.find('div',{'class':'list-authors'}).text
		abstract = dom.find('p',{'class':'mathjax'}).text
		abs_id = ('').join(prev_sibling.find('a',{'title':'Abstract'}).text.split('/')).replace('arXiv:','')
		link = urllib2.urlparse.urljoin(URL,prev_sibling.find_all('a')[2]['href'])
		downloadlink = dom.find('')
		W = Writer(abs_id)
		W.write(W.folder+'/title', title)
		W.write(W.folder+'/subject', subject)
		W.write(W.folder+'/authors', authors)
		W.write(W.folder+'/abstract', abstract)
		W.write(W.folder+'/link', link)
		del W
	except:
		title = dom.find('div',{'class':'list-title'}).text
		subject = dom.find('div', {'class':'list-subjects'}).text
		authors = dom.find('div',{'class':'list-authors'}).text
		href = urllib2.urlparse.urljoin(URL,prev_sibling.find('a',{'title':'Abstract'})['href'])
		abs_id = ('').join(prev_sibling.find('a',{'title':'Abstract'}).text.split('/')).replace('arXiv:','')
		link = urllib2.urlparse.urljoin(URL,prev_sibling.find_all('a')[2]['href'])
		try:
			abstract = bs(requests.get(href, headers = HEADERS).text, PARSER).find('blockquote', {'class':'abstract'}).text
			W = Writer(abs_id)
			W.write(W.folder+'/title', title)
			W.write(W.folder+'/subject', subject)
			W.write(W.folder+'/authors', authors)
			W.write(W.folder+'/abstract', abstract.replace('Abstract: ',''))
			W.write(W.folder+'/link', link)
			del W
			error_count = 0
		except KeyboardInterrupt:
			sys.exit()
		except:
			print 'skipping due to error.'
			error_count+=1
			if(error_count > 20):
				sys.exit()
	
def homepage(URL, PARSER):
	''' Gather the categories from the home page of the website
		arxive.org and also gather the forwarding links'''
	years = [year.zfill(2) for year in map(str, range(18))]
	years.reverse()
	months = [month.zfill(2) for month in map(str, range(1,13))]
	archive_links = []
	response = requests.get(URL).text
	soup = bs(response, PARSER)
	if('Access Denied' in response):
		print 'Access Denied'
		sys.exit()
	links = [link for link in soup.find_all('a') if 'list' in link['href'] if link.text == 'recent']
	for year in years:
		for month in months:
			for link in links:
				mod_link = link['href'].replace('recent',year+month)
				archive_links.append([urllib2.urlparse.urljoin(URL, mod_link), link.text])
	return archive_links

def pprint(item):
	''' Pretty print the html dom tree'''
	print item.prettify()

def pickproxy():
	'''Return random proxies to use'''
	proxies = ['http://199.15.198.7:8080','http://24.172.12.162:8080','http://216.100.88.228:8080']
	return random.choice(proxies)

def visitlink(link, rooturl):
	'''visit category links'''
	res = requests.get(link).text
	res_soup = bs(res, PARSER)
	content = res_soup.find('div', {'id':'content'}).find_all('ul')[-1].find_all('li')
	cat_links = []
	for item in content:
		try:
			cat_links.append(urllib2.urlparse.urljoin(rooturl, item.a['href']))
		except:
			pass
	return cat_links
	
def data_fetch(link, PARSER, HEADERS):
	'''Fetch the data from the page at the bottom of scraping tree'''
	temp = link
	temp = temp.split('/')
	response = requests.get(link, headers = HEADERS).text
	if('No listing' in response):
		print('No listing found for this period. Skipping....')
		return
	res_soup = bs(response, PARSER)
	for i,j in zip(res_soup.find_all('dd'), res_soup.find_all('dt')):
		writetofile(i,j, HEADERS)

if __name__ == '__main__':
	print 'Initializing...\r'
	filenumber = 10001
	SHOW_COUNT = 200
	REATTEMPTS = []
	URL = 'https://arxiv.org/'
	PARSER = 'html.parser'
	HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	archive_links = homepage(URL, PARSER)
	start = False
	skip = 0
	with open('status.txt', 'r') as file:
		text = file.read()
		donelink = text.split('\n')[0]
		if(len(text.split())<2):
			start = True
			skip = 0
		else:
			skip = int(text.split('\n')[-1])
	for link in archive_links:
		if (donelink.strip() == link[0].strip() and start == False):
			print('Partial Downloads Found. Resuming after ' + donelink +'\t -> skipping '+str(skip))
			start = True
			filenumber = int(text.split('\n')[1])

		if start == True:
			res = requests.get(link[0]).text
			MAX = int(bs(res, 'html.parser').find('small').find_all('a')[-1].text.split('-')[-1])
			temp_store = link[0].split('/')
			print 'Scraping for  '+temp_store[-2] + '->' + temp_store[-1][2:]+'/20'+temp_store[-1][:2]
			while(skip <= MAX):
				print 'Articles remaining on this page -> ' +str(MAX - skip) +'\n'
				print link[0]+'?skip='+str(skip)+'&show='+str(SHOW_COUNT)
				data_fetch(link[0]+'?skip='+str(skip)+'&show='+str(SHOW_COUNT), PARSER, HEADERS)
				num=0
				skip+=SHOW_COUNT
				with open('status.txt','w+') as file:
					print('Building checkpoint...\n\n')
					file.write(link[0] + '\n' + str(filenumber) + '\n' + str(skip))
					time.sleep(5)
			skip = 0
		
		
