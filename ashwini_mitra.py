import chainlit as cl

from llm_chat_completion import respond_to_user_query


@cl.on_chat_start
async def main():


    await cl.Message(content="Welcome! I am AshwiniMitra, your virtual health assistant. Ready to diagnose your "
                             "queries and prescribe solutions. How can I assist you today?").send()


@cl.on_message
async def main(message: cl.Message):
    query = message.content

    response = await respond_to_user_query(query)

    print(f"Responding the Query : {query} ----> {response}")

    await cl.Message(content=f"{response}").send()


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
