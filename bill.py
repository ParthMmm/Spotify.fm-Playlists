from lxml import etree
from io import StringIO
import requests

page = requests.get('http://www.billboard.com/charts/hot-100')
html = etree.HTML(page.content)

parser = etree.HTMLParser()
tree = etree.parse(StringIO(str(etree.tostring(html))), parser)
root = tree.getroot()

billboard = []
for article in root.iter('article'):
    if ('data-songtitle' in article.attrib):
        currSong = article.attrib['data-songtitle']
        for item in article.iter('a'):
            if (('class' in item.attrib) and (item.attrib['class'] == 'chart-row__artist')):
                currArtist = item.text
                billboard.append((currSong.strip(), currArtist.strip()))
                break

for entry in billboard:
    print (entry)
