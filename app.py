import chainlit as cl
from loguru import logger
import json

@cl.on_message
async def main(message: str):
    # Create a pure JSON-serializable adaptive card payload
    adaptive_card_json = {
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "TextBlock",
            "size": "Medium",
            "weight": "Bolder",
            "text": "Order Confirmation"
        },
        {
            "type": "FactSet",
            "facts": [
                {"title": "Order ID:", "value": "1234"},
                {"title": "Total:", "value": "$34.99"}
            ]
        }
    ],
    "actions": [
        {"type": "Action.Submit", "title": "Confirm", "data": {"action": "confirm"}},
        {"type": "Action.Submit", "title": "Cancel", "data": {"action": "cancel"}}
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2"
}
    # Send as JSON string in content
    await cl.Message(content=json.dumps(adaptive_card_json)).send()