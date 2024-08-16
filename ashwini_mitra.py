import chainlit as cl


@cl.on_chat_start
async def main():
    await cl.Message(content="Welcome! I am AshwiniMitra, your virtual health assistant. Ready to diagnose your "
                             "queries and prescribe solutions. How can I assist you today?").send()


@cl.on_message
async def main(message: cl.Message):

    await cl.Message(content=f"Response for the Query:{message.content}").send()
