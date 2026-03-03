import discord
import ollama
import argparse
import asyncio
import os
import random

from search import search
from dotenv import load_dotenv
from datetime import date

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--maintenance', action='store_true')
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_queue = asyncio.Queue()
        self.worker_task = None
        self.maintenance_messages = [
            "I'm currently under maintenance. Should be back up soon! Thanks for waiting!",
            "I'm being updated rn... pls be patient, ty!",
            "Go touch some grass while I'm going through maintenance",
            "Hi :D. you should wait until i'm done being maintained."
        ]

    async def setup_hook(self):
        self.worker_task = asyncio.create_task(self.queue_worker())

    async def reply(self, message: discord.Message, content: str) -> None:
        await message.reply(content[0:2000])
        for i in range(2000, len(content), 2000):
            await message.channel.send(content[i:i+2000])

    async def queue_worker(self):
        while True:
            message, messages_payload = await self.request_queue.get()

            messages_payload.insert(0, {
                'role': 'system',
                'content': f'Be concise with your response. There is no need to overthink or overdo anything, but be friendly. Do not use markdown tables or LaTeX because they are unsupported (any other markdown is fine; you are allowed to use any formating during and only during thinking). If a query seems to require search (complex information, or anything after 2023), you are required to use the search tool and cite the sources used in your reply. The search tool takes in only one parameter called `query`, which should be a string. Note that today is {str(date.today())}.'
            })

            try:
                async with message.channel.typing():
                    final_content = None
                    
                    while True:
                        response = await asyncio.to_thread(
                            ollama.chat,
                            model=os.getenv("MODEL"),
                            messages=messages_payload,
                            tools=[search],
                            options={"temperature": 0.6} # Should help it use tools better without sacrificing too much creativity.
                        )

                        messages_payload.append(response.message)
                        
                        if not response.message.tool_calls:
                            final_content = response.message.content
                            break
                        
                        for tool in response.message.tool_calls:
                            function_name = tool.function.name
                            function_args = tool.function.arguments

                            tool_result = None

                            match function_name:
                                case 'search':
                                    tool_result = await asyncio.to_thread(
                                        search, 
                                        **function_args
                                    )
                                case _:
                                    tool_result = f"The tool {function_name} does not exist."

                            messages_payload.append({
                                'role': 'tool',
                                'content': str(tool_result),
                                'name': function_name, 
                            })

                    # 5. Send the final response to Discord
                    if args.debug:
                        await self.reply(message, f"Debug: {response}")

                    if final_content:
                        await self.reply(message, final_content)

            except Exception as e:
                await self.reply(message, f"Error: {e}")

            self.request_queue.task_done()

    async def on_message(self, message: discord.Message):
        if self.user is None: return
        if (f"<@{self.user.id}>" not in message.content):
            if message.reference is None: return
            lookahead_msg = await message.channel.fetch_message(message.reference.message_id)
            if not (lookahead_msg and lookahead_msg.author == self.user): return
        elif message.author == self.user: return

        if args.maintenance:
            await self.reply(message, random.choice(self.maintenance_messages))
            return

        messages = []
        current_msg = message

        while current_msg:
            if current_msg.author == self.user:
                messages.insert(0, {
                    'role': 'assistant',
                    'content': current_msg.content
                })
            else:
                messages.insert(0, {
                    'role': 'user',
                    'content': current_msg.content.replace(f"<@{self.user.id}>", "")
                })

            if current_msg.reference and current_msg.reference.message_id:
                try:
                    current_msg = await message.channel.fetch_message(current_msg.reference.message_id)
                except:
                    break
            else:
                break

        await self.request_queue.put((message, messages))


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv("BOT_KEY"))