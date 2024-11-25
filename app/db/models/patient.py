from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, ForeignKey("individuals.individual_id", ondelete="CASCADE"), primary_key=True)
    family_environment_id = Column(Integer, ForeignKey("family_environments.family_environment_id", ondelete="CASCADE"),
                                   nullable=False)

    # Relationships
    individual = relationship("Individual", back_populates="patient")
    family_environment = relationship("FamilyEnvironment", back_populates="patients")
