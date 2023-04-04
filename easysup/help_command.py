import discord
from discord.ext import commands
import itertools

class CustomHelpCommand(commands.DefaultHelpCommand):
    clean_prefix = "$"

    def command_not_found(self, command):
        return f'Command `{command}` is not found'

    def subcommand_not_found(self, command, subcommand):
        if isinstance(command,
                      commands.Group) and len(command.all_commands) > 0:
            return f'Subcommand `{subcommand}` of `{command.qualified_name}` is not found'
        return f'Command `{command.qualified_name}` has no subcommands'

    async def send_error_message(self, error):
        destination = self.get_destination()
        await destination.send(f':x: {error}.', delete_after=5)
        await self.context.message.delete(delay=5)

    async def send_bot_help(self, mapping):
        try:
            ctx = self.context
            bot = ctx.bot

            embed = discord.Embed(title=':scroll: Help', color=discord.Color.gold()) \
            .set_footer(text=f'Type\u2002{self.clean_prefix}help <command>\u2002for more info on a command.\nYou can also type\u2002{self.clean_prefix}help <category>\u2002for more info on a category.')

            def get_category(command, *, no_category='No Category'):
                cog = command.cog
                return cog.qualified_name if cog is not None else no_category

            filtered = await self.filter_commands(bot.commands,
                                              sort=True,
                                              key=get_category)
            to_iterate = itertools.groupby(filtered, key=get_category)
            max_size = self.get_max_size(bot.commands)

            for cog_name, commands in to_iterate:
                commands = sorted(commands, key=lambda c: c.name)

                cog = bot.get_cog(cog_name)
                text = cog.description + '\n' if (cog is not None and
                                                  cog.description) else ''

                text += ', '.join([
                    f'`{self.clean_prefix}{command.name}`' for command in commands
                ])

                embed.add_field(name=cog_name, value=text, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"An error occurred: {e}")

    async def send_cog_help(self, cog):
        ctx = self.context

        embed = discord.Embed(title=':scroll: Help', color=discord.Color.gold())

        if cog.description:
            embed.add_field(name='Description',
                            value=cog.description,
                            inline=False)

        commands = await self.filter_commands(cog.get_commands(), sort=True)
        if commands:
            embed.add_field(name='Commands',
                            value=', '.join([
                                f'`{self.clean_prefix}{command.name}`'
                                for command in commands
                            ]),
                            inline=False)
        else:
            embed.description = 'No commands in category'
        await ctx.send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context

        embed = discord.Embed(title=':scroll: Help', color=discord.Color.gold())

        commands = await self.filter_commands(group.commands, sort=True)
        if commands:
            embed.add_field(name='Commands',
                            value=', '.join([
                                f'`{self.clean_prefix}{command.name}`'
                                for command in commands
                            ]),
                            inline=False)
        else:
            embed.description = 'No commands in this group'
        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        ctx = self.context

        embed = discord.Embed(title=':scroll: Help', color=discord.Color.gold())
        if command.description:
            embed.add_field(name='Description',
                            value=command.description,
                            inline=False)
        elif command.help:
            embed.add_field(name='Description',
                            value=command.help,
                            inline=False)
        embed.add_field(name='Usage',
                        value=f'`{self.get_command_signature(command)}`',
                        inline=False)

        await ctx.send(embed=embed)