# llm-bot
LLM Discord Bot for your servers!

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

## Usage:
Ping with @username for the bot to respond. It can see the entire reply chain as context.
