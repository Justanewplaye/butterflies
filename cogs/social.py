import discord, requests
from discord.ext import commands

def get_gif(action):
    try:
        return requests.get(f"https://nekos.life/api/v2/img/{action}").json()['url']
    except:
        return None

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def hug(self, ctx, member: discord.Member):
        url = get_gif("hug")
        e = discord.Embed(description=f"{ctx.author.mention} hugs {member.mention}", color=0xff9ff3)
        if url: e.set_image(url=url)
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def pat(self, ctx, member: discord.Member):
        url = get_gif("pat")
        e = discord.Embed(description=f"{ctx.author.mention} pats {member.mention}", color=0xff9ff3)
        if url: e.set_image(url=url)
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def slap(self, ctx, member: discord.Member):
        url = get_gif("slap")
        e = discord.Embed(description=f"{ctx.author.mention} slaps {member.mention}", color=0xed4245)
        if url: e.set_image(url=url)
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def kiss(self, ctx, member: discord.Member):
        url = get_gif("kiss")
        e = discord.Embed(description=f"{ctx.author.mention} kisses {member.mention}", color=0xff6b9d)
        if url: e.set_image(url=url)
        await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(Social(bot))
