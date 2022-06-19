import requests
import string
from bs4 import BeautifulSoup
import re
import os

def titletofn(x):
    """

    :param x: string, article name
    :return: string, filename with no extension
    """
    fn = x.strip()
    for p in string.punctuation:
        if p in fn:
            fn = fn.replace(p, '')
    fn = fn.replace(' ', '_')
    return fn


def scrapPage(year, pages, article_type: str):
    f"""

    :param year: int = Year to search articles for
    :param pages: int = Up to (and including) how many pages to scrape for
    :param article_type: str = What type of articles to search for. Check nature.com for types. 
    :return: Error if an error occurs. Saves all the articles of the article type and year to /year/Page_1, Page_2 etc 
    """
    url = f'https://www.nature.com/nature/articles?sort=PubDate&year={str(year)}'
    articles = 0
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    root_dir = os.getcwd()

    if not r.ok:  # Check if there articles that year
        return 'nature.com has no articles on that year. Exiting...'

    if not os.path.isdir(f'{root_dir}\{str(year)}'):   # Check if {year} folder exists, create if it doesn't
        os.mkdir(f'{root_dir}\{str(year)}')

    os.chdir(f'{root_dir}\{str(year)}')
    root_dir = os.getcwd()

    for p in range(1, pages + 1):
        url_page = f'{url}&page={p}'
        r = requests.get(url_page, headers={'Accept-Language': 'en-US,en;q=0.5'})

        if not r.ok:
            return '''
            Done. Saved {} articles from {} page(s).
            Look in {} for results
            '''.format(articles, p - 1, root_dir)

        os.chdir(root_dir)
        if not os.path.isdir(f'{root_dir}\Page_{str(p)}') : os.mkdir(f'{root_dir}\Page_{str(p)}')
        os.chdir(f'Page_{str(p)}')

        soupa = BeautifulSoup(r.content, 'html.parser').findAll(attrs={'data-test': 'article.type'})

        for i in soupa:
            if i.span.contents[0] == article_type:
                article_title = i.parent.parent.a.contents[0]
                link = 'https://www.nature.com{}'.format(i.parent.parent.a['href'])
                filename = f'{titletofn(article_title)}.txt'
                getArticle(link, filename)
                articles += 1

    return '''
    Done. Saved {} articles from {} page(s).
    Please look into {} for results
    '''.format(articles, p, root_dir)


def getArticle(link, filename):
    """

    :param link: a link to a nature.com article page
    :param filename: the filename.txt to save the article's body. Warning: will overwrite all content
    :return: 'Ok' when done, 'File already exists' if the filename exists
    """
    ra = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if os.path.exists(filename):
        return 'File already exists'
    fn = open(filename, mode='w+b')
    soupb = BeautifulSoup(ra.content, 'html.parser')
    soupc = soupb.findAll('div', {"class": re.compile(r'body')})
    for i in soupc:
        fn.write(bytes(str(i.get_text()), 'utf-8'))
    fn.close()
    return 'Ok'

print('Welcome to the Natural article scrapper.')
print('This script will search for articles in the nature.com website. Let us begin')
year = input('Year to search articles for in nature.com\n>')
pages = int(input('Result page to look up to (and including)\n>'))
type = input('Article type to search for\n>')


print(scrapPage(year, pages, type))