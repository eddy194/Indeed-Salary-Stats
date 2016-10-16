from bs4 import BeautifulSoup
import urllib2
import math
import time

language = "Java"
city = "Liverpool"
address = "http://www.indeed.co.uk/jobs?q=" + language.replace(" ", "%20") + "&l=" + city + "&limit=100&jt=contract"
scores = []

def get_soup(link):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
	response = opener.open(link)
	page_source = response.read()
	soup = BeautifulSoup(page_source, 'html.parser')
	return soup

def get_number_of_pages(link):
	soup = get_soup(link)
	ads = soup.find("div", {"id": "searchCount"}).text.split(" ")[-1]
	i = 0
	print ads
	while i < int(ads):
		print i 
		time.sleep(3)
		extract_all_rates(get_soup(link + "&start=" + str(i)))
		i += 100

def extract_all_rates(soup):
	whitelist = set('1234567890 ')
	all_nobr = soup.select("td > nobr")
	for element in all_nobr:
 		if("day" in str(element).lower()):
 			answer = ''.join(filter(whitelist.__contains__, str(element.decode_contents(formatter="html"))))
 			numbers = answer.replace("  ", " ").split(" ")
			numbers = [i for i in numbers if i != '']
			numbers = [ int(x) for x in numbers ]
		 	scores.append(sum(numbers) / float(len(numbers)))

get_number_of_pages(address)

print "Median value for " + language + " in " + city + " is " + str(int(sum(scores) / float(len(scores))))
print "List of values: "
print scores
