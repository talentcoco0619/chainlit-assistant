import json
import time
import base64
# from sia_sdk.defaults.times import VERY_LONG_PLUS_TIMEOUT
from helper import (
    AUTHOR,
    ROOT_URL,
    COMMAND_AUTHOR,
    stream_ndjson,
)
from loguru import logger
from aiohttp import ClientSession
import aiofiles
import chainlit as cl
import chainlit.data as cl_data

VERY_LONG_PLUS_TIMEOUT = 600

async def handle_debug_commands(message: cl.Message, user: cl.User) -> cl.Message:
    """Handle debug commands"""
    graph_token: str = user.metadata["graph_token"]
    _refresh_token: str = user.metadata["refresh_token"]

    if message.content == "/token":
        await cl.Message(
            content = graph_token,
            author=COMMAND_AUTHOR,
            # type="user_message",
            disable_feedback=True,
        ).send()
    elif message.content == "/refresh_token":
        await cl.Message(
            content =_refresh_token,
            author=COMMAND_AUTHOR,
            # type="user_message",
            disable_feedback=True,
        ).send()
    elif message.content == "/refresh_token()":
        await cl.Message(
            content ="Token refresh",
            author=COMMAND_AUTHOR,
            # type="user_message",
            disable_feedback=True,
        ).send()
    elif message.content == "/delete_token":
        del user.metadata["graph_token"]
        await cl.Message(
            content =user.metadata.get("graph_token", "Empty"),
            author=COMMAND_AUTHOR,
            # type="user_message",
            disable_feedback=True,
        ).send()
    elif message.content == "/openai_speedtest":
        msg = cl.Message(
            content = "Starting to test openai response times",
            author=COMMAND_AUTHOR,
            # type="user_message",
            disable_feedback=True,
        )
        await msg.send()
        start_time = time.perf_counter()
        async with ClientSession(trust_env=True) as session:
            response = await session.get("http://utils/v1/openai/runSpeedTest", timeout=3_600)
            response.raise_for_status()

        measured_time = time.perf_counter() - start_time
        await msg.stream_token("\nSuccessfully finished the test.")
        await msg.stream_token(f"\nThe speedtest took '{measured_time:.2f}'seconds.")
        await msg.update()
    # elif message.content = "/test": # TODO: only test stuff inside your group (user/serviceDesk)
    # Filter out tests by groups
    # test like in test_all
    elif message.content == "/test_all": # TODO: test all prompts
        await cl.Message(
            content="Starting to test some prompts.",
            author=COMMAND_AUTHOR,
            # type="user_message",
            disable_feedback=True,
        ).send()

        with open("./assets/sia-test.json") as f:
            payload = json.load(f)

        #Create all test messages
        messages = {
            item["prompt"]: cl.Message(
                content=item["prompt"] + "\n",
                author=COMMAND_AUTHOR,
                type="system_message",
            )
            for item in payload["tests"]
        }
        # send all test messages
        for message in messages.values():
            await message.send()

        headers = {"Authorization": f"Bearer {graph_token}"}
        params = {"stream": "true"}
        async with ClientSession(trust_env=True) as session:
            async with session.post(
                url="http://utils/v1/testall",            json=payload, params=params, timeout=3_600, headers=headers
            ) as response:
                response.raise_for_status()

                async for response_data in stream_ndjson(response):
                    #logger.trace(response_data)
                    context = response_data["context"]
                    data = response_data["data"]
                    error = response_data["error"]
                    status = response_data["status"]
                    prompt = response_data["prompt"]
                    model = response_data["model"]
                    response_time = response_data["time"]

                    if context == "sessionInfo":
                        if error is not None:
                            await messages[prompt].stream_token(f"\nWorkflow failed with exception: {error}\n\n")
                        else:
                            await messages[prompt].stream_token(f"\nSelected workflow: {data['workflowName']}\n\n")
                    elif context == "message":
                        output = (
                            data
                            if status in ["running", "failed"]
                            else f"{data}\nModel:{model}\nTime:{response_time}\n{data}"
                        )

                        await messages[prompt].stream_token(output)
                    else:
                        # TODO: Implement other contexts support
                        pass

async def handle_user_message(message: cl.Message, user:cl.User) -> cl.Message:
    """Handle the user message"""
    graph_token: str = user.metadata["graph_token"]

    msg = cl.Message(
        content="",
        author=AUTHOR,
        # type="system_message",
    )
    await msg.send()

    images = []
    if message.elements:
        for file in message.elements:
            if "image" not in file.mime:
                continue

            async with aiofiles.open(file.path, "rb") as file:
                data = await file.read()
                encoded_image = base64.b64encode(data).decode("ascii")
                images.append(encoded_image)

    # append user message to history
    message_history = cl.user_session.get("message_history")[::]
    assert len(message_history) % 2 == 0, "Message history is not even."
    cl.user_session.get("message_history").append({"role": "user", "content": message.content})

    payload = {
        "prompt": message.content,
        "images": images,
        # "workflow": None,
        # "workflowArgs": None,
        "platform": "Chainlit",
        "requestor": "user",
        "model": "End Users",
        "history": message_history,
        "debugLevel": "basic",
        "messageId": message.id,
        "sessionId": cl.user_session.get("id"),
        "usedDevice": "web",
    }
    # logger.trace(payload)
    headers = {"authorization": f"Bearer {graph_token}"}
    params = {"stream": "true"}

    ### RESPONSE initialization ###
    task_list = cl.TaskList(name="Steps")
    elements = []
    actions = []    #NOT YET USED
    status = "Running..."
    task_list.status = status
    #######################
    async with ClientSession(trust_env=True) as session:
        async with session.post(
            url=ROOT_URL, json=payload, params=params, timeout=VERY_LONG_PLUS_TIMEOUT, headers=headers
        ) as response:
            response.raise_for_status()

            async for response_data in stream_ndjson(response):
                context: str = response_data["context"]
                if context == "message":
                    #logger.trace(response_data["data"])
                    data = response_data["data"]
                    await msg.stream_token(data)
                elif context == "actions":
                    data = response_data["data"]
                    data = "```" + json.dumps(data, indent=2) + "```"
                    await msg.stream_token(token=data)

                elif context == "file":
                    logger.info("Adding file to message")
                    logger.trace(response_data["data"])
                    for data in response_data["data"]:
                        name = data["path"].split("/")[-1]
                        file = cl.File(name=name, url=data["url"], display="inline")
                        elements.append(file)
                elif context == "sessionInfo":
                    logger.info(response_data["data"])
                    session_data = response_data["data"]
                    if __debug__ is True:
                        async with cl.Step(name="SessionInfo") as step:
                            step.output = session_data
                elif context == "tasklist":
                    if __debug__ is True:
                        for iteration in response_data["data"]:
                            for step in iteration:
                                task = cl.Task(title=str(step["name"]), status=cl.TaskStatus.READY, forId=step["identifier"])
                                await task_list.add_task(task)
                        await task_list.send()
                        await msg.update()
                elif context == "stepStatus":
                    if __debug__ is True:
                        logger.info(f"Step {response_data['data']} is done")
                        logger.info(f"Task list: {task_list}")
                        try:
                            task_id = [
                                task_id
                                for task_id, task in enumerate(task_list.tasks)
                                if task.forId == response_data["data"]
                            ][0]
                            task_list.tasks[task_id].status = cl.TaskStatus.DONE
                            await task_list.send()
                            await msg.update()
                        except IndexError:
                            logger.warning(f"Task {response_data['data']} not found in task list")
                elif context == "actions" or context == "action":
                    logger.info("Action context")
                    logger.info(f"Action data: {response_data}")
                else:
                    raise TypeError(f"Unknown context type: {context}")

    msg.elements = elements
    await msg.update()

    task_list.status = "Done"
    await task_list.send()

    cl.user_session.get("message_history").append({"role": "assistant", "content": msg.content})

    if message and cl_data._data_layer:
        cl_data._data_layer.id = message.id
