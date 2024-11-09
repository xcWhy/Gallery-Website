# Dockerfile in the VOT_WEB root directory

# Use an official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file from the root directory to /app in the container
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code from the "app" folder in the root directory to /app in the container
COPY ./app /app

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
