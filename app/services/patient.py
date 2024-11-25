from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.schemas.patient_schema import (PatientCreate,
                                        PatientBasic,
                                        PatientUpdate)

from app.db.models.patient import Patient
from app.db.models.family_environment import FamilyEnvironment
from app.db.models.family_member import FamilyEnvironmentMember
from app.db.models.individual import Individual
from app.db.models.memory import Memory


def service_get_all_patient(db: Session):
    """
    Get all patient

    :param db: database connection
    :return:
    None or List of all patient
    """

    return db.query(Patient).all()


def service_get_family_patient_by_id(db: Session, family_id: int):
    """
    Get family patient by ID

    :param db: database connection
    :param family_id: ID of a family

    :return:
    None or object of patient
    """

    return db.query(Patient).filter(Patient.family_environment_id == family_id).first()


def service_get_patient_by_id(db: Session, patient_id: int):
    """
    Get patient by id

    :param db: database connection
    :param patient_id: ID of a patient

    :return:
    None or object of patient
    """

    return db.query(Patient).filter(Patient.patient_id == patient_id).first()


def service_search_for_patients(db: Session, patient_ids: list):
    """
    search for a list of patient IDs

    :param db: database connection
    :param patient_ids: patient IDs

    :return:
    None or List of patients
    """
    return db.query(Patient).filter(Patient.patient_id.in_(patient_ids)).all()


def service_get_all_memories_of_all_individual_by_patient(db: Session, patient_id: int):
    """
    Get all the memories of all individuals that exist with a patient across all families

    :param db: database connection
    :param patient_id: ID of a patient

    :return:
    None or List of memories
    """

    stmt = (
        select(Memory)
        .join(FamilyEnvironmentMember, Memory.individual_id == FamilyEnvironmentMember.individual_id)
        .join(Patient, Patient.family_environment_id == FamilyEnvironmentMember.family_environment_id)
        .filter(Patient.patient_id == patient_id)
    )

    memories = db.execute(stmt).scalars().all()

    return memories


def service_get_patient(db: Session, patient: PatientBasic):
    """
    Get patient

    :param db: database connection
    :param patient: pydantic schema of basic patient

    :return:
    None or object of a patient
    """

    return db.query(Patient).filter(Patient.patient_id == patient.patient_id).first()


def service_create_patient(db: Session, patient: PatientCreate):
    """
    Create a patient

    :param db: database connection
    :param patient: pydantic schema of a patient
    :return:
    None or object of a patient
    """

    try:
        db_patient = Patient(patient_id=patient.patient_id,
                             family_environment_id=patient.family_environment_id)
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    except IntegrityError:
        db.rollback()


def service_update_patient(db: Session, patient: PatientUpdate):
    """
    update a patient

    :param db: database connection
    :param patient: pydantic schema of updating patient
    :return:
    None or object of a patient
    """

    try:
        db_query = db.query(Patient).filter(Patient.patient_id == patient.patient_id)
        db_query.update(patient.model_dump())
        db.commit()
        return db_query.first()
    except IntegrityError:
        db.rollback()


def service_delete_patient(db: Session, patient_id: int):
    """
    Delete patient

    :param db: database connection
    :param patient_id: ID of a patient
    :return:
    None
    """
    db_query = db.query(Patient).filter(Patient.patient_id == patient_id)
    db_query.delete()
    db.commit()
    return True
