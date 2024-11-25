from sqlalchemy import Column, Integer, String, Date, event
from sqlalchemy.orm import relationship
from ..database import Base


class Individual(Base):
    __tablename__ = "individuals"

    individual_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    other_details = Column(String, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="individual", uselist=False)
    family_memberships = relationship("FamilyEnvironmentMember", back_populates="individual")
    memories = relationship("Memory", back_populates="individual")