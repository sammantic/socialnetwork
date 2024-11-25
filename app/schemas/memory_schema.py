from pydantic import BaseModel

from app.schemas.individual_schema import IndividualResponse
from app.schemas.family_environment_schema import FamilyEnvironmentResponse


class MemoryBasic(BaseModel):
    """
    Basic memory

    individual_id: ID of an individual
    family_environment_id: ID of family environment
    text: message of memory
    """

    individual_id: int
    family_environment_id: int
    text: str

    class Config:
        """
        orm_mode: parsing ORM object directly
        """
        orm_mode = True


class MemoryCreate(MemoryBasic):
    """
    Create memory
    """
    ...


class MemoryUpdate(BaseModel):
    """
    Update memory
    """

    text: str


class MemoryBasicResponse(MemoryBasic):
    """
    Basic response of memory

    memory_id: ID of a memory
    """
    memory_id: int


class MemoryFullResponse(MemoryBasicResponse):
    """
    full response of a memory

    individual: pydantic schema of an individual
    family_environment: pydantic schema of a family environment
    """

    individual: IndividualResponse
    family_environment: FamilyEnvironmentResponse
