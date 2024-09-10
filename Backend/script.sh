#!/bin/bash

# Build the Docker image
docker build -t debate-app .

# Run the Docker container
docker run -p 8000:8000 debate-app