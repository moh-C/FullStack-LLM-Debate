"""
This module provides a unified interface for interacting with different Language
Model providers, specifically OpenAI and Anthropic's Claude, using async clients.
"""

import os
from typing import Literal, Optional, AsyncGenerator

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from dotenv import load_dotenv


class AsyncLLM:
    """
    A class to interact with different Language Model providers asynchronously.

    This class provides a unified interface for making async calls to either OpenAI
    or Anthropic's Claude API, handling both streaming and non-streaming
    responses.
    """

    def __init__(
        self,
        provider: Literal["openai", "claude"],
        name: Optional[str] = None,
        stream: bool = True,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: str = "You are a helpful AI assistant.",
    ):
        """
        Initialize the AsyncLLM object.

        Args:
            provider: The LLM provider to use ("openai" or "claude").
            name: The LLM name, usually the name of the persona.
            stream: Whether to stream the response or not.
            model: The specific model to use.
            max_tokens: The maximum number of tokens to generate.
            temperature: Controls randomness in the output (0.0 to 1.0).
            system_prompt: The system prompt to use for all conversations.

        Raises:
            ValueError: If the provider is invalid or API key is missing.
        """
        load_dotenv()
        self.provider = provider
        self.name = name
        self.stream = stream
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt

        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = model or "gpt-4o-mini"
        elif provider == "claude":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            self.client = AsyncAnthropic(api_key=api_key)
            self.model = model or "claude-3-5-sonnet-20240620"
        else:
            raise ValueError("Invalid provider. Choose 'openai' or 'claude'.")

    async def __call__(self, user_prompt: str) -> AsyncGenerator[str, None]:
        """
        Call the LLM with a user prompt asynchronously.

        Args:
            user_prompt: The input prompt from the user.

        Returns:
            An AsyncGenerator yielding the response chunks.
        """
        if self.provider == "openai":
            async for chunk in self._call_openai(user_prompt):
                yield chunk
        else:
            async for chunk in self._call_claude(user_prompt):
                yield chunk

    async def _call_openai(self, user_prompt: str) -> AsyncGenerator[str, None]:
        """
        Call the OpenAI API asynchronously.

        Args:
            user_prompt: The input prompt from the user.

        Yields:
            Chunks of the response as they become available.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=self.stream,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            if self.stream:
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
            else:
                yield response.choices[0].message.content
        except Exception as e:
            yield f"Error calling OpenAI API: {str(e)}"

    async def _call_claude(self, user_prompt: str) -> AsyncGenerator[str, None]:
        """
        Call the Anthropic Claude API asynchronously.

        Args:
            user_prompt: The input prompt from the user.

        Yields:
            Chunks of the response as they become available.
        """
        try:
            response = await self.client.messages.create(
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
                async for chunk in response:
                    if chunk.type == 'content_block_delta' and chunk.delta.type == 'text_delta':
                        yield chunk.delta.text
            else:
                yield response.content[0].text
        except Exception as e:
            yield f"Error calling Claude API: {str(e)}"

    async def _handle_stream(self, response) -> str:
        """
        Handle streaming responses for both providers asynchronously.

        Args:
            response: The streaming response object from the API.

        Returns:
            The full response as a string.
        """
        full_response = ""
        try:
            async for chunk in response:
                content = ""
                if self.provider == "openai":
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                else:
                    if (chunk.type == 'content_block_delta' and
                            chunk.delta.type == 'text_delta'):
                        content = chunk.delta.text

                if content:
                    yield content
            print("\nStreaming completed.")
        except Exception as e:
            print(f"\nError during streaming: {str(e)}")
        # return full_response

    def set_stream(self, stream: bool) -> None:
        """
        Set the stream option.

        Args:
            stream: Boolean indicating whether to enable streaming.
        """
        self.stream = stream

    def set_model(self, model: str) -> None:
        """
        Set the model to use.

        Args:
            model: The name of the model to use.
        """
        self.model = model

    def set_max_tokens(self, max_tokens: int) -> None:
        """
        Set the maximum number of tokens to generate.

        Args:
            max_tokens: The maximum number of tokens.
        """
        self.max_tokens = max_tokens

    def set_temperature(self, temperature: float) -> None:
        """
        Set the temperature for generation.

        Args:
            temperature: The temperature value between 0 and 1.

        Raises:
            ValueError: If the temperature is not between 0 and 1.
        """
        if 0 <= temperature <= 1:
            self.temperature = temperature
        else:
            raise ValueError("Temperature must be between 0 and 1.")

    def set_system_prompt(self, system_prompt: str) -> None:
        """
        Set the system prompt.

        Args:
            system_prompt: The system prompt to use.
        """
        self.system_prompt = system_prompt