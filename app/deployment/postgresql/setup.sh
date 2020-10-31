####################################################################################################

su - postgres

createuser --pwprompt portal-demo
# dropdb portal-demo
createdb --owner=portal-demo --encoding=UTF8 --template=template0 portal-demo

####################################################################################################

# from Python env and app directory

export BACKEND_SETTINGS_PATH=/etc/portal-demo/prod.env
# set PYTHONPATH

inv -l
inv database.alembic-upgrade
