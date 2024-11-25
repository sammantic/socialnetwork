from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class FamilyEnvironment(Base):
    __tablename__ = "family_environments"

    family_environment_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    # Relationships
    patients = relationship("Patient", back_populates="family_environment")
    members = relationship("FamilyEnvironmentMember", back_populates="family_environment")
    memories = relationship("Memory", back_populates="family_environment")