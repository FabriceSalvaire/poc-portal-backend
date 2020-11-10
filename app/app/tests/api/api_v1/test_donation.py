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

from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.data.country import country_db
from app.schemas.donation import DonatorCreate, DonatorUpdate, DonationCreate, DonationUpdate
from app.tests.utils.utils import random_email, random_lower_string

# from app.tests.utils.donation import create_random_donation
from app.tests.crud.test_donation import create_random_donation

####################################################################################################

def test_create_donation(
    client: TestClient, db: Session
) -> None:
    country = 'France'
    data = dict(
        donator_type="individual", # DonatorType.individual
        email=random_email(),
        name=random_lower_string(),
        forname=random_lower_string(),
        address=random_lower_string(),
        complement=random_lower_string(),
        zip_code=random_lower_string(),
        country_code3=country_db[country].code3,
        date=datetime.now().isoformat(),
        donation_occurrence="once",   # DonationOccurrence.once
        int_amount=1000,
        payment_method="card",   # PaymentMethod.card
        callback_url="http://localhost:3000/",
        success_suffix_url="/success.html",
        cancel_suffix_url="/cancel.html",
        captcha=random_lower_string(),
    )
    response = client.post(
        f"{settings.API_V1_STR}/donations/", json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == data["email"]
    assert len(content["stripe_session_id"])
    assert "donator" in content

####################################################################################################

def test_read_donation(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    donation = create_random_donation(db)
    response = client.get(
        f"{settings.API_V1_STR}/donations/{donation.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == donation.id
    assert content["email"] == donation.email
