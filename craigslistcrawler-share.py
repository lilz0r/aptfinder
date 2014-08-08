#!/usr/bin/env python
# -*- coding: utf-8 -*-
from email.header    import Header
from email.mime.text import MIMEText
from getpass         import getpass
from smtplib         import SMTP_SSL

import urllib2, re, sys, os, getopt
from bs4 import BeautifulSoup

#send an email via gmail
def sendEmail(toSend, message, login, password):
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
	    print "sent email to: "+toSend 
	finally:
	    s.quit()

#scrapes page
def scrapePage(url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	return soup

#removes duplicates from a list
def removeduplicates(lst):
	lst = list(set(lst))
	return lst

#grabs stored links in a set from a specified temp file location
def grabstoredlinks(tempfile):
	storedlinks = [] #init and read from a file...
	k = 0

	fo = open(tempfile, 'w+')
	for line in fo.readlines():
		#print k
		k += 1
		if len(line) == 52:
			storedlinks.append(line[0:51])
	fo.close()
	return storedlinks

#gets all links from a craigslist url 
def getlinks(craigslisturl):
	mainsoup = scrapePage(craigslisturl)
	links = [ each.get('href') for each in mainsoup.findAll('a') ]
	return links

#stores new links to storedlinks
def storenewlinks(links, storedlinks):
	for link in links:
		if "html" in str(link):
			storedlinks.append(link)
	return storedlinks

#finds the email address of the ad given the url of the ad
def findemail(link):
	soup = scrapePage(link)
	emailarray = soup.findAll(text=re.compile("@"))
	#print "emailarray", emailarray
	if len(emailarray):
		text = str(emailarray[-1])
		if len(text) == 36:				
			email = text
			#print "email", email
			return email

#send emails to ads that you have not emailed before
def sendNewEmails(message, difflst, login, password):
	for link in difflst:
		#print "link: ", link
		email = findemail(link)
		#print "found an email! about to send to...", email
		if email:
			sendEmail(email, message, login, password) #replace with your own message

#gets the new list of urls for this run are from storedlinks
def getnewlst(storedlinks):
	newset = set(storedlinks)
	newlst = list(newset)
	return newlst

#use set difference to find what the new URLs to visit are.
def getdifflst(storedlinks, origstoredset):
	newset = set(storedlinks)
	diffset = newset.difference(origstoredset)
	difflst = list(diffset)
	return difflst

#set up, hardcoded info + cleanup
def main():
	filedir = "/Users/lily/Documents/workspace/"
	tempfile = filedir+'temp.txt'
	login, password = '', '' #sample test account for sending emails 
	storedlinks = grabstoredlinks(tempfile)
	origstoredset = set(storedlinks)
	craigslisturl = 'http://sfbay.craigslist.org/search/roo/sfc?query=&srchType=A&minAsk=600&maxAsk=1100&nh=1&nh=149&nh=4&nh=11&nh=10&nh=18&nh=21&nh=23'
	links = getlinks(craigslisturl)
	updatedstoredlinks = storenewlinks(links, storedlinks)
	newlst = getnewlst(updatedstoredlinks)
	difflst = getdifflst(updatedstoredlinks, origstoredset)
	message = "Hi! I'm interested in this apartment!"
	sendNewEmails(message, difflst, login, password)
	#now cleanup and overwrite tempfile
	os.remove(tempfile)
	j = 0
	fo = open(tempfile, 'wb+')
	for line in newlst:
		j += 1
		fo.write(line+'\n');
	fo.close()

if __name__ == "__main__":
   sys.exit(main())



