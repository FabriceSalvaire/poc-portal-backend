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
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.base_class import Base
from app.stripe import PaymentStatus

####################################################################################################

class DonatorType(StrEnum):
    individual = auto()   # means "particulier" in French

####################################################################################################

class Donator(Base):

    # Fixme: handle case where a donator come back but provides different data like email, or due to
    #   typos

    id = Column(Integer, primary_key=True, index=True)
    donator_type = Column(Enum(DonatorType))
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)   # forname name ???
    # ...

    donations = relationship("Donation", back_populates="donator")

####################################################################################################

class Donation(Base):

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=False), nullable=False)
    int_amount = Column(Integer, nullable=False)   # amount € *100 to fit an int
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.incomplete)
    # currency is € ???
    stripe_session_id = Column(String, nullable=True, default=None)

    donator_id = Column(Integer, ForeignKey("donator.id"))
    donator = relationship("Donator", back_populates="donations")

    ##############################################

    @hybrid_property
    def float_amount(self):
        return float(self.int_amount) / 100
