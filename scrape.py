import requests 
from bs4 import BeautifulSoup
import pprint # Combines and prints the pages

# Scrape data from two pages of the website HackerNews
res = requests.get('https://news.ycombinator.com/')  # HackerNews first page
res2 = requests.get('https://news.ycombinator.com/?p=2')  # HackerNews second page

soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.titleline>a') #Links of the first page
subtext = soup.select('.subtext')

links2 = soup2.select('.titleline>a') # Links of the second page
subtext2 = soup2.select('.subtext')

mega_links = links + links2  # Combine the two pages
mega_subtext = subtext + subtext2


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True) # Sort the stories by votes


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText() # Get title of the story
        href = item.get('href', None) # Get the link  of the story
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:            #Get stories with over 100 points                      
                hn.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(mega_links, mega_subtext)) # Print the two sorted pages with their titles, links and points

