from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.exception_schema import ExceptionSchema
from app.services.individuals import service_get_individual_by_id
from app.services.family_enviroment import service_get_family_by_id

from app.services.memory import (service_get_all_memory_family,
                                 service_get_memory_family_individual,
                                 service_get_memory_family_individual_full,
                                 service_create_memory,
                                 service_get_memory_by_id, service_update_memory_by_id, service_delete_memory_by_id)

from app.schemas.memory_schema import (MemoryBasicResponse,
                                       MemoryFullResponse,
                                       MemoryCreate,
                                       MemoryUpdate)

router = APIRouter(
    prefix="/memory",
    tags=["memory"]
)


@router.get('/{family_id}',
            response_model=List[MemoryBasicResponse],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None}
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve a memory by family")
async def get_memory(family_id: int, db: Session = Depends(get_db)):
    """
    Get memory

    :param family_id: ID of a family
    :param db: database connection
    :return:
    List[MemoryBasicResponse]: list of memory
    """

    ret = service_get_all_memory_family(db=db, family_id=family_id)
    if ret:  # check if there are memories
        return ret

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.get('/{family_id}/{individual_id}/full',
            response_model=List[MemoryFullResponse],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
                status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema}
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve a memory by family and individual")
async def get_memory_family_individual_full(individual_id: int, family_id: int, db: Session = Depends(get_db)):
    """
    Get all memories with full response of a specific individual and a specific family

    :param individual_id: ID of an individual
    :param family_id: ID of a family
    :param db: database connection

    :return:
    List[MemoryFullResponse]: list of memories
    """

    ret_individual = service_get_individual_by_id(db=db, id=individual_id)
    ret_family = service_get_family_by_id(db=db, id=family_id)

    # TODO: check if there is a membership

    # check if an individual and a family are exists
    if ret_individual and ret_family:
        ret = service_get_memory_family_individual_full(db=db, family_id=family_id, individual_id=individual_id)

        if ret:
            return ret
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Bad request, check values"
    )


@router.get('/{family_id}/{individual_id}',
            response_model=List[MemoryBasicResponse],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
                status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema}
            },
            status_code=status.HTTP_200_OK,
            description="Retrieve a memory by family and individual")
async def get_memory_family_individual(individual_id: int, family_id: int, db: Session = Depends(get_db)):
    """
    Get all memories with basic response of a specific individual and a specific family

    :param individual_id: ID of an individual
    :param family_id: ID of a family
    :param db: database connection

    :return:
    List[MemoryFullResponse]: list of memories
    """

    ret_individual = service_get_individual_by_id(db=db, id=individual_id)
    ret_family = service_get_family_by_id(db=db, id=family_id)

    # TODO: check if there is a membership

    # check if an individual and a family are exists
    if ret_individual and ret_family:
        ret = service_get_memory_family_individual(db=db, family_id=family_id, individual_id=individual_id)
        if ret:
            return ret
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Bad request, check values"
    )


@router.post('/',
             response_model=MemoryBasicResponse,
             responses={
                 status.HTTP_409_CONFLICT: {"model": ExceptionSchema}
             },
             status_code=status.HTTP_201_CREATED,
             description="Create a memory")
async def create_memory(memory: MemoryCreate, db: Session = Depends(get_db)):
    """
    Create a memory

    :param memory: pydantic of create memory
    :param db: database connection
    :return:
    MemoryBasicResponse: pydantic of memory basic response
    """

    ret = service_create_memory(db=db, memory=memory)

    # validate the creation
    if ret:
        return ret

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Please check the values"
    )


@router.put('/{memory_id}',
            response_model=MemoryBasicResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}
            },
            status_code=status.HTTP_201_CREATED,
            description="Update a memory by id")
async def update_memory(memory_id: int, text: MemoryUpdate, db: Session = Depends(get_db)):
    """
    Update a memory by id

    :param memory_id: ID of a memory
    :param text: text of a memory
    :param db: database connection

    :return:
    MemoryBasicResponse: pydantic basic response of memory
    """

    ret = service_get_memory_by_id(db=db, memory_id=memory_id)

    if ret:  # check if the memory exist
        ret_update = service_update_memory_by_id(db=db, memory_id=memory_id, memory=text)
        return ret_update

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The memory not found"
    )


@router.delete('/{memory_id}',
               responses={
                   status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}
               },
               status_code=status.HTTP_200_OK,
               description="Delete a memory by id")
async def delete_memory(memory_id: int, db: Session = Depends(get_db)):
    """
    Delete a memory by id

    :param memory_id: ID of a memory
    :param db: database connection

    :return:
    None
    """

    ret = service_get_memory_by_id(db=db, memory_id=memory_id)

    # check if a memory exist
    if ret:
        service_delete_memory_by_id(db=db, memory_id=memory_id)
        return {"message": "memory deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Memory not found"
    )
