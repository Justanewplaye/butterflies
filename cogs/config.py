import discord
from discord.ext import commands

cmd_info = {
    "kick": ("kick <member> [reason]", "Kicks a member from the server."),
    "ban": ("ban <member> [reason]", "Bans a member from the server."),
    "hardban": ("hardban <member> [reason]", "Bans a member and deletes their last 7 days of messages."),
    "unban": ("unban <user_id>", "Unbans a user by their ID."),
    "mute": ("mute <member> [time] [reason]", "Mutes a member. Time format: 10m or 2h. Leave blank for permanent."),
    "timeout": ("timeout <member> <time> [reason]", "Times out a member. Time format: 10m or 2h."),
    "purge": ("purge <amount>", "Deletes a number of messages in the current channel."),
    "lock": ("lock", "Prevents everyone from sending messages in the channel."),
    "unlock": ("unlock", "Allows everyone to send messages in the channel again."),
    "slowmode": ("slowmode <seconds>", "Sets slowmode on the channel. Use 0 to disable."),
    "nick": ("nick <member> [name]", "Changes a member's nickname. Leave name blank to clear it."),
    "r": ("r <member> <role>", "Toggles a role on a member. Adds it if they don't have it, removes it if they do."),
    "warn": ("warn <member> [reason]", "Warns a member. Warnings are saved and can be viewed later."),
    "warnings": ("warnings <member>", "Shows all warnings for a member."),
    "clearwarns": ("clearwarns <member>", "Clears all warnings for a member."),
    "logs_config": ("logs_config <channel>", "Sets the channel where log events are sent."),
    "welcome_config": ("welcome_config <channel> [join_img] [leave_img]", "Sets the welcome channel and optional join/leave images."),
    "userinfo": ("userinfo [member]", "Shows info about a member. Defaults to yourself."),
    "avatar": ("avatar [member]", "Shows a member's avatar. Defaults to yourself."),
    "banner": ("banner [member]", "Shows a member's banner if they have one."),
    "afk": ("afk [reason]", "Sets you as AFK. You'll be unmarked when you send a message."),
    "roles": ("roles", "Lists all roles in the server with their IDs."),
    "whohas": ("whohas <role>", "Shows all members who have a specific role."),
    "steal": ("steal <emoji> <name>", "Adds an emoji from another server to this one."),
    "firstmsg": ("firstmsg [channel]", "Links to the very first message in a channel."),
    "membercount": ("membercount", "Shows the server's member count split by humans and bots."),
    "serverinfo": ("serverinfo", "Shows detailed info about the server."),
    "botinfo": ("botinfo", "Shows the bot's uptime, ping, and server count."),
    "remind": ("remind <time> <reminder>", "Reminds you after a set time. Example: !remind 10m check oven"),
    "8ball": ("8ball <question>", "Ask the magic 8ball a question."),
    "coinflip": ("coinflip", "Flips a coin. Heads or tails."),
    "roll": ("roll [sides]", "Rolls a dice. Defaults to 6 sides."),
    "ship": ("ship <user1> [user2]", "Ships two users and gives a compatibility score."),
    "pp": ("pp [member]", "Important scientific measurement."),
    "rate": ("rate <thing>", "Rates something out of 10."),
    "mock": ("mock <text>", "Converts text to mocking spongebob format."),
    "reverse": ("reverse <text>", "Reverses text."),
    "snipe": ("snipe", "Shows the last deleted message in the channel."),
    "poll": ("poll <question>", "Creates a yes/no poll."),
    "trivia": ("trivia", "Gives you a random trivia question to answer."),
    "tictactoe": ("tictactoe <member>", "Starts a game of tic tac toe against another member."),
    "color": ("color <hex>", "Shows info about a hex color. Example: !color ff5733"),
    "giveaway": ("giveaway <time> <prize>", "Starts a giveaway. Example: !giveaway 10m Nitro"),
    "hug": ("hug <member>", "Hugs someone."),
    "pat": ("pat <member>", "Pats someone on the head."),
    "slap": ("slap <member>", "Slaps someone."),
    "kiss": ("kiss <member>", "Kisses someone."),
}

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help_cmd(self, ctx, *, command: str = None):
        if command:
            cmd = command.lower().lstrip("!")
            if cmd not in cmd_info:
                return await ctx.send(embed=discord.Embed(description=f"No info for `{cmd}`.", color=0xed4245))
            usage, desc = cmd_info[cmd]
            e = discord.Embed(color=0x2b2d31)
            e.add_field(name="Usage", value=f"`!{usage}`", inline=False)
            e.add_field(name="Description", value=desc, inline=False)
            e.set_footer(text=ctx.author.name)
            return await ctx.send(embed=e)
        e = discord.Embed(title="Commands", color=0x2b2d31)
        e.add_field(name="Moderation", value="`kick` `ban` `hardban` `unban` `mute` `timeout` `purge` `lock` `unlock` `slowmode` `nick` `r` `warn` `warnings` `clearwarns`", inline=False)
        e.add_field(name="Config", value="`logs_config` `welcome_config`", inline=False)
        e.add_field(name="Utility", value="`userinfo` `avatar` `banner` `afk` `roles` `whohas` `steal` `firstmsg` `membercount` `serverinfo` `botinfo` `remind`", inline=False)
        e.add_field(name="Fun", value="`8ball` `coinflip` `roll` `ship` `pp` `rate` `mock` `reverse` `snipe` `poll` `trivia` `tictactoe` `color` `giveaway`", inline=False)
        e.add_field(name="Social", value="`hug` `pat` `slap` `kiss`", inline=False)
        e.add_field(name="Booster", value="`/br create` `/br name` `/br color` `/br give` `/br take` `/br delete`", inline=False)
        e.set_footer(text="!help <command> for more info")
        await ctx.send(embed=e)

    @commands.hybrid_command(name="logs_config")
    @commands.has_permissions(administrator=True)
    async def logs_config(self, ctx, channel: discord.TextChannel):
        self.bot.cfg['log_channel'] = channel.id
        self.bot.save_cfg()
        await ctx.send(embed=discord.Embed(description=f"Logs -> {channel.mention}", color=0x57f287))

    @commands.hybrid_command(name="welcome_config")
    @commands.has_permissions(administrator=True)
    async def welcome_config(self, ctx, channel: discord.TextChannel, join_img: str = None, leave_img: str = None):
        self.bot.cfg['welcome_channel'] = channel.id
        if join_img: self.bot.cfg['join_image'] = join_img
        if leave_img: self.bot.cfg['leave_image'] = leave_img
        self.bot.save_cfg()
        await ctx.send(embed=discord.Embed(description=f"Welcome -> {channel.mention}", color=0x57f287))

async def setup(bot):
    await bot.add_cog(Config(bot))
