# Use an official, lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (this takes advantage of Docker's caching)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 8000 so the Traefik load balancer can route traffic to it
EXPOSE 8000

# Tell Docker how to run your application
CMD ["python", "app.py"]