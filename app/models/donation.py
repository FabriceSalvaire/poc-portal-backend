####################################################################################################

__all__ = ['DonatorType', 'PaymentStatus', 'Donator', 'Donation']

####################################################################################################

# from typing import TYPE_CHECKING
from enum import IntEnum

from sqlalchemy import (
    Column, ForeignKey,
    Boolean, Enum, Integer, String, DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.base_class import Base

####################################################################################################

class DonatorType(IntEnum):
    individual = 1   # means "particulier" in French

class PaymentStatus(IntEnum):
    pending = 0
    done = 1

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
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    # currency is € ???

    donator_id = Column(Integer, ForeignKey("donator.id"))
    donator = relationship("Donator", back_populates="donations")

    ##############################################

    @hybrid_property
    def float_amount(self):
        return float(self.int_amount) / 100
