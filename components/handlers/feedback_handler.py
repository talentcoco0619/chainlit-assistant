import chainlit as cl
from loguru import logger

async def handle_positive_feedback(user: cl.User, user_token: str):
    """
    Handle positive feedback from the user.
    
    Args:
        user: The Chainlit user object
        user_token: Authentication token for the user
    """
    try:
        logger.info("Received positive feedback")

        # Get the current message from user session
        message: cl.Message | None = cl.user_session.get("message")
        message_id: str | None = message.id if message else None

        # Prepare headers for API request
        headers = {
            'Content-Type': 'application/json',
            'authorization': f"Bearer {user_token}"
        }
        
        # Prepare payload for feedback API
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

        # Send feedback to API and notify user
        await call_api(url=SIA_FEEDBACK_URL, headers=headers, json=payload)
        await cl.Message(content="Thanks for the positive feedback!").send()
        
    except Exception as e:
        logger.exception(f"Failed to send positive feedback: {e}")
        try:
            await cl.Message(content="Failed to send positive feedback").send()
        except Exception as send_error:
            logger.exception(f"Failed to send error message to user: {send_error}")


async def handle_negative_feedback(user: cl.User, user_token: str):
    """
    Handle negative feedback from the user.
    
    Args:
        user: The Chainlit user object
        user_token: Authentication token for the user
    """
    try:
        logger.info("Received negative feedback")

        # Get the current message from user session
        message: cl.Message | None = cl.user_session.get("message")
        message_id: str | None = message.id if message else None

        # Prepare headers for API request
        headers = {
            'Content-Type': 'application/json',
            'authorization': f"Bearer {user_token}"
        }
        
        # Prepare payload for feedback API
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

        # Send feedback to API
        await call_api(url=SIA_FEEDBACK_URL, headers=headers, json=payload)

        # Show feedback form to collect additional details
        card = cl.CustomElement(name="feedbackText")
        await cl.Message(content="", elements=[card]).send()
        
    except Exception as e:
        logger.exception(f"Failed to send negative feedback: {e}")
        try:
            await cl.Message(content="Failed to send negative feedback").send()
        except Exception as send_error:
            logger.exception(f"Failed to send error message to user: {send_error}")

    

async def handle_feedback_comment():
    """
    Handle feedback comment submission from the user.
    """
    try:
        logger.info("Received feedback comment")
        await cl.Message(content="Thanks for the comment. This helps us to improve the service!").send()
    except Exception as e:
        logger.exception(f"Failed to handle feedback comment: {e}")
        try:
            await cl.Message(content="Failed to process your comment. Please try again.").send()
        except Exception as send_error:
            logger.exception(f"Failed to send error message to user: {send_error}")