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
#
# https://docs.pytest.org/en/stable
# https://docs.pytest.org/en/stable/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
#
# Fixture scopes
#   Fixtures are created when first requested by a test, and are destroyed based on their scope:
#
#   function: the default scope, the fixture is destroyed at the end of the test.
#   class:    the fixture is destroyed during teardown of the last test in the class.
#   module:   the fixture is destroyed during teardown of the last test in the module.
#   package:  the fixture is destroyed during teardown of the last test in the package.
#   session:  the fixture is destroyed at the end of the test session.
#
####################################################################################################

####################################################################################################

from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers

####################################################################################################
####################################################################################################

@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()

####################################################################################################
####################################################################################################

@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

####################################################################################################

@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)

####################################################################################################

@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
