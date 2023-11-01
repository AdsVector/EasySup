import discord 
from discord import app_commands
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions, MissingPermissions

from ..config.constants import STREAMERS_PATH, CHECKING_LIVE_USERS, WAITING_MESSAGE
from easysup.utils.utils import format_message, get_role
from easysup.json_managers import TW_Manager
from easysup.twitch_api_comm import GetStreamData, GetUserData
from easysup.tools.embeds import EmbedNotification

class Notification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = TW_Manager(STREAMERS_PATH)
        self.live_notif_loop.start()

    @tasks.loop(minutes=15)
    async def live_notif_loop(self):
        print(CHECKING_LIVE_USERS)
        self.manager.read_file()
        try:
            for guild_id in self.manager.getAllGuilds():
                actived, channel_id, role_receive_id, role_streamer_id = self.manager.getSettingsGuild(guild_id)
                
                if not actived: 
                    continue
                
                guild = self.bot.get_guild(int(guild_id))
                if guild is None :
                    print(f"Guild with ID {guild_id} not found")
                    continue
                
                channel    = self.bot.get_channel(channel_id)
                if channel is None:
                    print(f"Channel with ID {channel_id} not found in guild {guild.name}")
                    continue
            
                role_streamer = get_role(guild, role_streamer_id)
                role_receive = get_role(guild, role_receive_id)

                streamer_list = self.manager.getStreamersByGuildID(guild_id)
                all_users = GetStreamData(streamer_list)
                
                for streamer_data in all_users:      
                    user_login = streamer_data['user_login']
                    user_id, message, sent = self.manager.getStreamerByID(user_login)
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
        print(WAITING_MESSAGE)
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