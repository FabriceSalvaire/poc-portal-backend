####################################################################################################

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from ..models.donation import DonatorType, PaymentStatus

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
    pass

####################################################################################################

# Properties properties stored in DB
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
    pass

####################################################################################################

# Properties to receive on donation update
class DonationUpdate(DonationBase):
    pass

####################################################################################################

# Properties shared by models stored in DB
class DonationInDbBase(DonationBase):
    id: int
    donator_id: int
    payment_status: PaymentStatus

    class Config:
        orm_mode = True

####################################################################################################

# Properties to return to client
class Donation(DonationInDbBase):
    pass

####################################################################################################

# Properties properties stored in DB
class DonationInDb(DonationInDbBase):
    pass
