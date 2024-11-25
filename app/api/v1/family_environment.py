from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.exception_schema import ExceptionSchema
from app.services.family_enviroment import (service_get_all_families,
                                            service_get_family_by_name,
                                            service_get_family_by_id,
                                            service_create_family,
                                            service_update_family,
                                            service_delete_family)

from app.schemas.family_environment_schema import (FamilyEnvironmentResponse,
                                                   FamilyEnvironmentCreate,
                                                   FamilyEnvironmentUpdate)

router = APIRouter(
    prefix="/family",
    tags=["family environment"]
)


@router.get('/',
            response_model=List[FamilyEnvironmentResponse],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve a family environment by id")
async def get_family(db: Session = Depends(get_db)):
    """
    Retrieve a family environment by id

    :return:
    List[FamilyEnvironmentResponse]
    """

    res = service_get_all_families(db=db)
    if res:  # check if there are families
        return res

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post('/',
             response_model=FamilyEnvironmentResponse,
             responses={
                 status.HTTP_409_CONFLICT: {"model": ExceptionSchema}
             },
             status_code=status.HTTP_201_CREATED,
             description="Create a family environment"
             )
async def create_family(family_environment_create: FamilyEnvironmentCreate, db: Session = Depends(get_db)):
    """
    Create a family

    :param family_environment_create: pydantic schema of creating a family.
    :param db: database connection

    :return:
    FamilyEnvironmentResponse: pydantic schema of family response
    """

    res = service_get_family_by_name(db=db, name=family_environment_create.name)
    if res:  # check if family is exits
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="family already exists",
        )

    res = service_create_family(db=db, family=family_environment_create)
    return res


@router.put('/{family_id}',
            response_model=FamilyEnvironmentResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
                status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema}
            },
            status_code=status.HTTP_201_CREATED,
            description="Update a family environment by id")
async def update_family(family_id: int, family_update: FamilyEnvironmentUpdate,
                        db: Session = Depends(get_db)):
    """

    :param family_id: ID of a family
    :param family_update: pydantic schema of updating a family
    :param db: database connection

    :return:
     FamilyEnvironmentResponse: pydantic schema of family response
    """

    res = service_get_family_by_id(db=db, family_id=family_id)
    if res:  # check if the family exits

        res_update = service_update_family(db=db, family_id=family_id, family=family_update)

        # TODO: Decoupling the update errors
        if res_update:  # fail if the family name already used
            return res_update

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The family name already exists"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The family not found"
    )


@router.delete('/{family_id}',
               responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
               status_code=status.HTTP_200_OK,
               description="Delete a family environment by id")
async def delete_family(family_id: int, db: Session = Depends(get_db)):
    """
    Delete a family

    :param family_id: ID of a family
    :param db: database connection

    :return:
    {"message": "The individual deleted"}: confirmation message
    """

    res = service_get_family_by_id(db=db, family_id=family_id)
    if res:  # check if a family is exits
        service_delete_family(db=db, family_id=family_id)
        return {"message": "The individual deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The family not found"
    )
