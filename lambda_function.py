import os
import json
import base64
import logging
import urllib.request
import urllib.parse


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def fetch_params_startswith(startswith, attributes):
    ret = {}
    keys = [k for k in attributes.keys() if k.startswith(startswith)]

    for k in keys:
        rk = k.replace(startswith, "")
        ret[rk] = attributes[k]

    return ret


def lambda_handler(event, context):
    jenkins_url = os.environ.get("JENKINS_URL")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")

    # logger.info("Received event: " + json.dumps(event))
    attributes = event["placementInfo"]["attributes"]

    headers = {}

    if password is not None:
        basic_user_and_pasword = base64.b64encode((user+":"+password).encode("utf-8")).decode("utf-8")
        headers["Authorization"] = "Basic " + basic_user_and_pasword

    clickType = event["deviceEvent"]["buttonClicked"]["clickType"]
    job_name = attributes.get(clickType + "_JOB")

    if job_name is not None:
        params = fetch_params_startswith(clickType+"_", attributes)

    else:
        logger.fatal("Not suppert deveceEvent: " + clickType)
        return

    crumb_url = os.path.join(jenkins_url, 'crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)')
    logger.info("Crumb request to " + crumb_url)
    req = urllib.request.Request(crumb_url, headers=headers)

    try:
        with urllib.request.urlopen(req) as res:
            body = res.read().decode("utf-8")
            print(body)
            jenkins_crumb = body.split(":")[1]
            logger.info("Jenkins-Crumb: " + jenkins_crumb)
            headers["Jenkins-Crumb"] = jenkins_crumb
    except urllib.error.HTTPError as e:
        if e.code == 404:
            logger.info("No crumb")
        else:
            raise e

    url = os.path.join(jenkins_url, "job", job_name, "buildWithParameters")

    logger.info("Request to " + url)
    logger.info("Params is " + json.dumps(params))
    req = urllib.request.Request("{}?{}".format(url, urllib.parse.urlencode(params)),
                                 json.dumps(params).encode(),
                                 headers=headers)

    try:
        with urllib.request.urlopen(req) as res:
            logger.info("status: " + str(res.status))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            logger.error("job not found: " + job_name)
        else:
            raise e
