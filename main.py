import discord
import ollama
import argparse
import asyncio
import os
import random
from dotenv import load_dotenv

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

    async def queue_worker(self):
        while True:
            message, messages_payload = await self.request_queue.get()

            try:
                async with message.channel.typing():
                    response = await asyncio.to_thread(
                        ollama.chat,
                        model=os.getenv("MODEL"),
                        messages=messages_payload
                    )

                    if args.debug:
                        await message.reply(response)

                    response_content = response['message']['content']

                    await message.reply(response_content[0:2000])
                    for i in range(2000, len(response_content), 2000):
                        await message.channel.send(response_content[i:i+2000])

            except Exception as e:
                await message.reply(f"Error: {e}")

            self.request_queue.task_done()

    async def on_message(self, message: discord.Message):
        if (f"<@{self.user.id}>" not in message.content):
            lookahead_msg = await message.channel.fetch_message(message.reference.message_id)
            if not (lookahead_msg and lookahead_msg.author == self.user): return
        elif message.author == self.user: return

        if args.maintenance:
            await message.reply(random.choice(self.maintenance_messages))
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

        messages.insert(0, {
            'role': 'system',
            'content': 'Do not use markdown tables because they are unsupported (any other markdown is fine). Also, be concise with your response. There is no need to overthink or overdo anything.'
        })

        await self.request_queue.put((message, messages))


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv("BOT_KEY"))