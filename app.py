import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content = "This is Terms of Use"

    ).send()