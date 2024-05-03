import os
from openai import OpenAI


def get_client(openai_key):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=openai_key,
    )
    return client
