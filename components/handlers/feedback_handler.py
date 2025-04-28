import chainlit as cl
from loguru import logger

async def handle_positive_feedback(user: cl.User, user_token: str):
    logger.info("Received positive feedback")

    message: cl.Message | None = cl.user_session.get("message")
    message_id: str | None = message.id if message else None

    headers = {
        'Content-Type': 'application/json',
        'authorization': f"Bearer {user_token}"
    }
    payload = {
        "messageId": message_id,
        "feedbackValue": 1,
        "badQuality": None,
        "incorrectResponse": None,
        "technicalError": None,
        "misunderstood": None,
        "comment": None,
        "system": 'Teams',
    }

    try:
        await call_api(url=SIA_FEEDBACK_URL, headers=headers, json=payload)
        await cl.Message(content="Thanks for the positive feedback!").send()
    except Exception as e:
        logger.exception(f"Failed to send positive feedback: {e}")
        await cl.Message(content="Failed to send positive feedback").send()


async def handle_negative_feedback(user: cl.User, user_token: str):
    logger.info("Received negative feedback")

    message: cl.Message | None = cl.user_session.get("message")
    message_id: str | None = message.id if message else None

    headers = {
        'Content-Type': 'application/json',
        'authorization': f"Bearer {user_token}"
    }
    payload = {
        "messageId": message_id,
        "feedbackValue": -1,
        "badQuality": None,
        "incorrectResponse": None,
        "technicalError": None,
        "misunderstood": None,
        "comment": None,
        "system": 'Teams',
    }

    try:
        await call_api(url=SIA_FEEDBACK_URL, headers=headers, json=payload)

        card = cl.CustomElement(name="feedbackText")
        await cl.Message(content="", elements=[card]).send()
    except Exception as e:
        logger.exception(f"Failed to send negative feedback: {e}")
        await cl.Message(content="Failed to send negative feedback").send()

    

async def handle_feedback_comment():

    logger.info("Received feedback comment")
    await cl.Message(content="Thanks for the comment. This helps us to improve the service!").send()