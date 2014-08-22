web: newrelic-admin run-program gunicorn gifts.wsgi --log-file -
worker: python gifts/manage.py rqworker high default low