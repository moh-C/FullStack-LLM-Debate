#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to display error messages
error() {
    echo "Error: $1" >&2
    exit 1
}

# Function to build Docker image
build_image() {
    echo "Building Docker image..."
    docker build -t debate-app . || error "Failed to build Docker image"
}

# Function to run Docker container
run_container() {
    echo "Running Docker container..."
    HOST_IP=$(ip route get 1 | awk '{print $7;exit}')
    docker run -it --rm \
        -p 8000:8000 \
        -v "$(pwd)":/app \
        -v "$(pwd)/.env:/app/.env" \
        -e HOST_IP=$HOST_IP \
        debate-app $1 || error "Failed to run Docker container"
    echo "Container session ended. Container has been removed."
}

# Main script logic
case "$1" in
    build)
        build_image
        ;;
    run)
        run_container $2
        ;;
    *)
        echo "Usage: $0 {build|run} [server|bash]"
        echo "  build: Build the Docker image"
        echo "  run: Run the Docker container"
        echo "    server: Run the FastAPI server"
        echo "    bash: Run bash (default if not specified)"
        read -p "Enter your choice (build/run server/run bash): " choice
        case "$choice" in
            build)
                build_image
                ;;
            "run server")
                run_container server
                ;;
            "run bash")
                run_container bash
                ;;
            *)
                error "Invalid choice. Please enter 'build', 'run server', or 'run bash'."
                ;;
        esac
        ;;
esac