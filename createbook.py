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


createbook('http://etc.usf.edu/lit2go/165/buttercup-gold-and-other-stories/')