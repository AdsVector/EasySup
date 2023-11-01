import os, asyncio
import discord
from discord.ext import commands
from easysup.help_command import CustomHelpCommand
from easysup.config.constants import BOT_PREFIX, BOT_TOKEN
from webserver import keep_alive


class EasySup(commands.Bot):

	def __init__(self) -> None:
		super().__init__(command_prefix=BOT_PREFIX,
		                 help_command=CustomHelpCommand(),
		                 intents=discord.Intents.all())

	async def setup_hook(self):
		for filename in os.listdir('easysup/commands'):
			try:
				if filename.endswith('.py'):
					await self.load_extension(f'easysup.commands.{filename[:-3]}')
			except Exception as e:
				print(e)

		for filename in os.listdir('easysup/slashcomms'):
			try:
				if filename.endswith('.py'):
					await self.load_extension(f'easysup.slashcomms.{filename[:-3]}')
			except Exception as e:
				print(e)

	async def on_ready(self):
		await self.change_presence(activity=discord.Game(name="Test"))
		print(f'{self.user} has connected to Discord!')


bot = EasySup()


async def main():
	async with bot:
		await bot.start(BOT_TOKEN)


asyncio.run(main())

keep_alive()
