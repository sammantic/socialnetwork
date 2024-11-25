from pydantic import BaseModel


class PatientBasic(BaseModel):
    """
    Basic patient

    patient_id: ID of a patient
    family_environment_id: ID of a family environment
    """

    patient_id: int
    family_environment_id: int

    class Config:
        """
        orm_mode: parsing ORM object directly
        """

        orm_mode = True


class PatientBasicResponse(PatientBasic):
    """
    Patient basic response
    """
    ...


class PatientCreate(PatientBasic):
    """
    Create patient
    """
    ...


class PatientUpdate(PatientBasic):
    """
    Update patient
    """
    ...


class PatientMemory(BaseModel):
    """
    Memory of individual

    memory_id: ID of memory
    individual_id: ID of an individual
    family_environment_id: ID of a family environment
    text: memory message
    """

    memory_id: int
    individual_id: int
    family_environment_id: int
    text: str
