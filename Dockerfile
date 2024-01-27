# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run the Flask application
CMD ["python", "main.py"]
