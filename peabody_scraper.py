from urllib2 import urlopen
import re 

from bs4 import BeautifulSoup

BASE_URL = "http://www.pem.org"

def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'class': 'mainNav'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list 
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")]
    return navLinks

# From all navigation links, find all links for events and exhibitions
def get_link_events(link_url): 
	soup = make_soup(link_url)
	div = soup.find('div', {'class':'subNav'}) # find div to search  
	eventLinks = [BASE_URL + li.a["href"] for li in div.findAll("li")] # find all urls for events and exhibitions
	return eventLinks

# From current exhibitions page, find links for current exhibitions
def get_exhibitions(current_url): 
	soup = make_soup(current_url)
	content = soup.find('div', {'class': 'content'}) 
	exhLinks = [BASE_URL + dt.a["href"] for dt in content.findAll("dt")] #build array of exhibition links
	return exhLinks 

# From current exhibition links, get relevant title, dates, and information 
def get_event_info(event_url): 
	soup = make_soup(event_url) 
	feature = soup.find('div', {'class': 'feature_detail'}) #General wrapper for all event details
	info = feature.find('div', {'class': 'info'}) 
	exhTitle = info.find('h2').getText() # get exhibition title 

	exhDatesLoc = "" #String to store dates and location 
	for dates in feature.findAll('p', {'class':'dates'}): # iterate through tags to get dates and location
		exhDatesLoc += dates.getText() 

	text = "" # String to store all text for the exhibition 
	for p in feature.findAll('p', {'style':'text-align: justify;'}): 
		text += p.getText() 

	return exhTitle, exhDatesLoc, text  


###############################
#### Get information from Peabody Essex Museum website  
#### More information can be added to the 'get_event_info' function to get Related Events, images, and more  
#### Currently, the information for each current exhibit includes its name, date, location, and text 

def scrape(): 
	exhibitions = [] #list for event links, including upcoming, current, touring, etc. 
	eventInfo = {} #Dictionary stores ==> key (event/exhibition url): event/exhibition name, event date & loc, event descriptive text

	links = get_nav_links(BASE_URL) #get all navigation links from main page
	for link in links: 
		if re.match('(.*)exhibition', link, re.I): #find all links with exhibitions 
			exhibitions = get_link_events(link) #all exhibition links 

	for exh in exhibitions: 
		if re.match('(.*)current', exh, re.I): #find the link for current events (this can be changed for other desired links)
			currentExhUrl = exh # find current exhibitions link 

	currentExhs = get_exhibitions(currentExhUrl) # array of all current exhibition links 
	for link in currentExhs: 
		eventInfo[link] = get_event_info(link) # add all exhibition info to dictionary

	return eventInfo 
	
