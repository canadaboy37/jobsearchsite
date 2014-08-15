from site_crawler import SiteCrawler
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, SoupStrainer, NavigableString, Comment

class BCTechnologyCrawler(SiteCrawler):
	
	def __init__(self):
		super(BCTechnologyCrawler, self).__init__('http://www.bctechnology.com', '/scripts/search_results3.cfm?iterator=%s', 10, 100)
		
	def parse_job_listing(self, html):
		urls = []
		for link in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):	
			if link.has_key('href') and 'show_job.cfm' in link['href']:
				urls += link['href'] #urlparse(link['href'])
		return urls
		
	def parse_job_post(self, html):
		features = dict()
		soup = BeautifulSoup(html)
		form = soup.first('form', {'name' : 'applyjob'})
		features[COMPANY_NAME] = form.first('input', {'name' : 'company_name'})
		features[POSITION_TITLE] = form.first('input', {'name' : 'position'})
		features[POST_DATE] = form.first('input', {'name' : 'insert_date'})
			
			
		print html
		return (None, features)
	
def main():
	crawler = BCTechnologyCrawler()
	crawler.start()
		
if __name__ == '__main__':
	main()