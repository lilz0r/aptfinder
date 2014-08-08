#!/usr/bin/env python
# -*- coding: utf-8 -*-
from email.header    import Header
from email.mime.text import MIMEText
from getpass         import getpass
from smtplib         import SMTP_SSL


import urllib2, re, sys
from bs4 import BeautifulSoup

def sendEmail(toSend, message):
	#login, password = 'thelilz0r@gmail.com', getpass('Gmail password:')
	login, password = 'YOUREMAIL@gmail.com', 'PASSWORDGOESHERE'

	# create message
	msg = MIMEText(message, _charset='utf-8')
	msg['Subject'] = Header('Craigslist Apt Ad', 'utf-8')
	msg['From'] = login
	msg['To'] = toSend

	# send it via gmail
	s = SMTP_SSL('smtp.gmail.com', 465, timeout=10)
	s.set_debuglevel(0)
	try:
	    s.login(login, password)
	    s.sendmail(msg['From'], msg['To'], msg.as_string())
	finally:
	    s.quit()

# Testing:
#sendEmail('tim108@gmail.com', "HEY")


def scrapePage(url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	return soup


def removeduplicates(lst):
	lst = list(set(lst))
	return lst


storedlinks = [] #init and read from a file...

import os
k = 0

#CHANGE THIS DOCUMENT TO YOUR OWN THING
fo = open('/Users/lily/Documents/workspace/foo.txt', 'r')
for line in fo.readlines():
	#print k
	k += 1
	if len(line) == 52:
		storedlinks.append(line[0:51])
fo.close()

origset = set(storedlinks)


mainsoup = scrapePage('http://sfbay.craigslist.org/search/roo/sfc?query=&srchType=A&minAsk=600&maxAsk=1100&nh=1&nh=149&nh=4&nh=11&nh=10&nh=18&nh=21&nh=23')

links = [ each.get('href') for each in mainsoup.findAll('a') ]

#berksoup = scrapePage('http://sfbay.craigslist.org/search/roo?query=berkeley&srchType=A&minAsk=400&maxAsk=800')

eastbaysoup = scrapePage('http://sfbay.craigslist.org/search/roo/eby?maxAsk=800&minAsk=400&srchType=A')

#blinks = [ each.get('href') for each in berksoup.findAll('a') ]

elinks = [ each.get('href') for each in eastbaysoup.findAll('a') ]

for link in elinks:
	links.append(link)




#print links


#returnemail = [ eachone.get() for eachone in [ each.get('class') for each in mainsoup.findAll('span') ] ]
#problem... it keeps visiting craiglist pages it's visited before. maybe I need to strip the strings? maybe 
#I need to print everything it's drawing out from the links AND foo.txt?

def findemail(link):
	soup = scrapePage(link)
	print "visited new craigslist page"
	emailarray = soup.findAll(text=re.compile("@"))
	if len(emailarray):
		text = str(emailarray[0])
		if len(text) == 36:				
			email = text
			return email

for link in links:
	if "html" in str(link):
		storedlinks.append(link)

print len(storedlinks)

newset = set(storedlinks)

newlst = list(newset)

print len(newlst)

diffset = newset.difference(origset)

difflst = list(diffset)

print "difflst: ", difflst
#now visit difflst and go email them


for link in difflst:
	email = findemail(link)
	if email:
		sendEmail(email, "MESSAGE GOES HERE")
		print "email!"

os.remove('/Users/lily/Documents/workspace/foo.txt')

j = 0

fo = open('/Users/lily/Documents/workspace/foo.txt', 'wb+')
for line in newlst:
	#print j
	j += 1
	fo.write(line+'\n');
fo.close()

