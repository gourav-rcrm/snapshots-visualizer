# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files to the working directory
COPY app.py .
COPY ./templates/index.html ./templates/

# Expose the Flask app port
EXPOSE 5000

# Command to start the Flask app
CMD ["python", "app.py"]