# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the application dependencies into the container
# Install any dependencies specified in requirements.txt
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Define the command to run your application
CMD ["python", "extract_test.py"]