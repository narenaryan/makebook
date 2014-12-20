import requests
from lxml import html
import webbrowser
import os

def createbook(url):
	res = requests.get(url)
	folder = url.split('/')[-2]
	if not os.path.exists(folder):
		os.makedirs(folder)
	tree  = html.fromstring(res.text)
	parts = tree.xpath('//dl/dt/a/@href')
	for i in parts:
		res = requests.get(i)
		tree  = html.fromstring(res.text)
		parturl = tree.xpath('//audio/source[@type="audio/mpeg"]/@src')
		for surl in parturl:
			with open('%s/%s'%(folder,surl.split('/')[-1]), 'wb') as handle:
				response = requests.get(surl, stream=True)
				for block in response.iter_content(1024):
					if not block:
						break
					handle.write(block)

	print 'Successfully downloaded all books into single folder'


res = requests.get('http://etc.usf.edu/lit2go/books/')
tree = html.fromstring(res.text)
books = [i.encode('utf-8') for i in tree.xpath('//figcaption[@class="title"]/a/text()')]
links = tree.xpath('//figcaption[@class="title"]/a/@href')

catalog = dict(zip(books,links))
numcatalog = enumerate(books,1)
chose = {}
print '\n@@@@@@@@@@ Select from the top audio books below @@@@@@@@@\n'

for i,j in numcatalog:
	print '%d) %s'%(i,j)
	chose[i] = catalog[j]

choice = int(raw_input('Select Book'))

print 'Your book started downloading.......'
createbook(chose[choice])