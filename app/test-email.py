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

# https://github.com/lavr/python-emails
# https://python-emails.readthedocs.io
import emails

####################################################################################################

sender = '...'

message = emails.Message(
    subject="Test",
    text="just a test",
    # html='',
    mail_from=("Fabrice", sender),
)
smtp_options = {
    "host": "smtp.orange.fr",
    "port": 25,
}
# smtp_options["tls"] = True
# smtp_options["user"] = ""
# smtp_options["password"] = ""

environment = {}
response = message.send(to=sender, render=environment, smtp=smtp_options)
print(response)
if response.status_code not in [250, ]:
    print('Failed')
