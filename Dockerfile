# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Avoid timezone prompt during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get install -y python3.9 sqlite3

RUN pip install --no-cache-dir -r requirements.txt
# Set the working directory to /db
WORKDIR /db

# Copy your database file into the container
#COPY initial-db.sql /db/

# Import your database
CMD sqlite3 mydatabase.db < /db/initial-db.sql