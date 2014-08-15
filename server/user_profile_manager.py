from importers.resume_importer import ResumeImporter
from models.data_manager import DataManager
from nltk import FreqDist

class UserProfileManager(object):
	def __init__(self):
		return
	
	def create(self, user, resume):
		importer = ResumeImporter()
		(rawtext, words) = importer.importWordDoc(resume)
		
		freqdist = FreqDist(w.lower() for w in words)
		
		return freqdist
		
	def update(self, user):
		return
		
	def delete(self, user):
		return
			
def main():
	mgr = UserProfileManager()
	freqDist = mgr.create(None, 'test/RMcDonaldResume-Aug1-12.doc')
	
	from models.data_manager import DataManager
	from models.models import User, UserFeatures
	
	features = UserFeatures()
	features[features.CV_FREQDIST] = dict(freqDist)
	
	user = User('Robbi', 'McDonald', 'rlmcdona@hotmail.com', features)
	
	# start a new db session
	dataMgr = DataManager()
	dataMgr.add(user)
	dataMgr.commit()
	dataMgr.close()
	
if __name__ == '__main__':
	main()