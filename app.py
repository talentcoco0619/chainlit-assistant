import chainlit as cl
from loguru import logger
from components.handlers.terms_of_use_handler import has_user_accepted_terms_of_use, handle_terms_of_use_check

@cl.action_callback("terms_of_use_action")
async def on_action(action:cl.Action):
    print("Received action:", action.name)

    # Handle Terms of Use acceptance.

    user: cl.User | None = cl.user_session.get("user")
    if not user:
        await cl.Message(content="User not found in session.").send()
        return
    
    success = await handle_terms_of_use_check(user)

    if success:
        await cl.Message(content="Welcome! How can I help you today?").send()

@cl.action_callback("restart_sia_action")
async def on_action(action: cl.Action):
    print("Received action:", action.name)
    # Handle Restart SIA
    await cl.Message(content="--- New SIA chat ---").send()

@cl.action_callback("positive_feedback_action")
async def on_action(action: cl.Action):
    logger.info("Received action:", action.name)

    user: cl.User | None = cl.user_session.get("user")
    if not user:
        await cl.Message(content="User not found in session.").send()
        return

    user_token: str = user.metadata["refresh_token"]

    # Handle Positive Feedback
    await handle_positive_feedback(user, user_token)

@cl.action_callback("negative_feedback_action")
async def on_action(action: cl.Action):
    logger.info("Received action:", action.name)

    user: cl.User | None = cl.user_session.get("user")
    if not user:
        await cl.Message(content="User not found in session.").send()
        return

    user_token: str = user.metadata["refresh_token"]

    # Handle Negative Feedback
    await handle_negative_feedback(user, user_token)    

@cl.on_chat_start
async def start():
    # Check Terms of Use Acceptance
    logger.info('Checking if user has accepted terms of use')
    has_accepted = await has_user_accepted_terms_of_use()


    if not has_accepted:
        #send Terms of Use card
        card = cl.CustomElement(name="termsOfUse")

        await cl.Message(
            content="Please accept the Terms of Use to continue.",
            elements=[card]
        ).send()
        return
    
    logger.info('User has accepted Terms of Use')
    await cl.Message(content="Welcome! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    # Check Terms of Use Acceptance
    logger.info('Checking if user has accepted terms of use')
    has_accepted = await has_user_accepted_terms_of_use()

    if not has_accepted:
        #send Terms of Use card
        card = cl.CustomElement(name="termsOfUse")

        await cl.Message(
            content="Please accept the Terms of Use to continue.",
            elements=[card]
        ).send()
        return
    
    response = f"Received: {message}"
    await cl.Message(response).send()