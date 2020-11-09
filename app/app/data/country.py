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

__all__ = ['country_db']

####################################################################################################

from pathlib import Path
from typing import Optional
import yaml

from pydantic import BaseModel, conint, constr, PositiveInt

####################################################################################################

class Country(BaseModel):
    code: constr(regex=r'^[A-Z][A-Z]$')
    code3: constr(regex=r'^[A-Z][A-Z][A-Z]$')
    number: conint(gt=0)   # PositiveInt
    name: str
    local_name: Optional[str] = None
    flag: Optional[str] = None

####################################################################################################

class CountryDB:

    ##############################################

    def __init__(self):
        self._iso_country_list_lazy = None
        self._map_lazy = None

    ##############################################

    @property
    def _iso_country_list(self):
        if self._iso_country_list_lazy is None:
            self._load()
        return self._iso_country_list_lazy

    ##############################################

    @property
    def _map(self):
        if self._map_lazy is None:
            self._load()
        return self._map_lazy

    ##############################################

    def _load(self):

        path = Path(__file__).parent.joinpath('country.yaml')
        iso_country_list = yaml.load(
            open(str(path), 'r'),
            Loader=yaml.SafeLoader,
        )
        self._iso_country_list_lazy = [Country(**item) for item in iso_country_list]

        self._map_lazy = {}

        _ = {country.code3: country for country in self._iso_country_list_lazy}
        self._map_lazy.update(_)

        _ = {country.code: country for country in self._iso_country_list_lazy}
        self._map_lazy.update(_)

        _ = {country.name: country for country in self._iso_country_list_lazy}
        self._map_lazy.update(_)

        _ = {country.number: country for country in self._iso_country_list_lazy}
        self._map_lazy.update(_)

    ##############################################

    def __len__(self):
        return len(self._iso_country_list)

    ##############################################

    def __iter__(self):
        return iter(self._iso_country_list)

    ##############################################

    def __getitem__(self, key):
        return self._map[key]

####################################################################################################

country_db = CountryDB()
