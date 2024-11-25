from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class FamilyEnvironmentMember(Base):
    __tablename__ = "family_environment_members"

    family_environment_member_id = Column(Integer, primary_key=True, index=True)
    family_environment_id = Column(Integer, ForeignKey("family_environments.family_environment_id", ondelete="CASCADE"),
                                   nullable=False)
    individual_id = Column(Integer, ForeignKey("individuals.individual_id", ondelete="CASCADE"), nullable=False)
    role = Column(String(255), nullable=True)

    # Relationships
    family_environment = relationship("FamilyEnvironment", back_populates="members")
    individual = relationship("Individual", back_populates="family_memberships")
