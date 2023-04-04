import discord 
from discord import app_commands
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions, MissingPermissions

from easysup.config import config
from easysup.utils import format_message
from easysup.manager.JsonFileManager import JSON_Manager
from easysup.twitch_api_comm import GetStreamData, GetUserData
from easysup.tools.embeds import EmbedNotification

class Notification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = JSON_Manager(config.STREAMERS_PATH)
        self.live_notif_loop.start()

    @tasks.loop(minutes=15)
    async def live_notif_loop(self):
        print(config.CHECKING_LIVE_USERS)
        self.manager.read_file()
        try:
            for guild_id, guild_data in self.manager.data.items():
                
                if not guild_data.get('notify'):
                    continue
                
                guild = self.bot.get_guild(int(guild_id))
                if guild is None:
                    print(f"Guild with ID {guild_id} not found")
                    continue

                channel_id, streamer_role_id , receive_role_id = guild_data['settings'].values()

                channel    = self.bot.get_channel(channel_id)
                if channel is None:
                    print(f"Channel with ID {channel_id} not found in guild {guild.name}")
                    continue
            
                role_streamer    = guild.get_role(streamer_role_id)
                if role_streamer is None and streamer_role_id != 0:
                    print(f"Streamer: Role with ID {streamer_role_id} not found in guild {guild.name}")

                role_receive    = guild.get_role(receive_role_id)
                if role_receive is None and receive_role_id != 0:
                    print(f"Receive: Role with ID {receive_role_id} not found in guild {guild.name}")

                streamers = list(guild_data.get('streamers').keys())
                all_users = GetStreamData(streamers)
                
                for streamer_data in all_users:      
                    user_login = streamer_data['user_login']
                    user_id, message, sent = guild_data['streamers'][user_login].values()
                    member  = guild.get_member(user_id)
                    is_live = streamer_data['is_live']
   
                    if member and role_streamer:
                        if is_live:
                            await member.add_roles(role_streamer)
                        elif role_streamer in member.roles:
                            await member.remove_roles(role_streamer)
                
                    if not is_live or sent:
                        continue

                    if message:               
                        message = format_message(message, streamer_data)

                    if role_receive:
                        message = (message or "") + f'\n   ||{role_receive.mention}||'

                    user_data = GetUserData(user_login)
                    embed     = EmbedNotification(streamer_data, user_data)

                    await channel.send(content=message, embed=embed)    
                    
                    self.manager.update_element(
                                [str(guild_id), 'streamers', user_login], 'sent', is_live)   
  

        except Exception as e:
            print(f"An error occurred: {e}")
            
    @live_notif_loop.before_loop
    async def before_live_notif(self):
        print(config.WAITING_MESSAGE)
        await self.bot.wait_until_ready()

    @commands.command(name='Turn_On', aliases=['on', 'online'])
    async def turn_on_notifications(self, ctx):
        #self.live_notif_loop.start()
        guild_id = ctx.message.guild.id
        self.manager.update_element([str(guild_id)], 'notify', True)      
        await ctx.send("Ha activado la notificaciones de Twitch.")

    @commands.command(name='Turn_Off', aliases=['off', 'offline'])
    async def turn_off_notifications(self, ctx):
        #self.live_notif_loop.cancel()
        guild_id = ctx.message.guild.id
        self.manager.update_element([str(guild_id)], 'notify', False)
        await ctx.send("Notificaciones de Twitch: Desactivadas")
    


async def setup(bot):
    await bot.add_cog(Notification(bot))