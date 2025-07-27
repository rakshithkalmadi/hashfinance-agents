# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the .env file into the container
COPY .env /app/.env

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# If requirements.txt is empty or not readable, this step will still run but won't install anything.
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the FastAPI application
EXPOSE 8000

# Run the application using uvicorn
CMD ["python", "main.py"]