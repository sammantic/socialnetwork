from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.individual import Individual
from app.schemas.individual_schema import IndividualCreate, IndividualUpdate


def service_get_all_individuals(db: Session):
    """
    Get all individuals
    :parameter:
    db: database connection

    :return:
    db_individuals: None or object of individuals
    """

    db_individuals = db.query(Individual).all()
    return db_individuals


def service_get_individual_by_name(db: Session, name: str):
    """
    Get an individual by name
    :param db: database connection
    :param name: name of an individual

    :return:
    None or an individual object
    """
    return db.query(Individual).filter(Individual.name == name).first()


def service_get_individual_by_id(db: Session, individual_id: int):
    """
    Get an individual by ID

    :param db: db connection
    :param individual_id: an individual ID
    :return:
    None or and individual object
    """

    return db.query(Individual).filter(Individual.individual_id == individual_id).first()


def service_create_individual(db: Session, individual: IndividualCreate):
    """
    Create an individual

    :param db: database connection
    :param individual: Pydantic schema of individual create

    :return:
    None or the created data of an individual
    """

    db_individual = Individual(name=individual.name,
                               date_of_birth=individual.date_of_birth,
                               other_details=individual.other_details)
    db.add(db_individual)
    db.commit()
    db.refresh(db_individual)
    return db_individual


def service_update_individual(db: Session, individual_id: int, individual: IndividualUpdate):
    """
    Update an individual

    :param db: database connection
    :param individual_id: ID of an individual
    :param individual: pydantic schema of individual update

    :return:
    None or the updated data of individual
    """

    try:
        db_query = db.query(Individual).filter(Individual.individual_id == individual_id)
        db_query.update(individual.model_dump())
        db.commit()
        return db_query.first()
    except IntegrityError:
        db.rollback()


def service_delete_individual(db: Session, individual_id: int):
    """
    Delete an individual

    :param db: database connection
    :param individual_id: ID of an individual

    :return:
    None
    """

    # TODO: handle failure of the deletion
    db_query = db.query(Individual).filter(Individual.individual_id == individual_id)
    db_query.delete()
    db.commit()

