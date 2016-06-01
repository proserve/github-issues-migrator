# GitHub issues importer
A simple tool to migrate you issues from your old repository. 

## License
This tool is licensed under GNU Lesser General Public License (LGPL).


## Hacking
### Install dependencies

    sudo python setup.py install 


### Run on local server
Start a local webserver by running:

    python migration_app.py 



## Limitations
1. This tool import only the following fields ( title, body, assignee) due to the limitation imposed by the  GitHub APi (https://developer.github.com/v3/issues/#create-an-issue)

