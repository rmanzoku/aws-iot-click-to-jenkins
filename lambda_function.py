import os
import json
import base64
import logging
import urllib.request
import urllib.parse


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def single_click_function(attributes):
    return attributes.get("single_job"), {
        "ENV": attributes.get("single_env"),
        "VERSION": attributes.get("single_version"),
    }


def double_click_function(attributes):
    return attributes.get("double_job"), {
        "ENV": attributes.get("double_env"),
        "VERSION": attributes.get("double_version"),
    }


def long_click_function(attributes):
    return attributes.get("long_job"), {
        "ENV": attributes.get("long_env"),
        "VERSION": attributes.get("long_version"),
    }


def lambda_handler(event, context):
    jenkins_url = os.environ.get("JENKINS_URL")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")

    logger.info("Received event: " + json.dumps(event))
    attributes = event["placementInfo"]["attributes"]

    headers = {}

    if password is not None:
        basic_user_and_pasword = base64.b64encode((user+":"+password).encode("utf-8")).decode("utf-8")
        headers["Authorization"] = "Basic " + basic_user_and_pasword

    clickType = event["deviceEvent"]["buttonClicked"]["clickType"]
    if (clickType == "SINGLE") and (attributes.get("single_job") is not None):
        job_name, params = single_click_function(attributes)

    elif (clickType == "DOUBLE") and (attributes.get("double_job") is not None):
        job_name, params = double_click_function(attributes)

    elif (clickType == "LONG") and (attributes.get("long_job") is not None):
        job_name, params = long_click_function(attributes)

    else:
        logger.fatal("Not suppert deveceEvent: " + clickType)
        return

    url = os.path.join(jenkins_url, "job", job_name, "buildWithParameters")

    logger.info("Request to " + url)
    logger.info("Params is " + json.dumps(params))
    req = urllib.request.Request("{}?{}".format(url, urllib.parse.urlencode(params)),
                                 json.dumps(params).encode(),
                                 headers=headers)

    with urllib.request.urlopen(req) as res:
        logger.info("status: " + str(res.status))
