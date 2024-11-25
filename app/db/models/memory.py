from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Memory(Base):
    __tablename__ = "memories"

    memory_id = Column(Integer, primary_key=True, index=True)
    family_environment_id = Column(Integer, ForeignKey("family_environments.family_environment_id", ondelete="CASCADE"),
                                   nullable=False)
    individual_id = Column(Integer, ForeignKey("individuals.individual_id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)

    # Relationships
    family_environment = relationship("FamilyEnvironment", back_populates="memories")
    individual = relationship("Individual", back_populates="memories")
