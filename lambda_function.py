import os
import json
import base64
import logging
import urllib.request
import urllib.parse


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def single_click_function(attributes):
    return {
        "ENV": attributes.get("single_env"),
        "VERSION": attributes.get("single_version"),
    }


def lambda_handler(event, context):
    jenkins_url = os.environ.get("JENKINS_URL")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")

    logger.info("Received event: " + json.dumps(event))

    job_name = event["placementInfo"]["attributes"].get("job")
    url = os.path.join(jenkins_url, "job", job_name, "buildWithParameters")
    headers = {}

    if password is not None:
        basic_user_and_pasword = base64.b64encode((user+":"+password).encode("utf-8")).decode("utf-8")
        headers["Authorization"] = "Basic " + basic_user_and_pasword

    clickType = event["deviceEvent"]["buttonClicked"]["clickType"]
    if clickType == "SINGLE":
        params = single_click_function(event["placementInfo"]["attributes"])

    else:
        logger.fatal("Not suppert deveceEvent: " + clickType)
        exit(1)

    logger.info("Request to " + url)
    logger.info("Params is " + json.dumps(params))
    req = urllib.request.Request("{}?{}".format(url, urllib.parse.urlencode(params)),
                                 json.dumps(params).encode(),
                                 headers=headers)
    urllib.request.urlopen(req)
