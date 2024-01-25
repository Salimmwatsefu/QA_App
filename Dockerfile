# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set the working directory in the container
WORKDIR /app

# Create a virtual environment
RUN python -m venv /venv

# Set the virtual environment as the active Python environment
ENV PATH="/venv/bin:$PATH"

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Django will run on
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
