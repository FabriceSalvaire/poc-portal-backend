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

import os

from invoke import task

####################################################################################################

# @task()
# def celeryworker_pre_start(
#         ctx,
# ):
#     pass
# python /app/app/celeryworker_pre_start.py
# celery worker -A app.worker -l info -Q main-queue -c 1

####################################################################################################

@task()
def dev_server(ctx, settings="dev.env"):
    """Start a dev server"""
    os.putenv("BACKEND_SETTINGS_PATH", settings)
    ctx.run("uvicorn app.main:app --reload")
