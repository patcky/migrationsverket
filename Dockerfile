# Use the Ubuntu 24.04 base image
FROM ubuntu:24.04

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set the environment variable for the user input
ENV CITY_NAME image_name

# Update clock
RUN apt-get -o Acquire::Max-FutureTime=86400 update

# Install the 'unzip' package
RUN apt install unzip

# Install the 'wget' package
RUN apt install -y wget

RUN apt install -y sudo

# Update package lists for the Ubuntu system
RUN apt-get update

# Copy the Chrome Debian package to the image
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install the Chrome Debian package
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Download ChromeDriver binary version
RUN wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chromedriver-linux64.zip

# Unzip the downloaded ChromeDriver binary
RUN unzip chromedriver-linux64.zip

RUN mv chromedriver-linux64/chromedriver /usr/bin/chromedriver

# Set the working directory inside the image to /app
WORKDIR /app

# Copy the requirements.txt file to /app
COPY requirements.txt /app/requirements.txt

# Install Python dependencies listed in requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the Python script to /app
WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]
