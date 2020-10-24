source env/bin/activate
append_to_python_path_if_not ${PWD}
source <(invoke --print-completion-script bash)

export POSTGRES_USER="donate"
export POSTGRES_PASSWORD="donate"
export POSTGRES_SERVER="localhost"
export POSTGRES_DB="donate"
