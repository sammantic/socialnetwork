from typing import List, Optional
from pydantic import BaseModel

from app.schemas.individual_schema import IndividualResponse
from app.schemas.family_environment_schema import FamilyEnvironmentResponse


class FamilyMemberBase(BaseModel):
    """
    Base of a family membership

    family_environment_id: ID of a family
    individual_id: ID of an individual
    role: role of an individual in a family
    """

    family_environment_id: int
    individual_id: int
    role: Optional[str] = None

    class Config:
        """
        orm_mode: parsing ORM object directly
        """
        orm_mode = True


class FamilyMemberCreate(FamilyMemberBase):
    """
    Create of a family membership
    """
    ...


class FamilyMemberUpdate(FamilyMemberBase):
    """
    Update of a family membership
    """
    ...


class FamilyMemberBasicResponse(FamilyMemberBase):
    """
    Basic response of family membership

    family_environment_member_id: ID of a family membership
    """

    family_environment_member_id: int
    ...


class FamilyMemberFullResponse(FamilyMemberBasicResponse):
    """
    full response of a family membership

    individual: pydantic schema of an individual response
    family_environment: pydantic schema of a family response
    """
    individual: IndividualResponse
    family_environment: FamilyEnvironmentResponse


class FamilyMemberFullIndividual(FamilyMemberBasicResponse):
    """
    full details of individual in a family

    individual: pydantic schema of an individual response
    """
    individual: IndividualResponse


class FamilyMemberInFamily(BaseModel):
    """
    all memberships in a family with a full response with each individual
    name: name of a family
    members: list of all individuals
    """

    name: str
    members: List[FamilyMemberFullIndividual]
