# from smtplib import SMTP_SSL as SMTP
from smtplib import SMTP
from email.MIMEText import MIMEText

class JobMailer(object):

	SMTP_HOST 	= 'smtp.gmail.com'
	SMTP_PORT 	= 587
	SMTP_USER 	= 'scott.langevin@gmail.com'
	SMTP_PASS 	= 'whu5zoch2whoj6wu'
	SENDER 		= 'scott.langevin@gmail.com'
	
	MAX_DESC_LENGTH = 197
	
	def __init__(self):
		super(JobMailer, self).__init__()
		self.smtp = SMTP()
	
	def connect(self):
		self.smtp.connect(self.SMTP_HOST, self.SMTP_PORT)
		self.smtp.ehlo()
		self.smtp.starttls()
		self.smtp.ehlo()
		self.smtp.login(self.SMTP_USER, self.SMTP_PASS)
				
	def disconnect(self):
		try:
			self.smtp.quit()
		finally:
			self.smtp.close()
		
	def buildMailBody(self, jobs):
		return '\n\n'.join(['%s\n%s\n%s' % (job.url, job.title, '%s...' % job.description[:197]) for job in jobs])
		
	def buildMailSubject(self, jobs):
		return 'ProjectX found %s new Jobs for you!' % len(jobs)
		
	def sendDigest(self, user, jobs):
		try:
			self.connect()
			
			text_subtype = 'plain'
			body = self.buildMailBody(jobs)
			msg = MIMEText(body, text_subtype)
			msg['Subject'] = self.buildMailSubject(jobs)
			msg['From'] = self.SENDER # some SMTP servers will do this automatically, not all
			msg['To'] = user.email
			
			self.smtp.sendmail(self.SENDER, user.email, msg.as_string())
		
		except Exception, exc:
			print( "mail failed; %s" % str(exc) ) # give a error message
		finally:
			self.disconnect()