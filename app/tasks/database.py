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

import io
import logging
import os
import subprocess

from invoke import task

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config import settings
from app.core.datetime import now_to_str
from app.core.logging import setup_logging
from app.db.init_db import init_db
from app.db.session import SessionLocal, engine

####################################################################################################

logging_config_file = settings.LOGGING_CONFIG
logger = setup_logging(config_file=logging_config_file)
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

####################################################################################################

# https://alembic.sqlalchemy.org/en/latest/tutorial.html

####################################################################################################

@task()
def test_connection(
        ctx,
):
    """Test database connection"""

    max_tries = 60 * 5  # 5 minutes
    wait_seconds = 1

    @retry(
        stop=stop_after_attempt(max_tries),
        wait=wait_fixed(wait_seconds),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.WARN),
    )
    def init() -> None:
        try:
            db = SessionLocal()
            # Try to create session to check if DB is awake
            db.execute("SELECT 1")
        except Exception as e:
            logger.error(e)
            raise e

    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")

####################################################################################################

@task()
def create(
        ctx,
        drop=False,
):
    """Create the database"""

    postgres_server = settings.POSTGRES_SERVER
    postgres_db = settings.POSTGRES_DB
    postgres_user = settings.POSTGRES_USER
    postgres_password = settings.POSTGRES_PASSWORD

    # db = SessionLocal()
    # if drop:
    #     dump_postgresql(ctx)
    #     sql = f'DROP DATABASE IF EXISTS "{postgres_db}";'
    #     db.execute(sql)

    if drop:
        # dump_postgresql(ctx)
        sql = f'DROP DATABASE IF EXISTS "{postgres_db}";'
    else:
        sql = ''

    sql += (
        f'CREATE DATABASE "{postgres_db}"'
        f'  WITH OWNER = "{postgres_user}"'
        f'  TEMPLATE = template0'
        f'  ENCODING = "UTF8"'
        f'  CONNECTION LIMIT = -1'
        f';'
    )

    # How to change the default postgres password
    #
    # To disabled password
    #   /var/lib/pgsql/data/pg_hba.conf
    #     local   all   postgres   trust
    #
    # psql postgres postgres
    # \password postgres
    # \q

    # command = f'psql -h {postgres_server} -U {postgres_user}'
    command = f'psql -h {postgres_server} -U postgres'
    print(command)
    print(sql)

    string_io = io.StringIO(sql)
    logger.info("Create database")
    ctx.run(command, in_stream=string_io)

    # su - postgres
    # ctx.run('createuser --pwprompt {postgres_user}')
    # ctx.run('createdb --owner={postgres_user} --encoding=UTF8 --template=template0 {postgres_db}')

    # \dT show tables

####################################################################################################

@task()
def alembic_revision(ctx, message):
    """Create a Alembic migration script"""
    logger.warning('Run "create --drop" before to create the first revision !')
    ctx.run('alembic revision --autogenerate -m "{}"'.format(message))

####################################################################################################

@task()
def alembic_upgrade(ctx):
    """Run alembic upgrade"""
    logger.info("Upgrade database schema")
    ctx.run('alembic upgrade head')

####################################################################################################

@task()
def initialise(ctx):
    """Create initial data"""
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    logger.info("Initial data created")

####################################################################################################

@task()
def bootstrap(
        ctx,
        drop=False,
):
    """Bootstrap database"""
    create(ctx, drop)
    alembic_upgrade(ctx)
    initialise(ctx)

####################################################################################################

@task()
def dump(
        ctx,
):
    """Dump a PostgreSQL Database."""

    postgres_server = settings.POSTGRES_SERVER
    postgres_db = settings.POSTGRES_DB
    postgres_user = settings.POSTGRES_USER
    postgres_password = settings.POSTGRES_PASSWORD

    date = now_to_str()

    command = (
        'pg_dump',
        f'--host={postgres_server}',
        '-U', postgres_user,
        '--clean',
        '--create',
        f'--file={postgres_db}-{date}.sql.gz',
        '--compress=9',
        'donate',
    )
    print(' '.join(command))
    # Fixme: ???
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

####################################################################################################

@task()
def dump_to_json(
        ctx,
        host='localhost',
        username='donate',
        database='donate',
):
    """Dump a PostgreSQL Database to JSON."""

    postgres_server = settings.POSTGRES_SERVER
    postgres_db = settings.POSTGRES_DB
    postgres_user = settings.POSTGRES_USER
    postgres_password = settings.POSTGRES_PASSWORD

    tables = engine.table_names()
    # donate=> \d
    # public|alembic_version|table|donate
    # public|log|table|donate

    command = (
        'psql',
        f'--host={postgres_server}',
        '-U', postgres_user,
        postgres_db,
    )
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

    def send_command(command):
        try:
            outputs, errors = process.communicate(input=command, timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            outputs, errors = process.communicate()
        print('>', outputs)
        print('>', errors)
        return outputs

    # outputs = send_command('\d')
    # tables = []
    # for line in outputs.splitlines():
    #     if 'table' in line:
    #         name = [_ for _ in line.split('|')][1].strip()
    #         tables.append(name)

    date = now_to_str()

    commands = [
        r'\pset format unaligned',
        r'\t on',
    ]
    commands.extend([
        f'with t as (select * from {postgres_db}.public.{table}) select json_agg(t) from t \g donate-{table}-{date}.json'
        for table in tables
    ])
    command = os.linesep.join(commands)
    print(command)
    send_command(command)

####################################################################################################

@task()
def delete_donations(ctx):
    from app.db.session import SessionLocal
    from app.models.donation import Donator, Donation
    db = SessionLocal()
    db.query(Donation).delete()
    db.query(Donator).delete()
    db.commit()
