#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os 
import re


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

page_url = 'https://www.cleverism.com/company/skyhigh-networks/'

def get_cleverism_urls():
	myfile = "myxml.xml"
	os.system("curl https://www.cleverism.com/company-sitemap.xml -o %s" % myfile)
	sitemap = open(myfile).read()
	sites = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', sitemap)
	refined_list = []
	for site in sites:
		if "</loc>" in site:
			refined_list.append(site.replace("</loc>", ""))
	os.system("rm %s" % myfile)
	return refined_list[1:] # first one is not valid

def get_markdown(page_url):
	req = urllib2.Request(page_url, headers=hdr)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page, 'html.parser')

	business_model = soup.find('div', attrs={'class': 'business-model'})
	if business_model is None:
		return None
	business_model_str = str(business_model).replace("<strong>", "").replace("</strong>", "")

	markdown = md(business_model_str).encode('utf-8').strip()
	return markdown

def write_to_file(markdown, file):
	f = open(file, 'wb')
	f.write(markdown)
	f.close()


urls = get_cleverism_urls()

for url in urls:
	company = url.rsplit('/', 2)[1]
	print company
	markdown = get_markdown(url)
	if markdown is None:
		continue
	write_to_file(markdown, "raw_markdowns/cleverism_raw/%s.md" % company)
