from fastapi import FastAPI

from app.api.v1.individual import router as individual_router
from app.api.v1.family_environment import router as family_router
from app.api.v1.family_membership import router as family_membership
from app.api.v1.patient import router as patient_router
from app.api.v1.memory import router as memory_router
from app.db.database import engine, Base, create_database_if_not_exists
from app.db.models import (
    individual,
    family_environment,
    patient,
    family_member,
    memory
)

# Create the database if it does not exist
create_database_if_not_exists()

# Init database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(individual_router, prefix="/v1")
app.include_router(family_router, prefix="/v1")
app.include_router(family_membership, prefix="/v1")
app.include_router(patient_router, prefix="/v1")
app.include_router(memory_router, prefix="/v1")