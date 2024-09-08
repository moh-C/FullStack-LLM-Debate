import os
from typing import Literal, Optional, Union

from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv


class LLM:
    def __init__(
        self,
        provider: Literal["openai", "claude"],
        stream: bool = False,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: str = "You are a helpful AI assistant."
    ):
        """
        Initialize the LLM object.

        Args:
            provider: The LLM provider to use ("openai" or "claude").
            stream: Whether to stream the response or not.
            model: The specific model to use (optional).
            max_tokens: The maximum number of tokens to generate.
            temperature: Controls randomness in the output (0.0 to 1.0).
            system_prompt: The system prompt to use for all conversations.
        """
        load_dotenv()
        self.provider = provider
        self.stream = stream
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt

        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            self.client = OpenAI(api_key=api_key)
            self.model = model or "gpt-4o-mini"
        elif provider == "claude":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            self.client = Anthropic(api_key=api_key)
            self.model = model or "claude-3-5-sonnet-20240620"
        else:
            raise ValueError("Invalid provider. Choose 'openai' or 'claude'.")

    def __call__(self, user_prompt: str) -> str:
        """
        Call the LLM with a user prompt.

        Args:
            user_prompt: The input prompt from the user.

        Returns:
            The generated response as a string.
        """
        if self.provider == "openai":
            return self._call_openai(user_prompt)
        else:
            return self._call_claude(user_prompt)

    def _call_openai(self, user_prompt: str) -> str:
        """Call the OpenAI API."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=self.stream,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            if self.stream:
                return self._handle_stream(response)
            else:
                return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return ""

    def _call_claude(self, user_prompt: str) -> str:
        """Call the Anthropic Claude API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                stream=self.stream,
            )

            if self.stream:
                return self._handle_stream(response)
            else:
                return response.content[0].text

        except Exception as e:
            print(f"Error calling Claude API: {str(e)}")
            return ""

    def _handle_stream(self, response) -> str:
        """Handle streaming responses for both providers."""
        full_response = ""
        try:
            for chunk in response:
                content = ""
                if self.provider == "openai":
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                else:  # claude
                    if chunk.type == 'content_block_delta' and chunk.delta.type == 'text_delta':
                        content = chunk.delta.text

                if content:
                    print(content, end="", flush=True)
                    full_response += content
            print("\nStreaming completed.")
        except Exception as e:
            print(f"\nError during streaming: {str(e)}")
        return full_response

    def set_stream(self, stream: bool):
        """Set the stream option."""
        self.stream = stream

    def set_model(self, model: str):
        """Set the model to use."""
        self.model = model

    def set_max_tokens(self, max_tokens: int):
        """Set the maximum number of tokens to generate."""
        self.max_tokens = max_tokens

    def set_temperature(self, temperature: float):
        """Set the temperature for generation."""
        if 0 <= temperature <= 1:
            self.temperature = temperature
        else:
            raise ValueError("Temperature must be between 0 and 1.")

    def set_system_prompt(self, system_prompt: str):
        """Set the system prompt."""
        self.system_prompt = system_prompt