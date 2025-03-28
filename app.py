import chainlit as cl

@cl.on_message
async def main():
    html_content = """
    <p id="content">This is <b>HTML</b> content!</p>
    <script src="https://unpkg.com/adaptivecards/dist/adaptivecards.js"></script>
"""
    await cl.Message(content=html_content).send()

