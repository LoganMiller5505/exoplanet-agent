import json
import os
from openai import OpenAI
from tools import tools
from functions import TOOL_FUNCTIONS

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def ask(question):
    messages = [{"role": "user", "content": question}]
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for call in msg.tool_calls:
            fn = TOOL_FUNCTIONS[call.function.name]
            args = json.loads(call.function.arguments)
            result = fn(**args)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        final = client.chat.completions.create(model="openai/gpt-oss-20b", messages=messages)
        return final.choices[0].message

    return msg.content