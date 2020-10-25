# Fixme: naming !!!
#  obj_in
#  donator

####################################################################################################

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CrudBase
from app.models.donation import Donator, Donation
from app.schemas.donation import DonatorCreate, DonatorUpdate, DonationBase, DonationCreate, DonationUpdate

####################################################################################################

class CrudDonator(CrudBase[Donator, DonatorCreate, DonatorUpdate]):

    ##############################################

    def create(
        self, db: Session, *, obj_in: DonatorCreate
    ) -> Donator:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    ##############################################

    # def get_multi_by_donator(
    #     self, db: Session, *, donator_id: int, skip: int = 0, limit: int = 100
    # ) -> List[Donator]:
    #     return (
    #         db.query(self.model)
    #         .filter(Donator.donator_id == donator_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

####################################################################################################

donator = CrudDonator(Donator)

####################################################################################################

class CrudDonation(CrudBase[Donation, DonationCreate, DonationUpdate]):

    ##############################################

    def create(
        self, db: Session, *, obj_in: DonationCreate
    ) -> Donation:
        # print(type(obj_in), obj_in)
        #  <class 'app.schemas.donation.DonationCreate'> 
        #  date=datetime.datetime(2020, 10, 25, 19, 2, 50, 153000, tzinfo=datetime.timezone.utc)
        #  int_amount=0
        #  donator_type=<DonatorType.individual: 1>
        #  name='string'
        #  email='user@example.com'
        # obj_in_data = jsonable_encoder(obj_in)
        # print(type(obj_in_data), obj_in_data)
        #  <class 'dict'>
        #  {'date': '2020-10-25T19:02:50.153000+00:00', 'int_amount': 0, 'donator_type': 1, 'name': 'string', 'email': 'user@example.com'}

        _ = obj_in.dict()
        donation_create = DonationBase(**_)
        # donation_create = DonationBase.construct(**_)
        print(donation_create)
        donator_create = DonatorCreate(**_)
        print(donator_create)
        obj_in_data = jsonable_encoder(donation_create)

        # print(type(donator_create), donator_create)
        #  <class 'app.schemas.donation.DonatorCreate'>
        #  donator_type=<DonatorType.individual: 1> name='string' email='user@example.com'

        # Fixme: must check if it exists !
        db_donator = donator.create(db, obj_in=donator_create)
        db_obj = self.model(**obj_in_data, donator_id=db_donator.id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    ##############################################

    # def get_multi_by_donator(
    #     self, db: Session, *, donator_id: int, skip: int = 0, limit: int = 100
    # ) -> List[Donation]:
    #     return (
    #         db.query(self.model)
    #         .filter(Donation.donator_id == donator_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

####################################################################################################

donation = CrudDonation(Donation)
