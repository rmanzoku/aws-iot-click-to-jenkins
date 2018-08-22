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
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")

    logger.info("Received event: " + json.dumps(event))

    job_name = event["placementInfo"]["attributes"].get("job")
    url = os.path.join(jenkins_url, "job", job_name, "buildWithParameters")
    headers = {}
    logger.info("Request to " + url)

    if password is not None:
        basic_user_and_pasword = base64.b64encode((user+":"+password).encode("utf-8")).decode("utf-8")
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
