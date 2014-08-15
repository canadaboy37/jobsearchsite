from __future__ import absolute_import
from datetime import timedelta
from celery import Celery

celery = Celery(broker='amqp://localhost',
				backend='amqp://localhost',
				include=['crawler.tasks', 'nlp', 'models', 'mailer'])

# Optional configuration, see the application user guide.
celery.conf.update(
	CELERY_TASK_RESULT_EXPIRES=3600,
	CELERYBEAT_SCHEDULE = {
		'crawler': {
			'task': 'crawler.tasks.crawler',
			'schedule': timedelta(hours=12)
		},
		'mailer': {
			'task': 'crawler.tasks.digestMailer',
			'schedule': timedelta(hours=12)
		},
	}
)

