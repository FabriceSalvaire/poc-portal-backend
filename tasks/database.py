####################################################################################################
#
# Donate - A donation Web Application
# Copyright (C) 2020 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import io
import os
import subprocess
import sys

from invoke import task

#! from .Common.Datetime import now_to_str

####################################################################################################

# https://alembic.sqlalchemy.org/en/latest/tutorial.html

####################################################################################################

@task()
def alembic_revision(ctx, message):
    """Create a Alembic migration script"""
    ctx.run('alembic revision --autogenerate -m "{}"'.format(message))

####################################################################################################

@task()
def alembic_upgrade(ctx):
    """Run alembic upgrade"""
    ctx.run('alembic upgrade head')

####################################################################################################

@task()
def create_postgresql_database(
        ctx,
        host='localhost',
        user='postgres',
        database='donate',
        owner='donate',
        drop=False,
):

    if drop:
        dump_postgresql(ctx)
        sql = f'DROP DATABASE IF EXISTS "{database}";'
    else:
        sql = ''

    sql += (
        f'CREATE DATABASE "{database}"'
        f'  WITH OWNER = "{owner}"'
        f'  TEMPLATE = template0'
        f'  ENCODING = "UTF8"'
        f'  CONNECTION LIMIT = -1'
        f';'
    )

    string_io = io.StringIO(sql)
    ctx.run(f'psql -h {host} -U {user}', in_stream=string_io)

    # su - postgres
    # ctx.run('createuser --pwprompt donate')
    # ctx.run('createdb --owner=donate --encoding=UTF8 --template=template0 donate')

    # \dT show tables

####################################################################################################

@task()
def dump_postgresql(
        ctx,
        host='localhost',
        username='donate',
        database='donate',
):

    date = now_to_str()

    command = (
        'pg_dump',
        f'--host={host}',
        '-U', username,
        '--clean',
        '--create',
        f'--file={database}-{date}.sql.gz',
        '--compress=9',
        'donate',
    )
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

####################################################################################################

@task()
def dump_postgresql_to_json(
        ctx,
        host='localhost',
        username='donate',
        database='donate',
):

    """Dump a PostgreSQL Database to JSON.

    """

    # donate=> \d
    # public|alembic_version|table|donate
    # public|log|table|donate

    command = (
        'psql',
        f'--host={host}',
        '-U', username,
        database,
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

    tables = (
        'alembic_version',
        # 'log',
    )

    commands = [
        r'\pset format unaligned',
        r'\t on',
    ]
    commands.extend([
        f'with t as (select * from {table}) select json_agg(t) from t \g donate-{table}-{date}.json'
        for table in tables
    ])
    command = os.linesep.join(commands)
    print(command)
    send_command(command)
