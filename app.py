# import chainlit as cl

# async def get_ticket():
#     """Pretending to fetch data from linear"""
#     return {
#         "title": "Fix Authentication Bug",
#         "status": "in-progress",
#         "assignee": "Sarah Chen",
#         "deadline": "2025-01-15",
#         "tags": ["security", "high-priority", "backend"]
#     }

# @cl.on_message
# async def on_message(msg: cl.Message):
#     # Let's pretend the user is asking about a linear ticket.
#     # Usually an LLM with tool calling would be used to decide to render the component or not.
    
#     props = await get_ticket()
    
#     ticket_element = cl.CustomElement(name="LinearTicket", props=props)
#     # Store the element if we want to update it server side at a later stage.
#     cl.user_session.set("ticket_el", ticket_element)
    
#     await cl.Message(content="Here is the ticket information!", elements=[ticket_element]).send()

import chainlit as cl


@cl.on_chat_start
async def main():
    res = await cl.AskActionMessage(
        content="Pick an action!",
        actions=[
            cl.Action(name="continue", payload={"value": "continue"}, label="✅ Continue"),
            cl.Action(name="cancel", payload={"value": "cancel"}, label="❌ Cancel"),
        ],
    ).send()

    if res and res.get("payload").get("value") == "continue":
        await cl.Message(
            content="Continue!",
        ).send()