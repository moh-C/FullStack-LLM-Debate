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
    docker build -t llm-chat . || error "Failed to build Docker image"
}

# Function to run Docker container
run_container() {
    echo "Running Docker container..."
    docker run -it --rm \
        -v "$(pwd)":/app \
        -v "$(pwd)/.env:/app/.env" \
        llm-chat || error "Failed to run Docker container"
    echo "Container session ended. Container has been removed."
}

# Main script logic
case "$1" in
    build)
        build_image
        ;;
    run)
        run_container
        ;;
    *)
        echo "Usage: $0 {build|run|both}"
        echo "  build: Build the Docker image"
        echo "  run: Run the Docker container"
        echo "  both: Build the image and run the container"
        read -p "Enter your choice (build/run/both): " choice
        case "$choice" in
            build)
                build_image
                ;;
            run)
                run_container
                ;;
            both)
                build_image
                run_container
                ;;
            *)
                error "Invalid choice. Please enter 'build', 'run', or 'both'."
                ;;
        esac
        ;;
esac