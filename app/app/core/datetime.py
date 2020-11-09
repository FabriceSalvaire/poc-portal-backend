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

__all__ = [
    'datetime_to_str',
    'from_timestamp',
    'now_to_str',
    'str_to_datetime',
]

####################################################################################################

from datetime import datetime

####################################################################################################

_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Fixme: datetime.isoformat
def datetime_to_str(date):
    return date.strftime(_DATETIME_FORMAT)

def str_to_datetime(date):
    _ = str(date).strip()
    return datetime.strptime(_, _DATETIME_FORMAT)

####################################################################################################

def now_to_str(time=True):
    if time:
        return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    else:
        return datetime.now().strftime('%Y-%m-%d')

####################################################################################################

def from_timestamp(_):
    return datetime.fromtimestamp(int(_))
