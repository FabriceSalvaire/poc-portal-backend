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

from pydantic import BaseModel, EmailStr

from ..models.donation import DonatorType, PaymentStatus

####################################################################################################

# Donation = ForwardRef('Donation')

####################################################################################################

# Shared properties
class DonatorBase(BaseModel):
    donator_type: DonatorType
    name: str
    email: EmailStr

####################################################################################################

# Properties to receive on donator creation
class DonatorCreate(DonatorBase):
    pass

####################################################################################################

# Properties to receive on donator update
class DonatorUpdate(DonatorBase):
    pass

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
class DonationBase(BaseModel):
    date: datetime
    int_amount: int

####################################################################################################

# Properties to receive on donation creation
class DonationCreate(DonatorBase, DonationBase):
    callback_url: Optional[str] = None   # else use "Refere" HTTP header
    success_suffix_url: Optional[str] = "/success.html"
    cancel_suffix_url: Optional[str] = "/cancel.html"

####################################################################################################

# Properties to receive on donation update
class DonationUpdate(DonationBase):
    pass

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
