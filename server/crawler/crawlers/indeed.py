import json
import urllib
from site_crawler import SiteCrawler
from models.models import JobFeatures
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString, Comment

class IndeedCrawler(SiteCrawler):

	NUM_POSTS_PER_REQUEST = 100
	MAX_POSTS = 1000
	API_KEY = '1024522962966371'
	API_ROOT = 'http://api.indeed.com/ads/apisearch'
	USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
	
	def __init__(self):
		super(IndeedCrawler, self).__init__(self.NUM_POSTS_PER_REQUEST, self.MAX_POSTS)

	def fetch_body(self, div):
		body = ''
		for tag in div.contents:
			if tag.__class__ == NavigableString:
				body += tag.string.strip() + ' '
			elif tag.__class__ == Comment:
				return body
			else:
				body += self.fetch_body(tag)
		return body

	def retrievePostText(self, url):
		mUrl = url.replace("http://ca.indeed.com/", "http://ca.indeed.com/m/")
		html = self.doHttpRequest(mUrl)
		# description is located within <div id='desc'>
		soup = BeautifulSoup(html)		
		div = soup.first('div', {'id' : 'desc'})
		return self.fetch_body(div)

	def buildRequest(self, startPostNum, endPostNum):
		request = self.newRequestObj()
		params = dict()
		params['publisher'] = self.API_KEY	# Publisher ID
		params['v'] = '2'					# API Version
		params['userip'] = '127.0.0.1'		# The IP number of the end-user to whom the job results will be displayed.
		params['useragent'] = self.USER_AGENT # The User-Agent of the end-user to whom the job results will be displayed
		params['limit'] = str(self.NUM_POSTS_PER_REQUEST) # Maximum number of results returned per query
		# params['q'] = 'thermal'			# HACK to test matching for Robbi's resume
		params['l'] = 'Toronto'				# Search location: postal code or a "city, state/province/region" combination.
		params['jt'] = 'fulltime'			# Currently only supporting fulltime positions
		params['fromage'] = '1'				# Only search for postings for the past day
		params['latlong'] = '1'				# returns latitude and longitude information for each job result
		params['co'] = 'ca'					# Search within country specified
		params['format'] = 'json'			# Response string format:  "xml" or "json."
		params['sort'] = 'date'				# Sort by relevance or date.
		params['start'] = str(startPostNum)	# Start results at this result number, beginning with 0
		
		request[SiteCrawler.REQUEST_URL] = self.API_ROOT
		request[SiteCrawler.REQUEST_PARAMS] = params
		return request
	
	def parsePostsResponse(self, response):
		resObj = json.loads(response)
		return resObj['results']

	def parsePost(self, post):
		features = JobFeatures()
		
		print '-' * 10
		print post
		print '-' * 10
		
		if post['expired']: return None
		
		features[features.COMPANY_NAME] = post['company'].encode('ascii', 'xmlcharrefreplace')
		features[features.POSITION_TITLE] = post['jobtitle'].encode('ascii', 'xmlcharrefreplace')
		features[features.POSITION_CITY] = post['city'].encode('ascii', 'xmlcharrefreplace')
		features[features.POSITION_STATE] = post['state'].encode('ascii', 'xmlcharrefreplace')
		features[features.POSITION_COUNTRY] = post['country'].encode('ascii', 'xmlcharrefreplace')
		features[features.POST_DATE] = post['date']
		features[features.POST_URL] = post['url']
		features[features.SITE_JOBSID] = 'INDEED:%s' % post['jobkey']
		# TODO parse the latlong information
		
		features[features.POST_TEXT] = self.retrievePostText(post['url']).encode('ascii', 'xmlcharrefreplace')

		return features

def main():
	crawler = IndeedCrawler()
	crawler.start()

if __name__ == '__main__':
	main()