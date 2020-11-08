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

# https://alembic.sqlalchemy.org/en/latest/index.html

# print('Load env.py')

####################################################################################################

from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy import engine_from_config, pool

#! from .Config.ConfigFile import ConfigFile
#! from .Database import DatabaseMixin
#! from .Common.Orm.ServerDatabase import ServerDatabase

#! config_file = ConfigFile()

####################################################################################################

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set sqlalchemy.url
#! config.set_main_option('sqlalchemy.url', config.Database.connection_str())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
#! # database = ServerDatabase(config.Database)
#! declarative_base_cls, row_classes, table_classes = DatabaseMixin.create_schema_classes()
#! target_metadata = declarative_base_cls.metadata

from app.db.base import Base  # noqa
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

####################################################################################################

def get_url():
    from app.core.config import settings
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    server = settings.POSTGRES_SERVER
    db = settings.POSTGRES_DB
    url = f"postgresql://{user}:{password}@{server}/{db}"
    print(f'PostgreSQL: {url}')
    return url

####################################################################################################

def run_migrations_offline():

    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.

    """

    #! url = config.get_main_option("sqlalchemy.url")
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

####################################################################################################

def run_migrations_online():

    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection with the context.

    """

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        #! config.get_section(config.config_ini_section),
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

####################################################################################################

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
