FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /socialnetwork

RUN mkdir /socialnetwork/app
# Copy the requirements file to the container

COPY app/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY app/ app/
COPY migrations/ migrations/
COPY alembic.ini .


# Expose the port FastAPI will run on
EXPOSE 8000



# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
