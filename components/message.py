"""Handle user message."""

import json

from loguru import logger
import chainlit as cl
from aiohttp import ClientSession

from helper.constants import AUTHOR, SIA_URL, DEFAULT_TIMEOUT
from helper.web import stream_ndjson

async def stream_sia(payload: dict, headers: dict, params: dict):
    """Stream user message to SIA."""
    async with ClientSession(trust_env=True) as session:
        async with session.post(
            url=SIA_URL, json=payload, params=params, timeout=DEFAULT_TIMEOUT, headers=headers
        ) as response:
            response.raise_for_status()

            async for response_data in stream_ndjson(response):
                context: str = response_data["context"]
                if context == "message":
                    # logger.trace(response_data["data"])
                    data = response_data["data"]
                    yield data, None
                elif context == "actions":
                    data = response_data["data"]
                    data = "```" + json.dumps(data, indent=2) + "```"
                    yield data, None

                elif context == "file":
                    logger.info("Adding file to message")
                    logger.trace(response_data["data"])
                    for data in response_data["data"]:
                        name = data["path"].split("/")[-1]
                        file = cl.File(name=name, url=data["url"], display="inline")
                        yield None, file
                elif context == "actions" or context == "action":
                    logger.info("Action context")
                    logger.info(f"Action data: {response_data}")
                else:
                    logger.warning(f"Unknown context type: {context}")

async def handle_message(message: cl.Message, user: cl.User, user_token: str):
    """Handle user message."""
    await cl.Message(content="message received").send()

    # Create an empty message to stream into
    msg = cl.Message(
        content="",
        author=AUTHOR,
    )
    await msg.send()

    payload = {
        "prompt": message.content,
        "platform": "Chainlit",
        "requestor": "user",
        "model": "End Users",
        "messageId": message.id,
        "sessionId": user.metadata["sessionId"],
        "usedDevice": "web",
    }

    headers = {"authorization": f"Bearer {user_token}"}
    params = {"stream": "true"}

    async for object in stream_sia(payload, headers, params):
        response_msg, element=object

        if response_msg:
            await msg.stream_token(token=response_msg)

    await msg.send()