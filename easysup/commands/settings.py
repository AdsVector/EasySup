import discord 
from discord.ext import tasks, commands
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions

from easysup.config.constants import STREAMERS_PATH
from easysup.json_managers.JsonFileManager import JSON_Manager

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = JSON_Manager(STREAMERS_PATH)

    @commands.command(name='sync')
    @has_permissions(administrator=True)
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send("Estamos sicronizando los slash commands.")


async def setup(bot):
    await bot.add_cog(Settings(bot))