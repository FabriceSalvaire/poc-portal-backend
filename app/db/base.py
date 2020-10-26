####################################################################################################

# Import all the models, so that Base has them before being imported by Alembic,
#   cf. alembic/env.py
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
# Fixme: Alembic works without this line ???
from app.models.donation import Donator, Donation  # noqa
