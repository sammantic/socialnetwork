from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.exception_schema import ExceptionSchema
from app.services.family_membership import service_count_families_for_individual

from app.services.patient import (service_get_all_patient,
                                  service_get_patient,
                                  service_create_patient,
                                  service_get_family_patient_by_id,
                                  service_get_patient_by_id,
                                  service_update_patient,
                                  service_delete_patient,
                                  service_get_all_memories_of_all_individual_by_patient)

from app.schemas.patient_schema import (PatientBasicResponse,
                                        PatientCreate,
                                        PatientUpdate,
                                        PatientMemory)

router = APIRouter(
    prefix="/patient",
    tags=["patient"]
)


@router.get('/',
            response_model=List[PatientBasicResponse],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None}
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve a patient by id")
async def get_patient(db: Session = Depends(get_db)):
    """
    Get all patient

    :param db: database connection

    :return:
    List[PatientBasicResponse]: List of all patient
    """

    res = service_get_all_patient(db)
    if res:  # check if there are patients
        return res

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.get('/memory/{patient_id}',
            response_model=List[PatientMemory],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None}
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve memories of all individual for a given patient by id")
async def get_memory_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve memories of all individual for a given patient by ID

    :param patient_id: ID of a patient
    :param db: database connection

    :return:
    List[PatientMemory]: List of memories
    """

    res = service_get_all_memories_of_all_individual_by_patient(db=db, patient_id=patient_id)

    if res:  # Check if memories are exists
        return res

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post('/',
             response_model=PatientBasicResponse,
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
                 status.HTTP_409_CONFLICT: {"model": ExceptionSchema}
             },
             status_code=status.HTTP_201_CREATED,
             description="Create a patient")
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """
    Create a patient

    :param patient: pydantic schema of patient creation
    :param db: database connection

    :return:
    PatientBasicResponse: pydantic schema of patient basic response
    """

    res = service_get_patient(db=db, patient=patient)

    if not res:  # check if the patient is exits

        patient_family = service_get_family_patient_by_id(db=db, family_id=patient.family_environment_id)

        # TODO: optimize the search criteria of patient, in one query
        if not patient_family:  # check if the patient has family

            count = service_count_families_for_individual(db=db, individual_id=patient.patient_id)

            # check number of families
            # - patient must have only one family
            if count == 1:

                patient_create = service_create_patient(db=db, patient=patient)

                # check the creation of a patient
                # - patient_id: must be a foreign key in Individual
                # - family_environment_id: must be a foreign key in family environment
                if patient_create:
                    return patient_create

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request, check values"
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Family is full"
        )

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Patient already exist"
    )


@router.put('/',
            response_model=PatientUpdate,
            responses={
                status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
                status.HTTP_409_CONFLICT: {"model": ExceptionSchema},
                status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
            },
            status_code=status.HTTP_200_OK,
            description="Update a patient by id")
async def update_patient(patient: PatientUpdate, db: Session = Depends(get_db)):
    """
    Update patient

    :param patient: pydantic schema of updating a patient
    :param db: database connection

    :return:
    PatientUpdate: pydantic schema of updating a patient
    """

    res = service_get_patient(db=db, patient=patient)
    if res:  # check if the patient_id is valid
        patient_family = service_get_family_patient_by_id(db=db, family_id=patient.family_environment_id)
        if not patient_family:  # check if the family is already has patient
            count = service_count_families_for_individual(db=db, individual_id=patient.patient_id)
            if count == 1:  # check if the patient has more than one family membership
                ret_update_patient = service_update_patient(db=db, patient=patient)
                if ret_update_patient:  # check if the update done
                    return ret_update_patient
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bad request, bad values"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request, individual has more than family membership"
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Family is full"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Patient not found"
    )


@router.delete('/{patient_id}',
               responses={
                   status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}
               },
               status_code=status.HTTP_200_OK,
               description="Delete a patient by id")
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Delete a patient by id

    :param patient_id: ID of a patient
    :param db: database connection

    :return:
    {"message": "delete patient"}: confirmation message
    """

    res = service_get_patient_by_id(db=db, patient_id=patient_id)
    if res:
        service_delete_patient(db=db, patient_id=patient_id)
        return {"message": "delete patient"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The patient not found"
    )
