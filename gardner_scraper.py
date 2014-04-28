from urllib2 import urlopen
import re 

from bs4 import BeautifulSoup

def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'id': 'nav'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list 
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")]
    return navLinks

# From all navigation links, find current events and exhibitions
def get_link_events(link_url): 
	soup = make_soup(link_url)
	events = []
	content = soup.find('div', {'id':'content'}) # find content to search  
	for s in content.findAll('span'): # find tags for current works 
		if not (s and s.string): 
			continue 
		if s.string == 'Current Exhibitions': #find all current exhibitions, disregard past
			currentEvents = soup.find('ul', {'class': 'subnav_ul divided'}) #get current events links
			eventLinks = [BASE_URL+ li.a["href"] for li in currentEvents.findAll("li")] 
			events = events + eventLinks 
	return events  	

# From current exhibition links, get relevant dates and information
def get_event_info(event_url): 
	soup = make_soup(event_url) 
	content = soup.find('div', {'id':'content'}) # find content tag 
	h1 = content.find('h1') # find title tag 
	# em = h1.find('em')
	exhName = h1.text # save exhibition name 

	date = content.find('h4') #find date by this tag 
	if not date: #otherwise, search for a different tag 
		p = content.find('p', {'class': 'image_details'}) 
		date =  p.find('strong')
		if not date: # no date found
			date = "" 
	
	exhDateLoc = date.text; # save dates and gallery location

	return (exhName, exhDateLoc) 

# From event pages, get all descriptions/text 
def get_event_text(event_url): 
	soup = make_soup(event_url)
	div = soup.find('div', {'class': 'tab'}) # find div for paragraphs 
	text = ""
	for p in div.findAll('p'): 
		text += p.getText() + '\n' # add paragraph texts to empty string 
	return text 


## Get information from Isabella Gardner Museum website ## 
def scrape(): 
	BASE_URL = "http://www.gardnermuseum.org"
	currentExhibitions = [] #list for event links
	eventInfo = {} #Dictionary stores ==> key (event/exhibition url): event/exhibition name, event date & loc, event descriptive text

	links = get_nav_links(BASE_URL) #get all navigation links from main page
	for link in links: 
		if re.match('(.*)exhibition', link, re.I): #find all links with exhibitions 
			currentExhibitions.append(get_link_events(link)) #all current event links 

	currentExhibitions = currentExhibitions[1:] # get rid of first in list, which is None

	for exhList in currentExhibitions: #iterate through to get to each exhibition link
		for exh in exhList: 
			eventInfo[exh] = get_event_info(exh), get_event_text(exh) # add information to dict with corresponding link

	return eventInfo 
