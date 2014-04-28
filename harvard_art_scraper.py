from urllib2 import urlopen
import re 
from bs4 import BeautifulSoup

BASE_URL = "http://www.harvardartmuseums.org"


def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'id': 'main-menu'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list 
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")]
    return navLinks

# From all navigation links, find all links for events and exhibitions
def get_link_events(link_url): 
	soup = make_soup(link_url)
	eventLinks = []
	content = soup.find('section', {'id':'section-content'}) # Find where event links are stored
	for field in content.findAll('div', {'class':'field-item even'}):  # find div to search  
		if field.find("a"): 
			eventURL = BASE_URL + field.a["href"] 
			if re.match('^/', field.a["href"]) and (eventURL not in eventLinks): # Sort out the non-event links 
				eventLinks.append(eventURL)# add only the event links 
	
	return eventLinks

# From current exhibition links, get relevant title, dates, and information 
def get_event_info(event_url): 
	soup = make_soup(event_url) 
	section = soup.find('section', {'id': 'section-content'}) #General wrapper for all event details
	
	info = "" #String to store all info 

	for item in section.findAll('div', {'class': 'field-item even'}): 
		info += item.getText()

	return info 



###############################
#### Get events information from Harvard Art Museums website 
#### Currently, all information for the event is captured 

def scrape(): 
	eventInfo = {} #Dictionary stores ==> key (event url): event name, event date & loc, event descriptive text

	links = get_nav_links(BASE_URL) #get all navigation links from main page

	for link in links: 
		if re.match('(.*)calendar', link, re.I): #find the calendar link 
			events = get_link_events(link) #all exhibition links 

	for event in events: 
	 	eventInfo[event] = get_event_info(event) # add all exhibition info to dictionary

	return eventInfo 
	
