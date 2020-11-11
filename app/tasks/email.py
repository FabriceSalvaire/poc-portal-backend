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

from pathlib import Path

from invoke import task

# https://github.com/lavr/python-emails
# https://python-emails.readthedocs.io
# import emails

from app.core.config import settings
from app.utils import send_test_email

####################################################################################################

APP_PATH = Path(__file__).parents[1]
TEMPLATE_PATH = APP_PATH.joinpath("app", "email-templates")
SRC_PATH = TEMPLATE_PATH.joinpath("src")
BUILD_PATH = TEMPLATE_PATH.joinpath("build")

####################################################################################################

### def _send_test_email():
###     sender = settings.EMAILS_FROM_EMAIL
###
###     message = emails.Message(
###         subject="Test",
###         text="just a test",
###         # html='',
###         mail_from=("John Doe", sender),
###     )
###     smtp_options = {
###         "host": settings.SMTP_HOST,
###         "port": settings.SMTP_PORT,
###     }
###     # smtp_options["tls"] = True
###     # smtp_options["user"] = ""
###     # smtp_options["password"] = ""
###
###     environment = {}
###     response = message.send(to=sender, render=environment, smtp=smtp_options)
###     print(response)
###     if response.status_code not in [250, ]:
###         print('Failed')

####################################################################################################

@task()
def send_test_email(ctx):
    sender = settings.EMAILS_FROM_EMAIL
    send_test_email(sender)

####################################################################################################

@task()
def compile_mjml(ctx, watch=False):
    # https://mjml.io/documentation/#command-line-interface
    # -r, --read      Compile MJML File(s)                                 [tableau]
    # -m, --migrate   Migrate MJML3 File(s)                                [tableau]
    # -v, --validate  Run validator on File(s)                             [tableau]
    # -w, --watch     Watch and compile MJML File(s) when modified         [tableau]
    # -i, --stdin     Compiles MJML from input stream
    # -s, --stdout    Output HTML to stdout
    # -o, --output    Filename/Directory to output compiled files
    #                                                         [chaîne de caractères]
    # -c, --config    Option to pass to mjml-core
    command = [
        APP_PATH.joinpath("node_modules", ".bin", "mjml"),
    ]
    if watch:
        command += ["--watch", SRC_PATH]
    else:
        command += [SRC_PATH.joinpath("*.mjml")]
    command += [
        "--output", BUILD_PATH,
        "--config.beautify",
        # "--config.minify",
    ]
    command = " ".join([str(_) for _ in command])
    print(command)
    ctx.run(command)

####################################################################################################

# @task()
# def xdg_open(ctx):
#     ctx.run(f"xdg-open {BUILD_PATH}")
