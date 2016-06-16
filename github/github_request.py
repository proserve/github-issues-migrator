import json

import oauth_client as oauth2

from config.local import config


class GithubRequest(object):
    def __init__(self, access_token, github_client_id=config.get('github_client_id'),
                 github_client_secret=config.get('github_client_secret')):
        self.access_token = access_token
        self.oauth_settings = {
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'access_token_url': 'https://%s/login/oauth/access_token' % access_token,
        }

    def get_user_info(self):
        return self.make_request('user')

    def fetch_user_repos(self):
        return self.make_request('user/repos', params={'per_page': 1000})

    def get_issues_list(self, repo_name, repo_own):
        return self.make_request('repos/' + repo_own + '/' + repo_name + '/issues', params={'per_page': 1000})

    def create_issue(self, owner, repo, issue):
        body = json.dumps(issue)
        return self.make_request('repos/' + owner + '/' + repo + '/issues', method='POST', body=body)

    def get_oauth(self):
        return oauth2.Client(
            self.oauth_settings['client_id'],
            self.oauth_settings['client_secret'],
            self.oauth_settings['access_token_url']
        )

    def make_request(self, endpoint, body=None, method='GET', params=None):
        oauth_client = self.get_oauth()
        (headers, body) = oauth_client.request(
            'https://api.github.com/' + endpoint,
            access_token=self.access_token,
            token_param='access_token',
            method=method,
            body=body,
            params=params
        )
        return json.loads(body)
