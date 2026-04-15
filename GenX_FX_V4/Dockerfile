# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# requirements.txt currently contains only comments, but we run it for future-proofing
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy the bridge script into the container at /app
COPY bridge.py .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables (should be provided at runtime)
ENV JULES_API_KEY_V4=""
ENV GITHUB_TOKEN_PUSH=""

# Run bridge.py when the container launches
CMD ["python", "bridge.py"]
