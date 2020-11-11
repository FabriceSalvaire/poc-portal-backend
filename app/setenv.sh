source common.sh
source env/bin/activate
append_to_python_path_if_not ${PWD}
source <(invoke --print-completion-script bash)

export BACKEND_SETTINGS_PATH='dev.env'
