import chainlit as cl
from botbuilder.core import CloudAdapter, BotFrameworkHttpClient
from botbuilder.schema import Activity
from echo_bot import EchoBot

# Initialize the bot
bot = EchoBot()

# Create a CloudAdapter
adapter = CloudAdapter()

@cl.on_message
async def main(message: str):
    # Create an Activity object from the user's message
    activity = Activity(
        type="message",
        text=message,
        from_property={"id": "user", "name": "User"},
        recipient={"id": "bot", "name": "Bot"},
        channel_id="chainlit",
    )

    #Process the activity using the bot
    async def callback(turn_context):
        await bot.on_turn(turn_context)

    # Use the CloudAdapter to process the activity
    await adapter.process_activity(activity, "", callback)