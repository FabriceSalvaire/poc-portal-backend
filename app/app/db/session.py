####################################################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

####################################################################################################

# https://docs.sqlalchemy.org/en/13/core/engines.html?highlight=create_engine#sqlalchemy.create_engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    # enable the connection pool “pre-ping” feature that tests connections for liveness upon each
    # checkout
    pool_pre_ping=True,
    echo=True,   # Fixme: debug
)

# Session Process:
#  - session.add( register operation to the database )
#  - ( session.flush() communicates theses operation to the database, but they aren't yet persisted )
#  - session.commit() write on disk, notice it always issues a Session.flush()
#  - session.refresh(obj) refresh all attributes of an object

# https://docs.sqlalchemy.org/en/13/orm/session_api.html?highlight=sessionmaker#sqlalchemy.orm.session.sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
