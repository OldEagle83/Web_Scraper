import requests
import json
from bs4 import BeautifulSoup

# Error message variable initialization
e_msg0 = 'Invalid quote resource!'
e_msg1 = 'Invalid movie page!'


def quoteContent(url):
    '''Accepts a url and returns the Quote content from the json body response. Returns an error message if there is none.'''
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    try:
        return r.json()['content']
    except:
        return e_msg0

def getTitleDesc(url):
    '''Accepts an imdb url and returns the title and description of a movie/series. Returns an error message if
    the website is not imdb, or no title/description could be found'''
    if 'imdb' not in url:
        return e_msg1
    dict = {}
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')

    title = soup.find('h1')
    description = soup.find('span', {'data-testid': 'plot-l'})
    try:
        dict["title"] = title.text
        dict["description"] = description.text
        return dict
    except:
        return e_msg1

def saveUrl(url):
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r.status_code == 200:
        content = r.content
        sfile = open('source.html', 'wb')
        sfile.write(content)
        sfile.close()
        return 'Content saved.'
    else:
        return f'The URL returned {r.status_code}'

url = input()
print(saveUrl(url))


#print(getTitleDesc(url))