import pickle
from nltk import FreqDist
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, Float, PickleType, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import MutableType, TypeDecorator

Base = declarative_base()

class UserFeatures(dict):
	CV_FREQDIST		= 'CVFreqDist'
	
	def __init__(self):
		super(dict, self).__init__()
		
	def __getstate__(self):
		# Copy the object's state from self.__dict__ which contains
		# all our instance attributes. Always use the dict.copy()
		# method to avoid modifying the original state.
		state = super(UserFeatures, self).copy()
		return state
	
	def __setstate__(self, state):
		# Restore instance attributes (i.e., post_freqdist).
		for key, val in state.items():
			self.__dict__[key] = val
			
	def __setitem__(self, key, value):
		return super(UserFeatures, self).__setitem__(key, value)
	
	def __getitem__(self, name):
		return super(UserFeatures, self).__getitem__(name)
	
	def __delitem__(self, name):
		return super(UserFeatures, self).__delitem__(name)
	
	__getattr__ = __getitem__
	__setattr__ = __setitem__
	
	def copy(self):
		return UserFeatures(self)


class JobFeatures(dict):	
	COMPANY_NAME 		= 'CompanyName'
	POSITION_TITLE 		= 'PositionTitle'
	POSITION_CITY		= 'PositionCity'
	POSITION_STATE		= 'PositionState'
	POSITION_COUNTRY	= 'PositionCountry'
	POST_TEXT			= 'PostText'
	POST_FREQDIST		= 'PostFreqDist'
	POST_DATE			= 'PostDate'
	POST_URL			= 'PostUrl'
	SITE_JOBSID			= 'SiteJobsID'

	# def __init__(self, *args, **kwargs):
		# super(JobFeatures, self).__init__(self, *args, **kwargs)
		
	def __init__(self):
		super(dict, self).__init__()
		
	def __getstate__(self):
		# Copy the object's state from self.__dict__ which contains
		# all our instance attributes. Always use the dict.copy()
		# method to avoid modifying the original state.
		state = super(JobFeatures, self).copy()
		# state = self.copy()
		# print "STATE1" + str(state)
		# Replace the unpicklable entries.
		# state[self.POST_FREQDIST] = FreqDistStorer.object_to_dict(state[self.POST_FREQDIST])
		# print "STATE2" + str(state)
		return state
	
	def __setstate__(self, state):
		# Restore instance attributes (i.e., post_freqdist).
		for key, val in state.items():
			self.__dict__[key] = val
			
	def __setitem__(self, key, value):
		return super(JobFeatures, self).__setitem__(key, value)
	
	def __getitem__(self, name):
		return super(JobFeatures, self).__getitem__(name)
	
	def __delitem__(self, name):
		return super(JobFeatures, self).__delitem__(name)
	
	__getattr__ = __getitem__
	__setattr__ = __setitem__
	
	def copy(self):
		return JobFeatures(self)

class UserJobsAssociation(Base):
	__tablename__ = 'Results'
	jobsID = Column(Integer, ForeignKey('Jobs.jobsID'), primary_key=True)
	userID = Column(Integer, ForeignKey('Users.userID'), primary_key=True)
	score = Column(Float, default=0.0)
	processed = Column(String, default='N')
	dateAdded = Column(DateTime)
	job = relationship("Job")
	
class User(Base):
	__tablename__ = 'Users'
	
	userID = Column(Integer, primary_key=True)
	firstName = Column(String)
	lastName = Column(String)
	email = Column(String)
	featureObj = Column(PickleType)
	jobs = relationship('UserJobsAssociation')
	
	def __init__(self, firstname, lastname, email, featureObj):
		self.firstName = firstname
		self.lastName = lastname
		self.email = email
		self.featureObj = featureObj
		
	def __repr__(self):
		return "<User('%s','%s', '%s')>" % (self.firstName, self.lastName, self.email)
		
	def fullName(self):
		return "%s %s" % (self.firstName, self.lastName)
		
class Job(Base):
	__tablename__ = 'Jobs'
	
	jobsID = Column(Integer, primary_key=True)
	siteJobsID = Column(String)
	url = Column(String)
	shorturl = Column(String)
	title = Column(String)
	description = Column(String)
	featureObj = Column(PickleType)
	dateAdded = Column(DateTime)
	
	def __init__(self, siteJobsID, url, shorturl, title, description, featureObj):
		self.siteJobsID = siteJobsID
		self.url = url
		self.shorturl = shorturl
		self.title = title
		self.description = description
		self.featureObj = featureObj
		# self.dateAdded = dateAdded

	def __repr__(self):
		return "<Job('%s','%s', '%s')>" % (self.url, self.title, self.description)
	