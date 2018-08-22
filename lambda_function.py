import os
import json
import base64
import logging
import urllib.request
import urllib.parse


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    jenkins_url = os.environ.get("JENKINS_URL")
    job_name = "test"
    logger.info("Received event: " + json.dumps(event))

    url = os.path.join(jenkins_url, "job", job_name, "buildWithParameters")
    logger.info("Request to " + url)

    basic_user_and_pasword = base64.b64encode("jenkins:jenkins".encode("utf-8")).decode("utf-8")
    headers = {}
    headers["Authorization"] = "Basic " + basic_user_and_pasword

    params = {
        "ENV": "HOGEGG",
        "VERSION": "aaa",
    }

    req = urllib.request.Request("{}?{}".format(url, urllib.parse.urlencode(params)),
                                 json.dumps(params).encode(),
                                 headers=headers)
    # req = urllib.request.Request(url, json.dumps(params).encode(),
    #                              headers=headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()

    logger.info(body)
