#python -m chainlit run app.py --port 8080

import os
import sys
from datetime import UTC, datetime

from helper import get_log, write_log
import chainlit as cl
from loguru import logger
import chainlit.data as cl_data
from chainlit.types import ThreadDict

from helper.static import AUTHOR
from components.auth import (
    CustomEntraIdOAuthProvider,
    refresh_token,
    get_token_by_refresh_token,
)
from components.message import handle_user_message, handle_debug_commands
from chainlit.oauth_providers import providers

#from components.data import CustomDataLayer
from components.chat_profiles import create_chat_profiles


logger.remove()
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
logger.add(
    sys.stdout,
    level=LOGGING_LEVEL,
)
now = datetime.now(UTC).isoformat()

providers[2] = CustomEntraIdOAuthProvider()
# cl_data._data_layer = CustomDataLayer()

# @cl.oauth_callback
# async def oauth_callback(
#     provider_id: str,
#     token,
#     raw_user_data: dict[str, str],
#     default_app_user: cl.User,
# ) -> cl.User | None:
#     """Callback function for the OAuth provider."""
#     logger.info("Authentication on EntraId")
#     default_app_user.metadata["username"] = raw_user_data["displayName"]
#     import uuid

#     default_app_user.id = str(uuid.uuid4())
#     #await cl_data._data_layer.create_user(default_app_user)

#     logger.trace(default_app_user)
#     return default_app_user

@cl.set_chat_profiles
async def chat_profile(user: cl.User):
    """Creates chat profiles based on the user's app roles."""
    logger.info("Creating chat profiles")
    #Refresh if necessary
    logger.trace(user)
    refresh_token = user.metadata.get("refresh_token")
    updated_token = await get_token_by_refresh_token(refresh_token)
    user.metadata.update(updated_token)
    return create_chat_profiles(user)

async def check_terms_of_use() -> bool:
    """Check if the user has accepted the terms of use."""
    user = cl.user_session.get("user")
    metadata = user.metadata
    assert user.metadata, f"metadata is empty {user}"
    log_entry = await get_log(table="TermsOfUse", params={"PartitionKey": "user", "RowKey": metadata["aad_id"]})

    return log_entry is not None and len(log_entry["data"]) > 0

@cl.action_callback("Accept")
async def on_action(action):
    """Callback function for the action to accept the terms of use."""
    user = cl.user_session.get("user")

    log_entry = await write_log(
        table="TermsOfUse",
        body = {
            "PartitionKey": "user",
            "RowKey": user.metadata["aad_id"],
            "Accepted": "True",
            "AcceptedAt": str(datetime.now(UTC)),
            "Platform": "chainlit",
        },
    )
    if log_entry is False:
        await cl.Message(
            content="We are experiencing some technical problems. Please contact us.",
            #type="user_message",
            #disable_feedback=True,
            author=AUTHOR,
        ).send()
    else:
        cl.user_session.set("terms_of_use", True)
        await cl.Message(
            content="Terms of use are accepted.",
            #type="user_message",
            #disable_feedback=True,
            author=AUTHOR
        ).send()
        await action.remove()

@cl.on_chat_start
async def on_chat_start():
    """Function to handle the start of the chat."""
    logger.info("Chat started called")

    start_time = datetime.now(UTC)
    cl.user_session.set("startTime", str(start_time))
    cl.user_session.set("message_history", [])

    #Write session in log
    user = cl.user_session.get("user")
    user_data = user.metadata
    assert user_data, f"metadata is empty {user}"
    if not user_data.get("terms_of_use", False):
        try:
            has_accepted = await check_terms_of_use()
            cl.user_session.set("terms_of_use", has_accepted)

            if not has_accepted:
                await cl.Message(
                    content="Read and accept the terms of use. You can find them here:---",
                    actions=[cl.Action(name="Accept", value="accept", description="Accept the Terms of Use")],
                    #type = "user_message",
                    #disable_feedback = True,
                    author=AUTHOR
                ).send()
        except Exception as e:
            logger.error(f"Error writing tou message: {e}")
            await cl.Message(
                content="We are experiencing some technical problems. Please contact us.",
                author=AUTHOR,
            ).send()

            cl.user_session.set("terms_of_use", False)
            if __debug__ is True:
                raise

logger.info("Chat start was successful")

@cl.set_starters
async def set_starters():
    """Set the starters for the chat."""
    return [
        cl.Starter(
            label="Gives you an overview of the SIA features.", message="What can you do", icon="/public/idea.svg"
        ),
        cl.Starter(
            label="Generates an answer from the BASF knowledge base.",
            message="How to reset my password?",
            icon="/public/password.svg",
        ),
    ]

@cl.on_message
async def on_message(message: cl.Message):
    """Main function to handle incoming messages from the user."""
    logger.info("Received message from the user")

    user = cl.user_session.get("user")
    meta_data = user.metadata
    logger.debug(f"tou: {meta_data.get('terms_of_use')}")

    if meta_data.get("terms_of_use", False) is False and await check_terms_of_use() is False:
        logger.warning("User has not accepted the terms of use")
        await cl.Message(
            content="You have not accepted our terms of use yet. Please accept the terms of use first. If you don't see them please logout and in again. Thank you !",
            author=AUTHOR,
            # type="user_message",
            # disable_feedback=True,
        ).send()
        return

    # settings = cl.user_session.get("settings")

    _refresh_token = meta_data.get("refresh_token", "Empty")
    graph_token = meta_data.get("graph_token", "Empty")
    token_expires = meta_data.get("expires_at", "Empty")

    logger.trace(f"Token: {graph_token}")
    logger.trace(f"Refresh Token: {_refresh_token}")
    token = await refresh_token(token=graph_token, token_expires=token_expires, refresh_token=refresh_token)
    user.metadata.update(token)

    # Handle debug commands
    if __debug__ is True and message.content.startswith("/"):
        logger.info("Handling debug commands")
        await handle_debug_commands(message, user)
    else:
        logger.info("Handling user message")
        await handle_user_message(message, user)

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    """Function to handle the resume of the chat."""
    await cl.Message(f"Welcome back to {thread['name']}").send()
    if "metadata" in thread:
        await cl.Message(thread["metadata"], author="metadata", language="json").send()
    if "tags" in thread:
        await cl.Message(thread["tags"], author="tags", language="json").send()