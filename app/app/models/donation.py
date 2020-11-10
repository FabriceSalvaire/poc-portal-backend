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

__all__ = ['DonatorType', 'Donator', 'Donation']

####################################################################################################

# from typing import TYPE_CHECKING
from enum import auto   # IntEnum

from fastapi_utils.enums import StrEnum

from sqlalchemy import (
    Column, ForeignKey,
    Boolean, Enum, Integer, String, DateTime,
    # JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.data.country import country_db
from app.db.base_class import Base
from app.stripe import PaymentStatus   # Fixme: generic ???

####################################################################################################

class DonationOccurrence(StrEnum):
    once = auto()
    monthly = auto()

class DonatorType(StrEnum):
    individual = auto()   # means "particulier" in French
    organisation = auto()

class PaymentMethod(StrEnum):
    card = auto()   # means "particulier" in French
    bank_transfer = auto()
    check = auto()
    paypal = auto()

####################################################################################################

class DonatorMixin:

    email = Column(String, unique=True, index=True, nullable=False)

    donator_type = Column(Enum(DonatorType), default=DonatorType.individual)

    name = Column(String, index=True, nullable=False)   # for organisation and individual
    forname = Column(String, index=True, nullable=True)   # null for organisation !

    address = Column(String, nullable=False)
    complement = Column(String, nullable=True, default=None)
    zip_code = Column(String, nullable=False)
    country_code3 = Column(String(length=3), nullable=False)  # ISO code3

    ##############################################

    @hybrid_property
    def full_name(self):
        if self.forname:
            return f"{self.name} {self.forname}"
        else:
            return self.name

    @hybrid_property
    def country(self):
        return country_db[self.country_code3].name

    @hybrid_property
    def full_address(self):
        if self.complement:
            return f"{self.address} / {self.complement} / {self.zip_code} {self.country}"
        else:
            return f"{self.address} / {self.zip_code} {self.country}"

####################################################################################################

class Donator(DonatorMixin, Base):

    # Fixme: handle case where a donator come back but provides different data like email, or due to
    #   typos

    id = Column(Integer, primary_key=True, index=True)

    donations = relationship("Donation", back_populates="donator")

####################################################################################################

class Donation(DonatorMixin, Base):

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=False), nullable=False)

    donation_occurrence = Column(Enum(DonationOccurrence), default=DonationOccurrence.once)
    int_amount = Column(Integer, nullable=False)   # amount € *100 to fit an int

    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.card)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.incomplete)

    # for Stripe
    stripe_session_id = Column(String, nullable=True, default=None)

    # currency is € ???
    # check_id
    # lettering lettrage

    donator_id = Column(Integer, ForeignKey("donator.id"))
    donator = relationship("Donator", back_populates="donations")

    ##############################################

    @hybrid_property
    def float_amount(self):
        return float(self.int_amount) / 100
