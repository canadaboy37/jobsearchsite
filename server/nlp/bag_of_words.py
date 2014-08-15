import nltk
		
class BagOfWords(object):
	def __init__(self):
		self.stopwords = nltk.corpus.stopwords.words('english')
		self.stemmer = nltk.PorterStemmer()
		self.segmenter = nltk.data.load('tokenizers/punkt/english.pickle')
		
	def is_number(self, token):
		try:
			float(token)
			return True
		except ValueError:
			return False
			
	def is_punctuation(self, token):
		return False  # TODO
			
	def isValidToken(self, token):
		if (token in self.stopwords):
			return False
		if self.is_number(token):
			return False
		if (len(token) < 2):
			return False
		return True
		
	def tokenize(self, rawtext, normalize=True):
		segments = self.segmenter.tokenize(rawtext)
		
		tokens = []
		for segment in segments:
			tokens += nltk.word_tokenize(segment)
			
		if (normalize):	
			tokens = [self.stemmer.stem(token) for token in tokens if self.isValidToken(token.lower())]
		return tokens