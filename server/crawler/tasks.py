from __future__ import absolute_import
from crawler.celery import celery
from celery.signals import celeryd_after_setup
from models.data_manager import dataMgr
from sqlalchemy.orm import Session
from models.models import Job, User, UserJobsAssociation
from mailer.mailer import JobMailer
from recommender.job_recommender import JobRecommender

def chunk(list, chunksize):
	return [list[i:i+chunksize] for i in range(0, len(list), chunksize)]

# @celeryd_after_setup.connect
# def setup_direct_queue(sender, instance, **kwargs):


@celery.task(ignore_result=True)
def crawl(crawler):
	print "Crawl task started"
	for i in range(1, crawler.maxPosts, crawler.numPostsPerRequest):
		# retrievePosts.delay(crawler, crawler.buildRequest(i, (i + crawler.numPostsPerRequest)))
		chain = retrievePosts.s(crawler, crawler.buildRequest(i, (i + crawler.numPostsPerRequest))) | matchPosts.s()
		chain.apply_async()

@celery.task(ignore_result=True)
def retrievePosts(crawler, url):
	print "Retrieve posts task started"
	return crawler.processPosts(url)

@celery.task(ignore_result=True)
def matchPosts(posts):
	print "Match posts task started"
	for post in posts:
		findMatchingUsers.delay(post)

@celery.task(ignore_result=True)
def findMatchingUsers(post):
	print "Find matching users task started"
	users = dataMgr.findMatchingUsers(post)
	batches = chunk(users, 100)
	for batch in batches:
		matchPost.delay(post, batch)
	# dataMgr.close()

@celery.task(ignore_result=True)
def matchPost(post, users):
	print "Match post task started"
	rec = JobRecommender(0.25)
	matchUsers = rec.matchUsersToJob(users, post)

	for (user,score) in matchUsers:
		userjob = UserJobsAssociation()
		userjob.job = post
		userjob.userID = user.userID
		userjob.score = score
		dataMgr.add(userjob)
		
	dataMgr.commit()
	
@celery.task(ignore_result=True)
def crawler():
	# TODO should dynamically load crawlers
	from crawler.crawlers.indeed import IndeedCrawler
	crawlers = [IndeedCrawler()]
	
	for crawler in crawlers:
		crawl.delay(crawler)

@celery.task(ignore_result=True)
def sendDigest(users):
	mailer = JobMailer()
	print "Send job digest"
	for user in users:
		mailer.sendDigest(user, [jobassoc.job for jobassoc in user.jobs])
		for jobassoc in user.jobs:
			jobassoc.processed = 'Y'
			dataMgr.merge(jobassoc)
		dataMgr.commit()

@celery.task(ignore_result=True)
def digestMailer():
	print "Emailing job digest"
	users = dataMgr.findDigestUsers()
	
	batches = chunk(users, 100)
	for batch in batches:
		sendDigest.delay(batch)
