import requests
import time
import jwt

from flask import Flask
from flask import request
# from github import GithubIntegration
from github import Github

app = Flask(__name__)

GITHUB_API_URL = 'https://api.github.com'

@app.route("/", methods = ['POST', 'GET'])
def pull_request_webhook_handler():
    payload = request.json
    if payload['action'] in ['opened', 'reopened']:
        PR_COMMENT_RESOURCE = '/repos/{owner}/{repo}/pulls/{pull_number}/comments'.format(owner=payload['repository']['owner']['login'],
                                                                                          repo=payload['repository']['name'],
                                                                                          pull_number=payload['number'])

        body = 'This is my comment'
        my_jwt = get_jwt()
        headers = {"Authorization": "Bearer {}".format(my_jwt),
                   "Accept": "application/vnd.github.v3+json"}
        request_url = GITHUB_API_URL + PR_COMMENT_RESOURCE
        r = requests.post(request_url, data={'body': body}, headers=headers)
        print(r)

    return "bye world - testing"

def get_jwt():
    
    fname = '/Users/gill/Downloads/prdeployapp.2021-11-13.private-key.pem'
    
    current_time = int(time.time())
    payload = {
        # issued at time
        'iat': current_time,

        # JWT expiration time (10 minute maximum)
        'exp': current_time + (10 * 60),

        # GitHub App's identifier – you can get it from the github application dashboard
        'iss': 151624,
    }

    private_key_file = fname
    with open(private_key_file) as fd:
        private_key_contents = fd.read().encode()
    
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    from cryptography.hazmat.backends import default_backend

    cert_obj = load_pem_private_key(private_key_contents, password=None, backend=default_backend())
    encoded = jwt.encode(payload, private_key_contents, algorithm='RS256')

    return encoded

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=80)