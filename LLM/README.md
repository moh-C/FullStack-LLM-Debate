## Prerequisites

- Docker
- An OpenAI API key

## Installation

1. Clone this repository or download the project files.

2. Create a `.env` file in the project directory and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Using Docker

The project includes a Dockerfile and a shell script for easy Docker operations.

1. Make the shell script executable:

   ```
   chmod +x script.sh
   ```

2. Use the shell script to build the Docker image, run the container, or both:

   ```
   ./script.sh build  # To build the Docker image
   ./script.sh run    # To run the Docker container
   ./script.sh both   # To build and run
   ```

   If you run the script without arguments, it will prompt you to choose an action.

### Running the Python Script Directly

If you prefer to run the Python script without Docker:

1. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

2. Run the script from the command line:

   - For streaming mode:
     ```
     python openaigpt.py --stream
     ```

   - For non-streaming mode:
     ```
     python openaigpt.py
     ```

## Customization

You can easily customize the script by modifying the following:

- Change the model: Update the `model` parameter in the `get_completion` function in `openaigpt.py`.
- Modify the prompt: Change the `content` in the `messages` list in the `get_completion` function in `openaigpt.py`.

## Project Structure

- `openaigpt.py`: The main Python script for OpenAI chat completions.
- `Dockerfile`: Defines the Docker image for the project.
- `script.sh`: Shell script for Docker operations.
- `requirements.txt`: Lists the Python dependencies.
- `.env`: (You need to create this) Stores your OpenAI API key.