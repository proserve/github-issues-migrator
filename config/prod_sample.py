# Please rename this file to prod.py before deploy on openshift
config = {
    'environment': 'prod',
    # Github login
    # Register apps here: https://github.com/settings/applications/new
    'github_server': 'github.com',
    'github_redirect_uri': 'http://YOU-SITE.com/callback',
    'github_client_id': '_PUT_YOUR_GITHUB_CLIENT_ID',
    'github_client_secret': '_PUT_YOUR_GITHUB_CLIENT_SECRET',
}
