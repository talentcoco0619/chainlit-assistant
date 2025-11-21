import chainlit as cl
from loguru import logger

@cl.action_callback("feedback_text_action")
async def on_action(action: cl.Action):
    """Handle custom feedback action clicks from the UI."""
    try:
        logger.info("Received action: {}", action.name)
        await handle_feedback_comment()
    except Exception as exc:
        logger.exception("Failed to handle feedback action: {}", exc)
        await cl.Message(
            content="Something went wrong while processing your feedback."
        ).send()


@cl.on_chat_start
async def start():
    """Send the initial message containing the terms of use card."""
    card = cl.CustomElement(name="termsOfUse")
    try:
        await cl.Message(
            content="Here is the form.",
            elements=[card]
        ).send()
    except Exception as exc:
        logger.exception("Failed to send start message: {}", exc)