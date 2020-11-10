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
from typing import List, Optional, ForwardRef

from pydantic import BaseModel, EmailStr, constr, root_validator

from ..models.donation import DonatorType, DonationOccurrence, PaymentMethod, PaymentStatus

####################################################################################################

# Donation = ForwardRef('Donation')

####################################################################################################

# Shared properties
class DonatorBase(BaseModel):
    donator_type: DonatorType
    email: EmailStr
    name: str
    forname: Optional[str] = None  # null for organisation !
    address: str
    complement: Optional[str] = None
    zip_code: str
    country_code3: constr(regex=r'^[A-Z][A-Z][A-Z]$')

    @root_validator
    def check_forname(cls, values):
        donator_type = values.get('donator_type')
        forname = values.get('forname')
        if donator_type == DonatorType.individual and not forname:
            raise ValueError('forname is required for individual')
        return values

####################################################################################################

# Properties to receive on donator creation
class DonatorCreate(DonatorBase):
    pass

####################################################################################################

# Properties to receive on donator update
class DonatorUpdate(BaseModel):
    email: EmailStr = None
    name: str = None
    forname: Optional[str] = None
    address: str = None
    complement: Optional[str] = None
    zip_code: str = None
    country_code3: constr(regex=r'^[A-Z][A-Z][A-Z]$') = None

####################################################################################################

# Properties shared by models stored in DB
class DonatorInDbBase(DonatorBase):
    id: int

    class Config:
        orm_mode = True

####################################################################################################

# Properties to return to client
class Donator(DonatorInDbBase):
    donations: List['DonationInDbBase'] # Take care to recursion

####################################################################################################

# Properties stored in DB
class DonatorInDb(DonatorInDbBase):
    pass

####################################################################################################
####################################################################################################

# Shared properties
class DonationBase(DonatorBase):   # BaseModel
    date: datetime
    donation_occurrence: DonationOccurrence   # = DonationOccurrence.once
    int_amount: int
    payment_method: PaymentMethod   # = PaymentMethod.card

####################################################################################################

# Properties to receive on donation creation
class DonationCreate(DonationBase):
    callback_url: Optional[str] = None   # else use "Refere" HTTP header
    success_suffix_url: Optional[str] = "/success.html"
    cancel_suffix_url: Optional[str] = "/cancel.html"
    captcha: str

####################################################################################################

# Properties to receive on donation update
class DonationUpdate(BaseModel):
    payment_status: PaymentStatus = None

####################################################################################################

# Properties shared by models stored in DB
class DonationInDbBase(DonationBase):
    id: int
    # donator_id: int
    payment_status: PaymentStatus
    stripe_session_id: str

    class Config:
        orm_mode = True

####################################################################################################

# Properties to return to client
class Donation(DonationInDbBase):
    donator: DonatorInDbBase # Take care to recursion

####################################################################################################

# Properties stored in DB
class DonationInDb(DonationInDbBase):
    pass

####################################################################################################

Donator.update_forward_refs()
