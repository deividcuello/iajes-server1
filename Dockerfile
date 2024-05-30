# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8000

# Start the server
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
