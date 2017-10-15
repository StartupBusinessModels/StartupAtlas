#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from markdownify import markdownify as md

page = 'https://www.cleverism.com/company/skyhigh-networks/'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

req = urllib2.Request(page, headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, 'html.parser')

business_model = soup.find('div', attrs={'class': 'business-model'})

markdown = md(business_model).encode('utf-8').strip()

f = open("test", 'wb')
f.write(markdown)
f.close()
