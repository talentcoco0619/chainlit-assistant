from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity, ActionTypes

class EchoBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # Echo back what the user said
        user_message = turn_context.activity.text
        await turn_context.send_activity(f"You said: {user_message}")