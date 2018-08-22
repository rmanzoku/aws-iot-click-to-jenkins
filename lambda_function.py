import os
import json
import logging
import urllib.request
import urllib.parse


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    jenkins_url = os.environ.get('JENKINS_URL')
    logger.info('Received event: ' + json.dumps(event))
