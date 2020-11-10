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
import random

import pytest

import pydantic

from sqlalchemy.orm import Session

from app import crud
from app.models.donation import DonatorType, DonationOccurrence, PaymentMethod, PaymentStatus
from app.schemas.donation import DonatorCreate, DonatorUpdate, DonationCreate, DonationUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string
from app.data.country import country_db

####################################################################################################

excluded_donation_fields = ("success_suffix_url", "cancel_suffix_url", "captcha")

####################################################################################################

def make_donator():
    country = 'France'
    return (
        dict(
            donator_type=DonatorType.individual,
            email=random_email(),
            name=random_lower_string(),
            forname=random_lower_string(),
            address=random_lower_string(),
            complement=random_lower_string(),
            zip_code=random_lower_string(),
            country_code3=country_db[country].code3,
        ),
        country,
    )

####################################################################################################

def make_donation():
    fields, country = make_donator()
    return (
        dict(
            **fields,
            date=datetime.now(),
            donation_occurrence=DonationOccurrence.once,
            int_amount=random.randrange(100, 10**6),
            payment_method=PaymentMethod.card,
            # callback_url=None,   # use referer
            success_suffix_url="/success.html",
            cancel_suffix_url="/cancel.html",
            captcha=random_lower_string(),
        ),
        country,
    )

####################################################################################################

def create_random_donation(db: Session) -> None:
    fields, country = make_donation()
    donation_in = DonationCreate(**fields)
    referer = "https://localhost"
    donation = crud.donation.create(db=db, obj_in=donation_in, referer=referer)
    return donation

####################################################################################################

def assert_fields(obj, fields, exclude=()):
    for key, value in fields.items():
        if key not in exclude:
            assert getattr(obj, key) == value

####################################################################################################

def assert_obj_fields(obj1, obj2, keys, exclude=()):
    for key in keys:
        if key not in exclude:
            assert getattr(obj1, key) == getattr(obj2, key)

####################################################################################################
####################################################################################################

#@pytest.mark.skip()
def test_create_donator(db: Session) -> None:
    fields, country = make_donator()
    donator_in = DonatorCreate(**fields)
    donator = crud.donator.create(db=db, obj_in=donator_in)
    assert_fields(donator, fields)
    assert donator.country == country

    # test optional
    fields['email'] = random_email()
    fields['complement'] = None
    donator_in = DonatorCreate(**fields)
    donator = crud.donator.create(db=db, obj_in=donator_in)
    assert donator.complement == None

    # test forname is required for individual
    with pytest.raises(pydantic.ValidationError):
        fields['email'] = random_email()
        del fields['forname']
        del fields['complement']
        donator_in = DonatorCreate(**fields)
        donator = crud.donator.create(db=db, obj_in=donator_in)

    # test organisation
    fields['email'] = random_email()
    fields['donator_type'] = DonatorType.organisation
    donator_in = DonatorCreate(**fields)
    donator = crud.donator.create(db=db, obj_in=donator_in)
    assert donator.donator_type == DonatorType.organisation

####################################################################################################

def test_create_donation(db: Session) -> None:
    fields, country = make_donation()
    donation_in = DonationCreate(**fields)
    referer = "https://localhost"
    donation = crud.donation.create(db=db, obj_in=donation_in, referer=referer)
    assert_fields(donation, fields, exclude=excluded_donation_fields)
    assert donation.country == country
    assert len(donation.stripe_session_id)
    assert donation.payment_status == PaymentStatus.incomplete
    assert donation.donator.email == fields["email"]

####################################################################################################

def test_get_donator(db: Session) -> None:
    fields, country = make_donator()
    donator_in = DonatorCreate(**fields)
    donator = crud.donator.create(db=db, obj_in=donator_in)
    stored_donator = crud.donator.get(db=db, id=donator.id)
    assert stored_donator
    assert donator.id == stored_donator.id
    assert_obj_fields(donator, stored_donator, fields.keys())

####################################################################################################

def test_get_donation(db: Session) -> None:
    fields, country = make_donation()
    donation_in = DonationCreate(**fields)
    referer = "https://localhost"
    donation = crud.donation.create(db=db, obj_in=donation_in, referer=referer)
    stored_donation = crud.donation.get(db=db, id=donation.id)
    assert stored_donation
    assert donation.id == stored_donation.id
    assert_obj_fields(donation, stored_donation, fields.keys(), exclude=excluded_donation_fields)

####################################################################################################

def test_update_donator(db: Session) -> None:
    fields, country = make_donator()
    donator_in = DonatorCreate(**fields)
    donator = crud.donator.create(db=db, obj_in=donator_in)
    name = random_lower_string()
    donator_update = DonatorUpdate(name=name)
    donator2 = crud.donator.update(db=db, db_obj=donator, obj_in=donator_update)
    assert donator.id == donator2.id
    assert donator.email == donator2.email
    assert donator2.name == name

####################################################################################################

def test_update_donation(db: Session) -> None:
    fields, country = make_donation()
    donation_in = DonationCreate(**fields)
    referer = "https://localhost"
    donation = crud.donation.create(db=db, obj_in=donation_in, referer=referer)
    donation_update = DonationUpdate(payment_status=PaymentStatus.succeeded)
    donation2 = crud.donation.update(db=db, db_obj=donation, obj_in=donation_update)
    assert donation.id == donation2.id
    assert donation.email == donation2.email
    assert donation2.payment_status == PaymentStatus.succeeded

####################################################################################################

def test_delete_donator(db: Session) -> None:
    fields, country = make_donator()
    donator_in = DonatorCreate(**fields)
    donator = crud.donator.create(db=db, obj_in=donator_in)
    donator2 = crud.donator.remove(db=db, id=donator.id)
    donator3 = crud.donator.get(db=db, id=donator.id)
    assert donator3 is None
    assert donator2.id == donator.id
    assert donator2.email == fields["email"]

####################################################################################################

def test_delete_donation(db: Session) -> None:
    fields, country = make_donation()
    donation_in = DonationCreate(**fields)
    referer = "https://localhost"
    donation = crud.donation.create(db=db, obj_in=donation_in, referer=referer)
    donation2 = crud.donation.remove(db=db, id=donation.id)
    donation3 = crud.donation.get(db=db, id=donation.id)
    assert donation3 is None
    assert donation2.id == donation.id
    assert donation2.email == fields["email"]
