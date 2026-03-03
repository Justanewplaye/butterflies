import discord
from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help_cmd(self, ctx):
        e = discord.Embed(title="Commands", color=0x2b2d31)
        e.add_field(name="Moderation", value="`kick` `ban` `hardban` `unban` `mute` `timeout` `purge` `lock` `unlock` `slowmode` `nick` `r` `warn` `warnings` `clearwarns`", inline=False)
        e.add_field(name="Config", value="`logs_config` `welcome_config`", inline=False)
        e.add_field(name="Utility", value="`userinfo` `avatar` `banner` `afk` `roles` `whohas` `steal` `firstmsg` `membercount` `serverinfo` `botinfo` `remind`", inline=False)
        e.add_field(name="Fun", value="`8ball` `coinflip` `roll` `ship` `pp` `rate` `mock` `reverse` `snipe` `poll` `trivia` `tictactoe` `color` `giveaway`", inline=False)
        e.add_field(name="Social", value="`hug` `pat` `slap` `kiss`", inline=False)
        e.add_field(name="Booster", value="`/br create` `/br name` `/br color` `/br give` `/br take` `/br delete`", inline=False)
        e.set_footer(text=ctx.author.name)
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
