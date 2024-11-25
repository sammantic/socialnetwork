from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.db.models.memory import Memory
from app.schemas.memory_schema import MemoryCreate, MemoryUpdate


def service_get_all_memory_family(db: Session, family_id: int):
    """
    get all memory of a family

    :param db: database connection
    :param family_id: ID of a family

    :return:
    None or List of object
    """
    return db.query(Memory).filter(Memory.family_environment_id == family_id).all()


def service_get_memory_family_individual(db: Session, family_id: int, individual_id: int):
    """
    Get memory of a specific individual and a specific family with basic details

    :param db: database connection
    :param family_id: ID of a family
    :param individual_id: ID of an individual

    :return:
    List of object
    """

    return db.query(Memory).filter(Memory.individual_id == individual_id,
                                   Memory.family_environment_id == family_id).all()


def service_get_memory_family_individual_full(db: Session, family_id: int, individual_id: int):
    """
    Get memory of a specific individual and a specific family with full details

    :param db: database connection
    :param family_id: ID of a family
    :param individual_id: ID of an individual

    :return:
    List of object
    """

    db_query = db.query(Memory).options(
        joinedload(Memory.individual),
        joinedload(Memory.family_environment)
    ).filter(
        Memory.individual_id == individual_id,
        Memory.family_environment_id == family_id
    ).all()

    return db_query


def service_create_memory(db: Session, memory: MemoryCreate):
    """
    Create a memory

    :param db: database connection
    :param memory: pydantic schema of a memory
    :return:
    None or object of a created memory
    """
    try:
        memory_create = Memory(family_environment_id=memory.family_environment_id,
                               individual_id=memory.individual_id,
                               text=memory.text)
        db.add(memory_create)
        db.commit()
        db.refresh(memory_create)
        return memory_create
    except IntegrityError:
        db.rollback()


def service_get_memory_by_id(db: Session, memory_id: int):
    """
    get memory by id

    :param db: database connection
    :param memory_id: ID of a memory
    :return:
    None or object of memory
    """

    return db.query(Memory).filter(Memory.memory_id == memory_id).first()


def service_update_memory_by_id(db: Session, memory_id: int, memory: MemoryUpdate):
    """
    Update memory by ID

    :param db: database connection
    :param memory_id: ID of a memory
    :param memory: pydantic schema of a memory
    :return:
    None or object of updated memory
    """

    try:
        db_query = db.query(Memory).filter(Memory.memory_id == memory_id)
        db_query.update(memory.model_dump())
        db.commit()
        return db_query.first()
    except IntegrityError:
        db.rollback()


def service_delete_memory_by_id(db: Session, memory_id: int):
    """
    delete a memory

    :param db: database connection
    :param memory_id: ID of a memory
    :return:
    None
    """
    db_query = db.query(Memory).filter(Memory.memory_id == memory_id)
    db_query.delete()
    db.commit()