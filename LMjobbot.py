# Improved Parsing and Formatting for Discord Messages

import discord

class LMjobbot:
    def __init__(self):
        self.client = discord.Client()

    async def on_ready(self):
        print(f'Logged in as {self.client.user}')

    async def parse_message(self, message):
        # Improved parsing logic
        if message.author == self.client.user:
            return
        if message.content.startswith('!'):  # Command starts with '!', e.g., !help
            command = message.content[1:].lower()
            await self.handle_command(command, message.channel)

    async def handle_command(self, command, channel):
        # Improved formatting for Discord messages
        responses = {
            'help': 'Here is a list of commands you can use: \n !help - Show this help message \n !job - Get job updates',
            'job': 'Check out the latest job listings at [Job Link]!',
        }
        response = responses.get(command, 'Invalid command. Please type !help for the list of commands.')
        await channel.send(response)

    def run(self, token):
        self.client.run(token)