import requests
from bs4 import BeautifulSoup as bs
import re
import dateparser

headers={
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'DNT': '1',
}

url='https://finance.yahoo.com/topic/crypto'

page = requests.get(url, headers=headers)

soup=bs(page.content, 'lxml')

storyItems=soup.find_all('li', class_=re.compile('stream-item story-item *'))

for item in storyItems:
    itemData=dict()
    link=item.find('a')
    title=item.find('h3')
    footer=item.find('div', class_=re.compile('footer *'))

    if link is not None:
        itemData['href']=link.get('href')
    if title is not None:
        itemData['title']=title.get_text()
    if footer is not None:
        publisher=footer.find('div', class_=re.compile('publishing *'))
        if publisher is not None:
            source=publisher.get_text().split('•')
            itemData['source']=source[0].strip()
            itemData['date']=dateparser.parse(source[1]).strftime("%d/%m/%Y %H:%M:%S")
