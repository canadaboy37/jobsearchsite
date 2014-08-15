from db import Session
from sqlalchemy.orm import joinedload_all
from sqlalchemy.sql.expression import select, exists
from models import Job, User, UserJobsAssociation


class DataManager(Session):
	_instance = None
	
	def __init__(self):
		super(DataManager, self).__init__()

	def findMatchingUsers(self, post):
		# TODO filter users by filter rules
		return self.query(User).all()

	def findDigestUsers(self):
		return self.query(User).options(joinedload_all('jobs.job')).filter(UserJobsAssociation.processed=='N').all()
		
	def postExists(self, jobid):
		return (self.query(exists([Job.jobsID])).filter(Job.siteJobsID==jobid).scalar() is not None)

# Singleton datamanager
dataMgr = DataManager()