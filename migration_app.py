import json

from flask import Flask, render_template, redirect, request, jsonify, session

from config import config
from dateutil.parser import parse
from github import github
from github.github import GithubRequest

app = Flask(__name__)

github_helper = None
if config.get('environment') == 'local':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
elif config.get('environment') == 'prod':
    app.config.from_pyfile('app.cfg')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/auth/github")
def github_auth():
    scope = 'repo'
    helper = github.GithubAuth(config.get('github_server'),
                               config.get('github_redirect_uri'), scope)
    return redirect(helper.get_authorize_url())


@app.route("/callback/")
def github_auth_callback():
    code = request.args['code']
    scope = 'repo'
    helper = github.GithubAuth(config.get('github_server'),
                               config.get('github_redirect_uri'), scope)
    access_token = helper.get_access_token(code)
    session['access_token'] = access_token
    return redirect("choose_repo")


@app.route("/choose_repo/")
def choose_repo():
    access_token = session['access_token']
    repos_list = GithubRequest(access_token).fetch_user_repos()
    return render_template('choose_repo.html', repos_list=repos_list)


@app.route("/migrate_issues/")
def migrate_issues():
    repo_from_data = str(request.args['from_repo']).split(',')
    from_repo_name = repo_from_data[0]
    from_repo_own = repo_from_data[1]

    repo_into_data = str(request.args['into_repo']).split(',')
    into_repo_name = repo_into_data[0]
    into_repo_own = repo_into_data[1]
    access_token = session['access_token']
    repo_issues = GithubRequest(access_token).get_issues_list(from_repo_name, from_repo_own)
    issues = {issue.get('number'): issue for issue in repo_issues}
    return render_template('migrate_issues.html', issues=issues, into_repo=into_repo_name,
                           from_repo=from_repo_name, into_repo_own=into_repo_own)


@app.route("/migrate/", methods=['GET', 'POST'])
def migrate():
    access_token = session['access_token']
    issues = json.loads(request.values.get('issues'))
    owner = request.values.get('owner')
    repo = request.values.get('repo')
    for issue in issues:
        GithubRequest(access_token).create_issue(owner, repo, issue)
    return jsonify(sucss=True)


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = parse(date)
    native = date.replace(tzinfo=None)
    form = fmt if fmt else '%b %d %Y %I:%M%p'
    return native.strftime(form)


if __name__ == '__main__':
    app.run(debug=True)
