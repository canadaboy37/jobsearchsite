import abc
import urllib
from models.data_manager import dataMgr
from models.models import User, Job
from nltk import FreqDist
from nlp.bag_of_words import BagOfWords

class SiteCrawler(object):
	REQUEST_URL 		= 'RequestUrl'
	REQUEST_PARAMS 		= 'RequestParams'
	
	def __init__(self, numPostsPerRequest, maxPosts):
		self.numPostsPerRequest = numPostsPerRequest
		self.maxPosts = maxPosts
		
	@abc.abstractmethod
	def parsePostsResponse(self, html):
		return
	
	@abc.abstractmethod	
	def parsePost(self, post):
		return
	
	@abc.abstractmethod
	def buildRequest(self, startPostNum, endPostNum):
		return
		
	def newRequestObj(self):
		return {self.REQUEST_URL : None, self.REQUEST_PARAMS : None}
		
	def doHttpRequest(self, url):
		return urllib.urlopen(url).read()
		
	def doRequest(self, request):
		params = urllib.urlencode(request[self.REQUEST_PARAMS])
		url = request[self.REQUEST_URL]+ "?%s" % params
		return self.doHttpRequest(url)

	def retrievePosts(self, request):
		response = self.doRequest(request)
		# print response
		return self.parsePostsResponse(response)
		
	def processPosts(self, request):
		posts = self.retrievePosts(request)
		jobs = []
		
		for post in posts:
			# TODO skip over url's that have already been processed
			features = self.parsePost(post)
			# TODO save the parse output
			bagofwords = BagOfWords()
			freq = FreqDist(w.lower() for w in bagofwords.tokenize(features[features.POST_TEXT]))
			features[features.POST_FREQDIST] = dict(freq)
			print features
			# do not add duplicates!
			if not dataMgr.postExists(features[features.SITE_JOBSID]):
				jobs.append( 
					Job(
						features[features.SITE_JOBSID],
						features[features.POST_URL], 
						'TODO', 
						features[features.POSITION_TITLE],
						features[features.POST_TEXT],
						features
					)
				)
			else:
				print 'skipping %s' % features[features.POST_URL]
				
		# commit transaction
		dataMgr.add_all(jobs)
		dataMgr.commit()
		return jobs

	def start(self):
		for i in range(1, self.maxPosts, self.numPostsPerRequest):
			self.processPosts(self.buildRequest(self.newRequestObj(), i, self.numPostsPerRequest))

	def test(self):
		jobs = []
		for i in range(1, self.maxPosts, self.numPostsPerRequest):
			request = self.buildRequest(self.newRequestObj(), i, self.numPostsPerRequest)
			posts = self.retrievePosts(request)
			
			for post in posts:
				# TODO skip over url's that have already been processed
				features = self.parsePost(post)
				bagofwords = BagOfWords()
				features[self.POST_FREQDIST] = FreqDist(w.lower() for w in bagofwords.tokenize(features[self.POST_TEXT]))
				jobs.append(features)
		return jobs