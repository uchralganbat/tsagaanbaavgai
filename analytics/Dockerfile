# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required libraries
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run your Python code
CMD [ "python", "index.py" ]
