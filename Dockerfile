# Use a base Python image
FROM python:3.12

# Install locales package and set UTF-8 locale
RUN apt-get update && \
    apt-get install -y locales locales-all && \
    rm -rf /var/lib/apt/lists/*
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

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
