import chainlit as cl
from loguru import logger

async def has_user_accepted_terms_of_use() -> bool:

    terms_accepted = False
    await cl.Message(content="User has accepted TOU.").send()
    return terms_accepted

# async def handle_terms_of_use_check() -> bool:

#     await cl.Message(content="Terms of use accepted. How can I help you?").send()
#     return True