from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, joinedload

from app.db.models.family_member import FamilyEnvironmentMember
from app.db.models.family_environment import FamilyEnvironment

from app.schemas.family_member_schema import FamilyMemberCreate, FamilyMemberUpdate


def service_get_all_family_membership(db: Session):
    """
    Get all families memberships

    :param db: database connection

    :return:
    None or object of all families memberships
    """

    # query relation many-to-many
    return db.query(FamilyEnvironmentMember).options(
        joinedload(FamilyEnvironmentMember.individual),
        joinedload(FamilyEnvironmentMember.family_environment)
    ).all()


def service_get_family_members_by_family(db: Session, family_name: str):
    """
    Get all members in a family by family name

    :param db: database connection
    :param family_name: name of a family

    :return:
    None or object of all members in a family
    """

    # query all member in a family
    # query the details of each member from individual
    family = (
        db.query(FamilyEnvironment)
        .options(
            joinedload(FamilyEnvironment.members).joinedload(FamilyEnvironmentMember.individual)
        )
        .filter(FamilyEnvironment.name == family_name)
        .first()
    )

    return family


def service_get_family_membership(db: Session, family_membership: FamilyMemberCreate):
    """
    Get a family membership

    :param db: database connection
    :param family_membership: pydantic scheme of a family membership, I reused FamilyMemberCreate

    :return:
    None or an object of family membership
    """

    return db.query(FamilyEnvironmentMember).filter(
        FamilyEnvironmentMember.family_environment_id == family_membership.family_environment_id,
        FamilyEnvironmentMember.individual_id == family_membership.individual_id
    ).first()


def service_get_family_by_membership_id(db: Session, membership_id: int):
    """
    Get family membership by membership id

    :param db: database connection
    :param membership_id: ID of a membership

    :return:
    None or an object of family membership
    """

    return db.query(FamilyEnvironmentMember).filter(
        FamilyEnvironmentMember.family_environment_member_id == membership_id).first()


def service_create_family_membership(db: Session, family_membership: FamilyMemberCreate):
    """
    Create a family membership

    :param db: database
    :param family_membership: pydantic schema of family membership creation

    :return:
    None or an object of a family membership
    """

    try:
        db_membership = FamilyEnvironmentMember(family_environment_id=family_membership.family_environment_id,
                                                individual_id=family_membership.individual_id,
                                                role=family_membership.role)
        db.add(db_membership)
        db.commit()
        db.refresh(db_membership)
        return db_membership

    except IntegrityError as e:
        db.rollback()
        # Check if the IntegrityError is due to a unique constraint violation
        if 'violates unique constraint' in str(e.orig):
            return {"error": "A family membership is already exists."}
        else:
            return {"error": "An integrity error occurred."}
    except OperationalError as e:
        db.rollback()
        return {"error": "A database operational error occurred."}
    except Exception as e:
        db.rollback()
        return {"error": f"An unexpected error occurred: {str(e)}"}


def service_update_family_membership(db: Session, membership_id: int, membership: FamilyMemberUpdate):
    """
    Update a family membership

    :param db: database connection
    :param membership_id: ID of a family membership
    :param membership: pydantic schema of updating family membership

    :return:
    None or an object of family membership
    """

    try:
        db_update = db.query(FamilyEnvironmentMember).filter(
            FamilyEnvironmentMember.family_environment_member_id == membership_id)
        db_update.update(membership.model_dump())
        db.commit()
        return db_update.first()
    except IntegrityError as e:
        db.rollback()
        # Check if the IntegrityError is due to a unique constraint violation
        if 'violates unique constraint' in str(e.orig):
            return {"error": "A family membership already exists."}
        else:
            return {"error": "An integrity error occurred."}
    except OperationalError as e:
        db.rollback()
        return {"error": "A database operational error occurred."}
    except Exception as e:
        db.rollback()
        return {"error": f"An unexpected error occurred: {str(e)}"}


def service_delete_family_membership(db: Session, membership_id: int):
    """
    Delete a family membership

    :param db: database connection
    :param membership_id: ID of a family membership

    :return:
    None
    """

    # TODO: handle failure of the deletion
    try:
        db_query = db.query(FamilyEnvironmentMember).filter(
            FamilyEnvironmentMember.family_environment_member_id == membership_id)
        res_delete = db_query.delete()
        if res_delete == 0:
            return False
        else:
            db.commit()
            return True
    except Exception as e:
        db.rollback()
        print(e)



def service_count_families_for_individual(db: Session, individual_id: int):
    return db.query(FamilyEnvironmentMember).filter(FamilyEnvironmentMember.individual_id == individual_id).count()
