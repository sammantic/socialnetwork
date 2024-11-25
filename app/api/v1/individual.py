from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.exception_schema import ExceptionSchema
from app.services.individuals import (service_get_all_individuals,
                                      service_get_individual_by_name,
                                      service_get_individual_by_id,
                                      service_create_individual,
                                      service_update_individual,
                                      service_delete_individual)

from app.schemas.individual_schema import (IndividualResponse,
                                           IndividualCreate,
                                           IndividualUpdate)

router = APIRouter(
    prefix="/individual",
    tags=["individual"]
)


@router.get('/',
            response_model=List[IndividualResponse],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve an individual by id")
async def get_individual(db: Session = Depends(get_db)):
    """
    Retrieve all individual
    :parameter:
    db: Database connection

    :return:
    List[IndividualResponse]: List of all individuals
    """

    res = service_get_all_individuals(db=db)
    if res:
        return res
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post('/',
             response_model=IndividualResponse,
             responses={
                 status.HTTP_409_CONFLICT: {"model": ExceptionSchema}
             },
             status_code=status.HTTP_201_CREATED,
             description="Create an individual"
             )
async def create_individual(individual_create: IndividualCreate, db: Session = Depends(get_db)):
    """
    Create an individual
    :parameter:
    individual_create: pydantic schema of creating individual
    db: database connection

    :return:
    IndividualResponse: pydantic schema of the updated data
    """

    res = service_get_individual_by_name(db=db, name=individual_create.name)
    if res:  # check if the individual is already exits
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Individual already exists",
        )
    res = service_create_individual(db=db, individual=individual_create)
    return res


@router.put('/{individual_id}',
            response_model=IndividualResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
                status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema}
            },
            status_code=status.HTTP_201_CREATED,
            description="Update an individual by id")
async def update_individual(individual_id: int, individual_update: IndividualUpdate,
                            db: Session = Depends(get_db)):
    """
    Update an individual
    :parameter:
    individual_id: ID of an individual
    individual_update: pydantic schema of individual data
    db: database connection

    :return:
    IndividualResponse: pydantic schema of update data
    """

    res = service_get_individual_by_id(db=db, individual_id=individual_id)
    if res:  # check if the individual is already exits
        res_update = service_update_individual(db=db, individual_id=individual_id, individual=individual_update)

        # TODO: Decoupling the update errors
        if res_update:  # fails if the individual name is already used
            return res_update

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The individual name already used"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The individual not found"
    )


@router.delete('/{individual_id}',
               responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
               status_code=status.HTTP_200_OK,
               description="Delete an individual by id")
async def delete_individual(individual_id: int, db: Session = Depends(get_db)):
    """
    Delete an individual
    :parameter:
    individual_id: ID of an individual
    db: database connection

    :return:
    {"message": "The individual deleted"}: confirmation message
    """

    res = service_get_individual_by_id(db=db, individual_id=individual_id)
    if res:  # check if the individual is already exits
        service_delete_individual(db=db, individual_id=individual_id)
        return {"message": "The individual deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The individual not found"
    )
