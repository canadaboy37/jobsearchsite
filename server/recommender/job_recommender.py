from models.models import UserFeatures, JobFeatures
from crawler.crawlers.indeed import *
from user_profile_manager import UserProfileManager
from sets import Set
import math
import numpy

class JobRecommender(object):
	def __init__(self, threshold = 0.5):
		self.THRESHOLD = threshold
	
	def cosine_distance(self, u, v):
		"""
		Returns the cosine of the angle between vectors v and u. This is equal to
		u.v / |u||v|.
		"""
		dist = numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v))) 
		print 'distance: ' + str(dist)
		return dist
		
	def createVectors(self, x, y):
		xkeys = x.keys()
		ykeys = y.keys()
		# words = [key for key in xkeys if key in ykeys]
		words = Set(xkeys + ykeys)
		
		vx = []
		vy = []
		
		for word in words:
			cx = 0
			cy = 0
			if word in x: cx = x[word]
			if word in y: cy = y[word]
			vx.append(cx)
			vy.append(cy)
		return (vx, vy)
		
	def matchUsersToJob(self, users, jobpost):
		matches = []
		
		postFreqDist = jobpost.featureObj[JobFeatures.POST_FREQDIST]

		for user in users:
			userFreqDist = user.featureObj[UserFeatures.CV_FREQDIST]
			(u, v) = self.createVectors(userFreqDist, postFreqDist)
			
			score = self.cosine_distance(u, v)
			if score > self.THRESHOLD:
				matches.append((user,score))
		return matches

	def matchJobsToUser(self, user, jobposts):
		matches = []
		
		userFreqDist = user.featureObj[UserFeatures.CV_FREQDIST]
		
		for post in jobposts:
			postFreqDist = post.featureObj[JobFeatures.POST_FREQDIST]
			(u, v) = self.createVectors(userFreqDist, postFreqDist)
			
			score = self.cosine_distance(u, v)
			if score > self.THRESHOLD:
				matches.append((post,score))
		return matches
	
def main():
	# Import test
	usrMgr = UserProfileManager()
	crawler = IndeedCrawler()
	
	user = usrMgr.create('robbi', '~/Dropbox/Employment/Robbi/RMcDonaldRes2008.doc')
	jobs = crawler.test()
	
	recommender = JobRecommender(0.2)
	
	matches = recommender.matchJobsToUser(user, jobs)
	print matches
		
if __name__ == '__main__':
	main()