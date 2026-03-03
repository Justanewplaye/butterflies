import discord, random
from discord.ext import commands

responses = [
    "yes", "no", "maybe", "absolutely not", "definitely",
    "ask again later", "don't count on it", "signs point to yes",
    "outlook not so good", "obviously", "no chance", "for sure"
]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="8ball")
    async def ball(self, ctx, *, question: str):
        await ctx.send(embed=discord.Embed(description=f"🎱 {random.choice(responses)}", color=0x2b2d31))

    @commands.hybrid_command()
    async def coinflip(self, ctx):
        await ctx.send(embed=discord.Embed(description=random.choice(["Heads", "Tails"]), color=0x2b2d31))

    @commands.hybrid_command()
    async def roll(self, ctx, sides: int = 6):
        await ctx.send(embed=discord.Embed(description=f"🎲 {random.randint(1, sides)}", color=0x2b2d31))

    @commands.hybrid_command()
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member = None):
        user2 = user2 or ctx.author
        pct = random.randint(0, 100)
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        e = discord.Embed(description=f"{user1.mention} 💗 {user2.mention}\n\n`{bar}` **{pct}%**", color=0xff6b9d)
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def pp(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        size = "8" + "=" * random.randint(0, 12) + "D"
        await ctx.send(embed=discord.Embed(description=f"{member.mention}'s pp:\n{size}", color=0x2b2d31))

    @commands.hybrid_command()
    async def rate(self, ctx, *, thing: str):
        n = random.randint(0, 10)
        await ctx.send(embed=discord.Embed(description=f"I rate **{thing}** a {n}/10", color=0x2b2d31))

    @commands.hybrid_command()
    async def mock(self, ctx, *, text: str):
        out = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))
        await ctx.send(embed=discord.Embed(description=out, color=0x2b2d31))

    @commands.hybrid_command()
    async def reverse(self, ctx, *, text: str):
        await ctx.send(embed=discord.Embed(description=text[::-1], color=0x2b2d31))

    @commands.hybrid_command()
    async def snipe(self, ctx):
        msg = self.bot.snipe.get(ctx.channel.id)
        if not msg:
            return await ctx.send(embed=discord.Embed(description="Nothing to snipe.", color=0x2b2d31))
        e = discord.Embed(description=msg.content or "No text", color=0xed4245)
        e.set_author(name=msg.author.name, icon_url=msg.author.display_avatar.url)
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def poll(self, ctx, *, question: str):
        e = discord.Embed(description=question, color=0x5865f2)
        e.set_footer(text=f"Poll by {ctx.author.name}")
        msg = await ctx.send(embed=e)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

async def setup(bot):
    await bot.add_cog(Fun(bot))
