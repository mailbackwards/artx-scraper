from urllib2 import urlopen
import re 

from bs4 import BeautifulSoup

BASE_URL = "http://brandeis.edu/rose"

def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    navLinks = [] 

    nav = soup.find('div', {'id': 'navSidebar'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list 
    for li in nav.findAll('li'): 
    	link = BASE_URL + "/" + li.a["href"] # exhibition link to be added 
    	if link not in navLinks: 
    		navLinks.append(link)  # add only if not already in list 
    return navLinks


# From exhibitions page, find all links for events and exhibitions
def get_link_events(link_url): 
	soup = make_soup(link_url)
	eventLinks = [] 
	URL = BASE_URL + '/onview/' 

	div = soup.find('div', {'id':'contentText'}) # find div to search  
	for tr in div.findAll('tr'): 
		link = URL + tr.a["href"] # link of exhibition
		if link not in eventLinks:
			eventLinks.append(link) # find all urls for events and exhibitions

	return eventLinks


# From exhibition links, get relevant title, dates, and information 
def get_event_info(event_url): 
	soup = make_soup(event_url) 

	content = soup.find('div', {'id': 'content'}) #General wrapper for all event details
	
	# GET NAME
	name = ""
	text = content.find('div', {'id': 'contentText'})
	for h2 in text.findAll('h2'):  # get exhibition title 
		string = h2.getText() 
		title = re.sub('(\xa0)*\n', ':', string) #remove whitespace and tabs 
		name += title.strip() 


	# GET DATES AND LOC
	date = ""
	loc = ""

	
	# GET EVENT DESCRIPTION 
	body = content.find('tbody') # To get text 
	text = "" # String to store all text for the exhibition 
	for tr in body.findAll('tr'): 
		text += tr.getText().strip() 

	
	# GET IMAGE 
	img = body.find('img')['src'] #Find image link 
	match = re.sub('../../','',img)
	imageURL = BASE_URL + '/' + match  # add all images associated with event/exhibition
	imageURL = imageURL.strip() 

	return name, date, loc, text, imageURL  


###############################
#### Get information from Peabody Essex Museum website  
#### More information can be added to the 'get_event_info' function to get Related Events, images, and more  
#### Currently, the information for each current exhibit includes its name, date, location, and text 

def scrape(): 
	allEvents = [] #Array for all dictionaries created 

	links = get_nav_links(BASE_URL) #get all navigation links from main page
	for link in links: 
		if re.match('(.*)onview/index', link, re.I): #find link for current exhibitions 
	 		exhibitions = get_link_events(link) #all exhibition links 


	for exh in exhibitions: 
		# For each distinctive exh: return dictionary with url, dates, description, image, and name labels
			#For each distinctive url: return dictionary with url, dates, description, image, and name labels
			info = {} 	
			name,date, loc, text,image = get_event_info(exh) # get info 
			info['url'] = exh; # add value for 'url' key 
			info['dates'] = date
			info['location'] = loc 
			info['description'] = text
			info['image'] = image
			info['name'] = name 
			allEvents.append(info)  

	return allEvents 


