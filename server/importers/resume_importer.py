import os
from nlp.bag_of_words import BagOfWords

ANTIWORD = '/usr/bin/antiword'

class ResumeImporterException(Exception):
	pass

class ResumeImporter:
	def __init__(self):
		self.bagofwords = BagOfWords()
		
	def importWordDoc(self, filepath):
		try:
			rawtext = os.popen("%s %s" % (ANTIWORD, filepath)).read()
			words = self.bagofwords.tokenize(rawtext)
			return (rawtext, words)
		except Exception, err:
			raise ResumeImporterException(err, 'Error importing word document: ')
			
def main():
	importer = ResumeImporter()
	print importer.importWordDoc('~/Dropbox/Employment/Robbi/RMcDonaldRes2008.doc')
	
if __name__ == '__main__':
	main()