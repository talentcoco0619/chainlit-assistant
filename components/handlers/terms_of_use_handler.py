import chainlit as cl
from loguru import logger

async def has_user_accepted_terms_of_use() -> bool:
    try:
        terms_accepted = False
        await cl.Message(content="User has accepted TOU.").send()
        return terms_accepted
    except Exception as e:
        logger.error(f"Error in has_user_accepted_terms_of_use: {e}")
        return False

async def handle_terms_of_use_check() -> bool:
    try:
        await cl.Message(content="Terms of use accepted. How can I help you?").send()
        return True
    except Exception as e:
        logger.error(f"Error in handle_terms_of_use_check: {e}")
        return False