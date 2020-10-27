source env/bin/activate
append_to_python_path_if_not ${PWD}
source <(invoke --print-completion-script bash)

####################################################################################################
#
# Environments
#

export PROJECT_NAME="Donate"

export SERVER_NAME="localhost" # ???
export SERVER_HOST="http://localhost" # ???
export BACKEND_CORS_ORIGINS='["http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:8080"]'

export SENTRY_DSN="" # Fixme: None

export POSTGRES_SERVER="localhost"
export POSTGRES_USER="donate"
export POSTGRES_PASSWORD="donate"
export POSTGRES_DB="donate"
# SQLALCHEMY_DATABASE_URI = None

# export SMTP_TLS="False"
# export SMTP_PORT=""
# export SMTP_HOST=""
# export SMTP_USER=""
# export SMTP_PASSWORD=""

export EMAILS_FROM_EMAIL=""
export EMAILS_FROM_NAME=""
export EMAIL_TEMPLATES_DIR="./app/email-templates/build"
export EMAILS_ENABLED="False"
# EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

export FIRST_SUPERUSER="test@example.com"
export FIRST_SUPERUSER_PASSWORD="admin"

# USERS_OPEN_REGISTRATION: bool = False

source secret_env.sh
