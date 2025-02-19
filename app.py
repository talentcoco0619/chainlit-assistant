"""Main application file.
To run this local do: "cd web/sia-web && clear && python -m chainlit run app.py --port 8001 -w -d"
"""

import os
import sys
import uuid

import chainlit as cl
from loguru import logger

from helper.constants import AUTHOR

from chainlit.oauth_providers import providers

import components
from components.auth import CustomEntraIdOAuthProvider

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

logger.remove()
logger.add(
    sys.stdout,
    level=LOGGING_LEVEL,
    colorize=True,
)

providers[2] = CustomEntraIdOAuthProvider()

@cl.oauth_callback
async def oauth_callback(
    provider_id: str,
    token: str,     #this token is valid graph token
    raw_user_data: dict[str, str],
    default_user: cl.User,
    redirected_uri: str | None = None,
) -> cl.User | None:
    """Handle OAuth callback."""
    logger.info(token)

    logger.trace(default_user.metadata)

    #1. This works
    #del default_user.metadata["image"]
    #default_user.metadata["token"] = token

    #2. This does not work = unauthorized in terminal and blank browser
    #default_user.metadata["token"] = token

    #3. This results in an error:
    #cl.user_session.set("token", token)

    default_user.display_name = raw_user_data["displayName"]
    default_user.metadata["sessionId"] = str(uuid.uuid4())

    return default_user

@cl.on_message
async def main(message: cl.Message):
    """Handle user message."""

    logger.trace(message.content)

    user:cl.User | None = cl.user_session.get("user", None)
    logger.trace(user)
    if user is None:
        msg = "User not found in session."
        raise ValueError(msg)
    
    user_token: str = user.metadata["graph_token"]


    #user_token: str | None = cl.user_session.get("http_cookie")
    #user_token: str | None = TOKEN_MAP.get(user.identifier)

    logger.debug(user_token)
    if not user_token:
        await cl.Message(content="User token not found in session.", author=AUTHOR).send()
        raise ValueError("User token not found in session.")
    
    if message.content.startswith("/"):
        stop = await components.handle_commands(message, user, user_token)
        if stop is True:
            return
        
    await components.handle_message(message, user, user_token)