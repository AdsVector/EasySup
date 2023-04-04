import discord
from discord.ext import commands
from easysup.config import config

class ReceiveButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Activar",style=discord.ButtonStyle.primary)
    async def yes_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        try:
            member = interaction.guild.get_member(interaction.user.id)
            await member.add_roles(self.role_receive)
            await interaction.response.send_message(content=f"Ahora recibiras notificaciones del canal Streames", ephemeral=True)
        except Exception as e:
            print(f"Yes <> An error occurred: {e}")
    
    @discord.ui.button(label="Desactivar",style=discord.ButtonStyle.red)
    async def no_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        try:
            member = interaction.guild.get_member(interaction.user.id)
            if self.role_receive in member.roles:
                await member.remove_roles(self.role_receive)
            
            await interaction.response.send_message(content=f"Ya no recibiras notificaciones directas, pero aun podras ver los avisos.", ephemeral=True)
        except Exception as e:
            print(f"No <> An error occurred: {e}")

    async def on_timeout(self):
        try:
            self.clear_items()
            await self.message.edit(content=config.TIMEOUT_MESSAGE, view=None)
        except Exception as e:
            print(f"TimeOut <> An error occurred: {e}")

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='ward', aliases=['otros'], invoke_without_command=True, pass_context=True)
    async def ward(self, ctx):
        await ctx.send('Comandos de ayuda multiple.')

    @commands.group(name='math', aliases=['calculator', 'calc'])
    async def calc(self, ctx):
        pass
    
    @ward.command(name='receive-state', aliases=['receive'])
    async def get_role_receive(self, ctx):
        await ctx.message.delete()

        role_receive_id = self.manager.get_value([str(ctx.message.guild.id), 'role_receive'], 0)
        role_receive    = ctx.guild.get_role(role_receive_id)
        if role_receive is None:
            ctx.send("No hay un rol activo para las menciones.")
            return 
        
        view = ReceiveButtons()
        view.role_receive = role_receive
        view.manager = self.manager
        view.message = await ctx.send("Aqui puedes activar/desactivar la mención de los avisos.", view=view)


    @ward.command(name="limpiar", aliases=['cls', 'clear', 'clean'], pass_context=True)
    async def clear(self, ctx, amount: int = 10):
        if amount > 0 and amount < 101:
            if ctx.channel.permissions_for(ctx.author).manage_messages:
                msg = await ctx.channel.purge(limit=(amount+1))
                await ctx.send(f'Se han a limpiar {len(msg)-1} mensajes por {ctx.author.mention}', delete_after=5)
        else:
            await ctx.send(f'{ctx.author.mention} Escriba un motón de mensajes entre 1 y 100.', delete_after=5)

    @ward.command(name="ping", aliases=['pong'])
    async def ping(self, ctx):
        mycl = 0x990000
        lant = round(self.bot.latency * 1000)

        if lant <= 50: mycl = 0x44ff44 
        elif lant <= 100: mycl = 0xffd000
        elif lant <= 200: mycl = 0xff6600
        else: mycl = 0x990000
        
        embed=discord.Embed(
            title="PING", 
            description=f":hammer_pick: The ping is **{lant}** milliseconds! :ping_pong:", 
            color=mycl)
        await ctx.send(embed=embed)
        
    @calc.command(name="Sumar", aliases=['sumar', 'plus'])
    async def sum(self, ctx, arg1, arg2):
        try:
            numOne = float(arg1)
            numTwo= float(arg2) 
        except ValueError:
            await ctx.send(f'{ctx.author.mention} no ingresó números validos!')
        else:
            await ctx.send(numOne + numTwo)

    @calc.command(name="Restar", aliases=['restar', 'subtract'])
    async def sum(self, ctx, arg1, arg2):
        try:
            numOne = float(arg1)
            numTwo= float(arg2) 
        except ValueError:
            await ctx.send(f'{ctx.author.mention} no ingresó números validos!')
        else:
            await ctx.send(numOne - numTwo)

async def setup(bot):
    await bot.add_cog(General(bot))