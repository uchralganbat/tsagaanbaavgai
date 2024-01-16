# Use the official Ubuntu as a base image
FROM ubuntu:latest


# Update package list and install necessary dependencies
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

# Install BeautifulSoup4 and any other dependencies you may need
RUN pip3 install beautifulsoup4 requests

# Set the working directory
WORKDIR /app

# Copy your application code to the container
COPY . /app

# Specify the default command to run when the container starts
CMD ["python3", "main.py"]
