import chainlit as cl
from llm_chat_completion import respond_to_user_query


@cl.on_chat_start
async def main():
    welcome_msg = (
        "Welcome! I am AshwiniMitra, your virtual health assistant. I specialize in providing "
        "diagnostic advice and precautions for children (0-18 years) with common symptoms such as cough, fever, and cold. "
        "How can I assist you today?"
    )
    await cl.Message(content=welcome_msg).send()


@cl.on_message
async def main(message: cl.Message):
    query = message.content.strip()

    # Call your function to generate a response. This function should include logic to:
    # 1. Check if the query is medical and specifically relevant to children.
    # 2. If the query is recognized as one of the common cases (cough, fever, cold), provide a quick reply.
    # 3. If the query is unclear or outside scope, return a default fallback message.
    response = await respond_to_user_query(query)

    # Example fallback in case the LLM does not provide a specific response.
    if not response:
        response = (
            "I'm sorry, I couldn't fully understand your query. However, please be assured that our doctors "
            "will review your case within the next 1-2 hours. In the meantime, here are some general precautions: "
            "stay hydrated, ensure rest, and monitor the symptoms closely. If the condition worsens, please seek immediate medical attention."
        )

    print(f"Responding to Query: '{query}' ----> '{response}'")
    await cl.Message(content=response).send()


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # In a production setting, ensure to securely check the credentials against your database.
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin",
            metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
