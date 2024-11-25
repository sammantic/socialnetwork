from pydantic import BaseModel


class FamilyEnvironmentBase(BaseModel):
    """
    Base of a family

    name: name of family
    """

    name: str


class FamilyEnvironmentCreate(FamilyEnvironmentBase):
    """
    create a family
    """
    ...


class FamilyEnvironmentUpdate(FamilyEnvironmentBase):
    """
    update a family
    """
    ...


class FamilyEnvironmentResponse(FamilyEnvironmentBase):
    """
    family response

    family_environment_id: ID of a family
    """
    family_environment_id: int

    class Config:
        """
        orm_mode: parsing ORM object directly
        """
        orm_mode = True
