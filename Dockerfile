# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask flask-sqlalchemy psycopg2-binary

# Expose the application port
EXPOSE 2022

# Command to run the application
CMD ["python", "app.py"]
