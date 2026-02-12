import discord
import ollama
import argparse
import asyncio
import os
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

    async def setup_hook(self):
        self.worker_task = asyncio.create_task(self.queue_worker())

    async def queue_worker(self):
        while True:
            message, messages_payload = await self.request_queue.get()

            try:
                response = await asyncio.to_thread(
                    ollama.chat,
                    model='gpt-oss:20b',
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

    async def on_message(self, message):
        if message.author == self.user:
            return

        if "<@1471265965583896801>" not in message.content:
            return

        if args.maintenance:
            await message.reply("I'm currently under maintenance. Should be back up soon! Thanks for waiting!")
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
                    'content': current_msg.content.replace("<@1471265965583896801>", "")
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
            'content': 'do not use markdown tables, as they are unsupported (any other markdown is fine)\nalso be concise with your response'
        })

        await self.request_queue.put((message, messages))


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv("BOT_KEY"))