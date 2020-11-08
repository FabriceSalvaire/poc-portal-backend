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

from typing import Optional

from pydantic import BaseModel, EmailStr

####################################################################################################

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

####################################################################################################

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

####################################################################################################

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

####################################################################################################

class UserInDbBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

####################################################################################################

# Additional properties to return via API
class User(UserInDbBase):
    pass

####################################################################################################

# Additional properties stored in DB
class UserInDb(UserInDbBase):
    hashed_password: str
