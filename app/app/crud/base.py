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

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

####################################################################################################

# https://docs.python.org/3/library/typing.html#typing.TypeVar
# https://docs.python.org/3/library/typing.html#typing.Generic
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

####################################################################################################

class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    ##############################################

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    ##############################################

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get an item by id"""
        return db.query(self.model).filter(self.model.id == id).first()

    ##############################################

    def get_multi(
            self, db: Session,
            *,
            skip: int = 0,
            limit: int = 100,
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    ##############################################

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        print('CrudBase.create', type(obj_in), obj_in)
        obj_in_data = jsonable_encoder(obj_in)
        print('CrudBase.create', type(obj_in_data), obj_in_data)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)  # to update e.g. auto increment field like id
        return db_obj

    ##############################################

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        print('CrudBase.update', type(db_obj), db_obj, type(obj_in), obj_in)
        #  <class 'app.models.donation.Donation'> <app.models.donation.Donation object at 0x7fb93a45adc0>
        #  <class 'dict'> {'stripe_session_id': 'cs_test_KJhkmStOXoA5HIlKmropUY0D3k4NalCBhNvbiHAKb7aNtgA6i36aWbtP'}
        obj_data = jsonable_encoder(db_obj)   # Fixme: purpose ??? validation ??? only use keys
        print('CrudBase.update', type(obj_data), obj_data)
        #  <class 'dict'> {'donator_id': 2, 'payment_status': 'incomplete', 'date': '2020-10-26T14:24:12.709000', 'stripe_session_id': None, 'int_amount': 5000, 'id': 2}
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    ##############################################

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
