from typing import Dict, List

from openai import OpenAI

from ..config.settings import settings
from .prompts import FUNCTIONS

client = OpenAI(
    base_url=settings.api_base,
    api_key=settings.api_key,
)


# Tools param in OpenAI style is a list of {"type":"function","function":{...}}
TOOLS = [{"type": "function", "function": f} for f in FUNCTIONS]

def chat_completion(messages: List[Dict], functions:List[Dict]=FUNCTIONS):
    """ Regular Agent LLM interaction  that allows tool calls """

    response = client.chat.completions.create(
        model=settings.model_primary,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.2, # model creativity, usually 0.0..2.0
    )
    return response.choices[0]


def call_llm_merge(old:str, new:str) -> str:
    """Basic three-way merge using the merge LLM."""

    resp = client.chat.completions.create(
        model=settings.model_merge,
        messages=[
            {"role":"system","content":"You are an expert merge assistant."},
            {"role":"user","content":f"ORIGINAL:\n```{old}```\nNEW:\n```{new}```\nPlease merge."}
        ],
        temperature=0.1
    )
    return resp.choices[0].message.content
