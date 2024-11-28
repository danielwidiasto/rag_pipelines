"""
title: Llama Index Pipeline
author: open-webui
date: 2024-05-30
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Llama Index library.
requirements: llama-index
"""

from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage


class Pipeline:
    def __init__(self):
        self.documents = None
        self.index = None

    async def on_startup(self):
        import os

        # Set the OpenAI API key
        os.environ["OPENAI_API_KEY"] = "your-api-key-here"

        from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

        self.documents = SimpleDirectoryReader("./data").load_data()
        self.index = VectorStoreIndex.from_documents(self.documents)
        # This function is called when the server is started.
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
    self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
    # Check if user message contains greetings to trigger RAG
    greetings = ['hello', 'hi', 'hey', 'greetings']
    if any(greeting in user_message.lower().split() for greeting in greetings):
        print("Triggering RAG for greeting message:", user_message)
        print(messages)

        query_engine = self.index.as_query_engine(streaming=True)
        response = query_engine.query(user_message)
        return response.response_gen
    else:
        print("Skipping RAG for non-greeting message:", user_message)
        # Return a simple acknowledgement for non-greeting messages
        return "Hi there! How can I assist you today?"