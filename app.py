import json
import os
import time

import jwt
import requests

from flask import Flask
from flask import request

app = Flask(__name__)

GITHUB_API_DOMAIN = 'https://api.github.com'
ACCESS_TOKEN_ENDPOINT = '/app/installations/{}/access_tokens'

@app.route("/", methods = ['POST', 'GET'])
def pull_request_webhook_handler():
    """Handles the webhook generated when a pull request is raised."""
    payload = request.json
    if payload['action'] in ['opened', 'reopened']:

        # repo_clone_url = payload['pull_request']['head']['repo']['clone_url']
        # branch_name = payload['pull_request']['head']['ref']

        post_webapp_link_as_comment(payload)

    return "comment has been added"

def post_webapp_link_as_comment(payload):
    """Posts the link of the deployed website as a comment in the pull request"""
    request_url = payload['pull_request']['issue_url'] + '/comments'
    body = 'This is my comment'
    access_token = get_access_token(payload)
    headers = {"Authorization": "token {}".format(access_token),
               "Accept": "application/vnd.github.v3+json"}
    requests.post(request_url, json={'body': body}, headers=headers)

    return


def get_access_token(payload):
    app_installation_id = payload['installation']['id']
    request_url = GITHUB_API_DOMAIN + ACCESS_TOKEN_ENDPOINT.format(app_installation_id)

    my_jwt = get_jwt()
    headers = {"Authorization": "Bearer {}".format(my_jwt),
               "Accept": "application/vnd.github.v3+json"}

    response = requests.post(request_url, headers=headers)
    access_token = json.loads(response.content)['token']
    return access_token


def get_jwt():
    path_to_private_key = os.getenv("PEM_FILE_PATH")
    pem_file = open(path_to_private_key, "rt").read()

    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + (10 * 60),
        "iss": os.getenv("GITHUB_APP_ID"),
    }
    encoded_jwt = jwt.encode(payload, pem_file, algorithm="RS256")

    return encoded_jwt

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)