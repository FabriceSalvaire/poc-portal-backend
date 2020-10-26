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
