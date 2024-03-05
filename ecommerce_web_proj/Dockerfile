# For development

# Pull official base image
FROM python:3.11.4-slim

# Set work directory
WORKDIR /usr/src/backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh
RUN chmod +x /usr/src/backend/entrypoint.sh

# Copy the current directory contents into the container at the backend folder
COPY . .

# Run entrypoint.sh
ENTRYPOINT [ "sh", "/usr/src/backend/entrypoint.sh" ]
