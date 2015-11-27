import vim
import parser
import urllib2
from HTMLParser import HTMLParser
import xml.dom.minidom

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	
class DocumentLoader:
	def __init__(self, title):
		self.title = title;
	def loadDocument(self):
		attempts = 0
		url = "https://namu.wiki/raw/"+self.title
		while attempts < 3:
			try:
				req = urllib2.Request(url, headers=header)
				conn = urllib2.urlopen(req,timeout = 5)
				encoding = conn.headers.getparam('charset')
				self.encoding = encoding
				content = conn.read()
				self.raw = content
				break
			except urllib2.URLError as e:
				attempts += 1
	def getBody(self):
		return self.raw

def getUserInput():
	vim.command('call inputsave()')
	vim.command("let user_input = input('Enter Title: ')")
	vim.command('call inputrestore()')
	return vim.eval('user_input')

def main():
	title = getUserInput()
	dl = DocumentLoader(title)
	dl.loadDocument()
	f = dl.getBody()
	vim.command('tabnew namu') # create temp buffer(namu)
	vim.current.buffer.append(f.split("\n"))

main()

