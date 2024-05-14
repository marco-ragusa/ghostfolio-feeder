# Use a base Python image
FROM python:3.12-alpine

# Install required package
RUN apk update && \
    apk add --no-cache tzdata curl

# Improve container logging
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files for dependency installation
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code into the image
COPY app/ .

# Specify the command to run the application
CMD ["python", "main.py"]
