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

from datetime import datetime, timedelta
from typing import Any, Union

# JavaScript Object Signing and Encryption (JOSE)
#   https://github.com/mpdavis/python-jose
#   https://python-jose.readthedocs.io/
from jose import jwt

# Passlib is a password hashing library
#   https://passlib.readthedocs.io
from passlib.context import CryptContext

from app.core.config import settings

####################################################################################################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"   # for JWT

####################################################################################################

def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

####################################################################################################

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

####################################################################################################

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
