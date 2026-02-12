# llm-bot
Locally Hosted LLM Discord Bot for your servers!

Ping with @username for the bot to respond. It can see the entire reply chain as context.

## Setup:
1. Create a Python environment and install the packages in requirements.txt
2. Install Ollama (if needed) and a model
3. Modify the model in main.py to whatever model you are running: `model='MODEL HERE',`
4. Create an application on ther Discord Developer Portal: https://discord.com/developers/applications
5. Go to the "Bot" tab on the left
6. Make sure "Message Content Intent" is on
7. Click on the "Reset Token" button and copy it
8. Create a `.env` file, and put in `BOT_KEY=TOKEN HERE`
9. Run the bot server with `python main.py`

### Some potential pointers
1. Be sure to allow both user install and guild install.
2. From there, you can simply use the install link in `Installation` tab in settings.

## Features:
- Responds to messages with a Ollama model
- Sees reply chain as context
- Queues messages when there's a lot coming in at the same time
- Splits long output among several Discord messages when needed due to the message character limit

### Current Differences from the base repo
- No need to ping the bot when replying to it
- Easier setup through `self.user.id`
- Specify the model in `.env`. No need to be stuck on `gpt-oss:20b`

## Roadmap:
- Allow the model to search for information on the web
  - This will be pulled from the base repo when it's implemented.
