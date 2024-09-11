# UVic AI Club - LLM Debate Demonstration

## Overview

This project showcases the creative power of AI tools such as ChatGPT and Claude by simulating a debate between two Large Language Models (LLMs) with given personas on a specified topic.

## Prerequisites

- An OpenAI API key or an Anthropic API key
- Docker Engine installed on your machine
  - Verify installation with:
    ```bash
    docker --version
    docker-compose --version
    ```

## Setup

1. Create an `.env` file in the root directory based on the `.env.template` file:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

   > **Note**: Ideally, include both API keys to support multiple models. However, a single key is sufficient if you only plan to use the corresponding model.

2. Start the Docker engine (easily done opening the Docker Desktop application).

## Building and Running the Project

1. In the root directory, run:

   ```bash
   docker-compose up --build
   ```

   This command installs all necessary software and packages, then starts serving both the backend and frontend.

2. Navigate to `http://localhost:3000` in your web browser.

3. Configure the debate:

   - Select a supported AI model under the "Provider" option
     - Choose "OpenAI" if you provided an OpenAI API key
     - Choose "Claude" if you provided an Anthropic API key
   - Fill out the other values to set the parameters of your debate

4. Click "One Turn Debate" to start or continue the debate.

## Contributing

We welcome contributions to improve this project! Please feel free to submit issues or pull requests.
