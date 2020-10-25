####################################################################################################

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

####################################################################################################

router = APIRouter()

####################################################################################################

@router.get("/", response_model=List[schemas.Donation])
def read_donations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve donations.
    """
    # Fixme:
    if crud.user.is_superuser(current_user):
        donations = crud.donation.get_multi(db, skip=skip, limit=limit)
    else:
        donations = crud.donation.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return donations

####################################################################################################

@router.post("/", response_model=schemas.Donation)
def create_donation(
    *,
    db: Session = Depends(deps.get_db),
    donation_in: schemas.DonationCreate,
) -> Any:
    """
    Create new donation.
    """
    donation = crud.donation.create(db=db, obj_in=donation_in)
    return donation

####################################################################################################

# @router.put("/{id}", response_model=schemas.Donation)
# def update_donation(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     donation_in: schemas.DonationUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an donation.
#     """
#     donation = crud.donation.get(db=db, id=id)
#     if not donation:
#         raise HTTPException(status_code=404, detail="Donation not found")
#     if not crud.user.is_superuser(current_user) and (donation.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     donation = crud.donation.update(db=db, db_obj=donation, obj_in=donation_in)
#     return donation

####################################################################################################

@router.get("/{id}", response_model=schemas.Donation)
def read_donation(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get donation by ID.
    """
    donation = crud.donation.get(db=db, id=id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    if not crud.user.is_superuser(current_user) and (donation.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return donation

####################################################################################################

# @router.delete("/{id}", response_model=schemas.Donation)
# def delete_donation(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an donation.
#     """
#     donation = crud.donation.get(db=db, id=id)
#     if not donation:
#         raise HTTPException(status_code=404, detail="Donation not found")
#     if not crud.user.is_superuser(current_user) and (donation.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     donation = crud.donation.remove(db=db, id=id)
#     return donation
