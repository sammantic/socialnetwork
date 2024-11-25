from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.exception_schema import ExceptionSchema
from app.services.family_membership import (service_get_all_family_membership,
                                            service_get_family_membership,
                                            service_get_family_members_by_family,
                                            service_create_family_membership,
                                            service_get_family_by_membership_id,
                                            service_update_family_membership,
                                            service_delete_family_membership, service_count_families_for_individual)

from app.schemas.family_member_schema import (FamilyMemberBasicResponse,
                                              FamilyMemberCreate,
                                              FamilyMemberUpdate,
                                              FamilyMemberFullResponse,
                                              FamilyMemberInFamily)
from app.services.patient import service_get_patient_by_id, service_search_for_patients

router = APIRouter(
    prefix="/familymember",
    tags=["family member"]
)


@router.get('/',
            response_model=List[FamilyMemberFullResponse],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve a families memberships")
def get_family_member(db: Session = Depends(get_db)):
    """
    Get all families memberships

    :param db: database connection

    :return:
    List[FamilyMemberFullResponse]: list of families memberships
    """

    res = service_get_all_family_membership(db=db)

    if res:  # check if there is a family membership
        return res

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.get('/{family_name}',
            response_model=FamilyMemberInFamily,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve all members in family"
            )
def get_family_member_by_family(family_name: str, db: Session = Depends(get_db)):
    """
    Get all members in a family by family name

    :param family_name: name of a family
    :param db: database connection

    :return:
    None or FamilyMemberInFamily: pydantic schema of all members in a family
    """

    res = service_get_family_members_by_family(db=db, family_name=family_name)
    if res:  # check if a family is exits
        return res

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="the family is not exist"
    )


@router.post('/',
             response_model=FamilyMemberBasicResponse,
             responses={
                 status.HTTP_409_CONFLICT: {"model": ExceptionSchema},
                 status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema}
             },
             status_code=status.HTTP_200_OK,
             description="Create new membership")
def create_family_membership(family_membership: FamilyMemberCreate, db: Session = Depends(get_db)):
    """
    Create a family membership

    :param family_membership: pydantic schema of family creation
    :param db: database connection

    :return:
    FamilyMemberBasicResponse: pydantic schema of family basic response
    """

    res = service_get_family_membership(db=db, family_membership=family_membership)
    if not res:  # check if a family membership is not exist

        is_patient = service_get_patient_by_id(db=db, patient_id=family_membership.individual_id)
        count = service_count_families_for_individual(db=db, individual_id=family_membership.individual_id)

        # Check if the membership for a patient
        # - an individual must not be a patient
        # - number of memberships is zero
        if is_patient and count >= 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The is patient and already has a family"
            )

        res_create = service_create_family_membership(db=db, family_membership=family_membership)

        # check values of the membership
        # - family_environment_id is a foreign key
        # - individual_id is a foreign key
        if res_create:
            return res_create

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad values"
        )

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="the membership already exits"
    )


@router.put('/{membership_id}',
            response_model=FamilyMemberBasicResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
                status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema}
            },
            status_code=status.HTTP_201_CREATED,
            description="Update membership by membership ID")
def update_family_membership(membership_id: int, membership: FamilyMemberUpdate, db: Session = Depends(get_db)):
    """
    Update a family membership

    :param membership_id: ID of a family membership
    :param membership: pydantic schema of family membership update
    :param db: database connection

    :return:
    FamilyMemberBasicResponse: pydantic schema of a family membership basic response
    """

    res = service_get_family_by_membership_id(db=db, membership_id=membership_id)

    if res:  # check if the membership is exits

        is_new_patient = service_search_for_patients(db=db, patient_ids=[membership.individual_id, res.individual_id])

        # check if the new individual and the old individual are patients
        # if it patient it means, it has a family
        # patient has only one family.

        if is_new_patient:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update not allowed, the new individual is patient"
            )

        res_update = service_update_family_membership(db=db,
                                                      membership_id=membership_id,
                                                      membership=membership)

        # check if the membership is exits
        # - family_environment_id is a foreign key
        # - individual_id is a foreign key
        if res_update:
            return res_update

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request, check values"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="the membership not found"
    )


@router.delete('/{membership_id}',
               responses={
                   status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
                   status.HTTP_409_CONFLICT: {"model": ExceptionSchema}
               },
               status_code=status.HTTP_200_OK,
               description="Delete membership by membership ID")
def delete_family_membership(membership_id: int, db: Session = Depends(get_db)):
    """
    delete a family membership

    :param membership_id: ID of a family membership
    :param db: database connection

    :return:
    {"message": "Membership is deleted"}: confirmation message
    """

    res = service_get_family_by_membership_id(db=db, membership_id=membership_id)

    if res:  # check if a family membership is exits

        is_patient = service_get_patient_by_id(db=db, patient_id=res.individual_id)

        # check if a family has a patient
        if is_patient:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Delete not allowed, the membership has patient"
            )

        service_delete_family_membership(db=db, membership_id=membership_id)
        return {"message": "Membership is deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="the membership not found"
    )
