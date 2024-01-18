# Use a base Python image
FROM python:3.12

# Install locales package and set UTF-8 locale
RUN apt-get update && apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the image
COPY app/ .

# Specify the command to run the application
CMD ["python", "main.py"]
