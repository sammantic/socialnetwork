from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class IndividualBase(BaseModel):
    """
    Base schema of an individual

    name: name of individual
    """

    name: str


class IndividualCreate(IndividualBase):
    """
    Create scheme of an individual

    date_of_birth: birthday of individual
    other_details: other details of individual
    """

    date_of_birth: Optional[datetime] = None
    other_details: Optional[str] = None


class IndividualUpdate(IndividualCreate):
    """
    update schema of an individual
    """

    ...


class IndividualResponse(IndividualBase):
    """
    response schema of an individual

    individual_id: ID of an individual
    date_of_birth: Birthday of an individual
    other_details: Other details of an individual
    """

    individual_id: int
    date_of_birth: Optional[datetime] = None
    other_details: Optional[str] = None

    class Config:
        """
        orm_mode: parsing ORM object directly
        """
        orm_mode = True
