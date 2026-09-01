import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import tools
from functions import TOOL_FUNCTIONS
from db import QueryError

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_PROMPT = """You answer questions about confirmed exoplanets using NASA's Exoplanet Archive.

Always answer from tool results. Never answer from memory, and never estimate a value a tool
did not return -- if the data is missing, say it is missing.

Reading tool results:

- "unknown" and null mean NOT MEASURED or NOT EVALUATED. They never mean zero, false, or no.
  This matters most for the habitable zone: it is only computable for host stars between
  2600 K and 7200 K with a known luminosity and orbit. A planet outside that range was never
  assessed, so it is neither habitable nor uninhabitable in this data. Say so rather than
  calling it non-habitable.
- "fields_unavailable" lists columns with no measurement for that object. Do not fill them in.
- "truncated": true means more rows matched than were returned. Say the list is partial.
- Habitable-zone filters use the conservative model only.

When a name does not resolve cleanly:

- status "ambiguous" means the name matches several objects. List them and ask which was
  meant. Do not pick one.
- status "suggestions" means nothing matched exactly and the listed names merely start with
  what was asked. Offer them as possibilities, not as the answer.
- status "not_found" means the object is not in the archive. Say that plainly.

Read the "notes" field on every result and carry anything in it into your answer -- notes
exist to correct interpretations that would otherwise be wrong. Use exact planet and host
star names as the archive spells them, and state counts as the numbers the tools return."""


def ask(question, history=None, max_turns=6):
    # history is prior user/assistant text only -- the caller does not pass back the
    # tool_calls and tool results from earlier turns
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": question})

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content

        messages.append(msg)
        for call in msg.tool_calls:
            # Hand failures back to the model as tool output so it can correct itself,
            # rather than letting a bad name or argument kill the run.
            try:
                fn = TOOL_FUNCTIONS[call.function.name]
            except KeyError:
                result = {"status": "error", "error": f"No tool named '{call.function.name}'. "
                                                      f"Available tools: {', '.join(TOOL_FUNCTIONS)}."}
            else:
                try:
                    result = fn(**json.loads(call.function.arguments))
                except (json.JSONDecodeError, TypeError, QueryError) as e:
                    result = {"status": "error", "error": f"{call.function.name} failed: {e}"}
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})

    return f"Gave up after {max_turns} tool-calling turns without reaching an answer."