####################################################################################################

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
### Retrieving Poetry metadata
###
### # Welcome to Poetry!
###
### This will download and install the latest version of Poetry,
### a dependency and package manager for Python.
###
### It will add the `poetry` command to Poetry's bin directory, located at:
###
### $HOME/.poetry/bin
###
### This path will then be added to your `PATH` environment variable by
### modifying the profile files located at:
###
### $HOME/.profile
### $HOME/.bash_profile
###
### You can uninstall at any time by executing this script with the --uninstall option,
### and these changes will be reverted.
###
### Installing version: 1.1.3
###   - Downloading poetry-1.1.3-linux.tar.gz (57.01MB)
###
### Poetry (1.1.3) is installed now. Great!
###
### To get started you need Poetry's bin directory ($HOME/.poetry/bin) in your `PATH`
### environment variable. Next time you log in this will be done
### automatically.
###
### To configure your current shell run `source $HOME/.poetry/env`

####################################################################################################

python3.8 -m venv env
source env/bin/activate

pip install --upgrade pip

poetry install

####################################################################################################
#
# see doc/deployment.md
#

# ...

####################################################################################################

# http://127.0.0.1:8000/docs
# login using username = FIRST_SUPERUSER and password = FIRST_SUPERUSER_PASSWORD
