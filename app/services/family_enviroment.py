from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.family_environment import FamilyEnvironment
from app.schemas.family_environment_schema import FamilyEnvironmentCreate, FamilyEnvironmentUpdate


def service_get_all_families(db: Session):
    """
    Get all families
    :param db: database connection

    :return:
    None or object of families
    """

    db_family = db.query(FamilyEnvironment).all()
    return db_family


def service_get_family_by_name(db: Session, name: str):
    """
    Get a family by name

    :param db: database connection
    :param name: name of a family

    :return:
    None or object of a family
    """

    return db.query(FamilyEnvironment).filter(FamilyEnvironment.name == name).first()


def service_get_family_by_id(db: Session, family_id: int):
    """
    Get a family by ID

    :param db: Database connection
    :param family_id: ID of a family

    :return:
    None or object of a family
    """

    return db.query(FamilyEnvironment).filter(FamilyEnvironment.family_environment_id == family_id).first()


def service_create_family(db: Session, family: FamilyEnvironmentCreate):
    """
    Create of a family

    :param db: database connection
    :param family: pydantic schema of family creation

    :return:
    None or object of a family
    """

    db_family = FamilyEnvironment(name=family.name)
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family


def service_update_family(db: Session, family_id: int, family: FamilyEnvironmentUpdate):
    """
    Update a family

    :param db: database connection
    :param family_id: ID of a family
    :param family: pydantic schema of updating a family

    :return:
    None or object of updated family
    """

    try:
        db_query = db.query(FamilyEnvironment).filter(FamilyEnvironment.family_environment_id == family_id)
        db_query.update(family.model_dump())
        db.commit()
        return db_query.first()
    except IntegrityError:
        db.rollback()


def service_delete_family(db: Session, family_id: int):
    """
    Delete a family

    :param db: database connection
    :param family_id: ID of a family

    :return:
    None
    """

    # TODO: handle failure of the deletion
    db_query = db.query(FamilyEnvironment).filter(FamilyEnvironment.family_environment_id == family_id)
    db_query.delete()
    db.commit()
