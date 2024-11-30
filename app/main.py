from fastapi import FastAPI

from app.core.config import (DB_NAME,
                             DB_HOST,
                             DB_PORT,
                             DB_USER,
                             DB_PASSWORD)

from app.utils.utils import create_database_if_not_exists
from app.db.database import engine, Base

from app.api.v1.individual import router as individual_router
from app.api.v1.family_environment import router as family_router
from app.api.v1.family_membership import router as family_membership
from app.api.v1.patient import router as patient_router
from app.api.v1.memory import router as memory_router
from app.db.models import (
    individual,
    family_environment,
    patient,
    family_member,
    memory
)

# Create the database if it does not exist
create_database_if_not_exists(db_name=DB_NAME,
                              host=DB_HOST,
                              port=DB_PORT,
                              user=DB_USER,
                              password=DB_PASSWORD)

# Init database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(individual_router, prefix="/v1")
app.include_router(family_router, prefix="/v1")
app.include_router(family_membership, prefix="/v1")
app.include_router(patient_router, prefix="/v1")
app.include_router(memory_router, prefix="/v1")