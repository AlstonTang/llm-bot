# llm-bot
Locally Hosted LLM Discord Bot for your servers!

Ping with @username or reply to the bot's message for the bot to respond. It can see the entire reply chain as context.

## Setup:
1. Create a Python environment and install the packages in requirements.txt
2. Install Ollama (if needed) and a model
3. Create an application on the Discord Developer Portal: https://discord.com/developers/applications
4. Go to the "Bot" tab on the left
5. Make sure "Message Content Intent" is on
6. Click on the "Reset Token" button and copy it
7. Create a `.env` file, and put in `BOT_KEY=TOKEN HERE`, as well as `MODEL=MODEL HERE`
8. Run the bot server with `python main.py`

### Some potential pointers
1. Be sure to allow both user install and guild install.
2. From there, you can simply use the install link in `Installation` tab in settings.

## Features:
- Responds to messages with a Ollama model
- Sees reply chain as context
- Queues messages when there's a lot coming in at the same time
- Splits long output among several Discord messages when needed due to the message character limit

## Roadmap:
- Allow the model to search for information on the web
