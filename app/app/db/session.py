####################################################################################################
#
# POC - 
# Copyright (C) 2020 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

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
