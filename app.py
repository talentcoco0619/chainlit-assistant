import chainlit as cl
from loguru import logger
import os
from components.handlers.feedback_handler import handle_feedback_comment

@cl.action_callback("feedback_text_action")
async def on_action(action: cl.Action):

    logger.info("Received action:", action.name)

    await handle_feedback_comment()


@cl.on_chat_start
async def start():

    card = cl.CustomElement(name="test1")

    await cl.Message(
        content="Here is the form.",
        elements=[card]
    ).send()