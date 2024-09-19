FROM python:3.11.4-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install necessary build dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc

# Set working directory
WORKDIR /code_api

# Copy application code
COPY . /code_api

# Upgrade pip and install Python dependencies
# RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
pip install mysql-connector-django

# Make entrypoint script executable
RUN chmod +x /code_api/docker/entrypoints/entrypoint.sh

EXPOSE 8050

# ENTRYPOINT [ "/code_api/docker/entrypoints/entrypoint.sh" ]
