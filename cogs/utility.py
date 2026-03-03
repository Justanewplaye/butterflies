import discord, requests, asyncio, datetime
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        e = discord.Embed(color=member.color)
        e.set_author(name=member.name)
        e.set_image(url=member.display_avatar.url)
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def banner(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user = await self.bot.fetch_user(member.id)
        if not user.banner:
            return await ctx.send("No banner.")
        e = discord.Embed()
        e.set_author(name=member.name)
        e.set_image(url=user.banner.url)
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        e = discord.Embed(color=member.color)
        e.set_author(name=member.name, icon_url=member.display_avatar.url)
        e.set_thumbnail(url=member.display_avatar.url)
        e.add_field(name="ID", value=member.id)
        e.add_field(name="Joined", value=member.joined_at.strftime("%b %d, %Y"))
        e.add_field(name="Boosting", value="Yes" if member.premium_since else "No")
        e.add_field(name="Roles", value=" ".join(roles) or "None", inline=False)
        await ctx.send(embed=e)

    @commands.hybrid_command()
    @commands.has_permissions(manage_roles=True)
    async def roles(self, ctx):
        lines = "\n".join(f"{r.mention} `{r.id}`" for r in reversed(ctx.guild.roles) if r.name != "@everyone")
        await ctx.send(embed=discord.Embed(title="Roles", description=lines or "None", color=0x5865f2))

    @commands.hybrid_command()
    @commands.has_permissions(manage_roles=True)
    async def whohas(self, ctx, *, role: discord.Role):
        members = [m.mention for m in role.members]
        desc = ", ".join(members) if members else "Nobody."
        if len(desc) > 4000:
            desc = desc[:3997] + "..."
        e = discord.Embed(title=role.name, description=desc, color=role.color)
        e.set_footer(text=f"{len(role.members)} members")
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def afk(self, ctx, *, reason: str = "AFK"):
        self.bot.afk[ctx.author.id] = reason
        await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} is AFK.", color=0xfaa61a))

    @commands.hybrid_command()
    @commands.has_permissions(manage_expressions=True)
    async def steal(self, ctx, emoji: str, name: str):
        obj = discord.PartialEmoji.from_str(emoji)
        data = requests.get(obj.url).content
        new = await ctx.guild.create_custom_emoji(name=name, image=data)
        await ctx.send(embed=discord.Embed(description=f"Added {new}", color=0x57f287))

    @commands.hybrid_command()
    async def firstmsg(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        msgs = [m async for m in channel.history(limit=1, oldest_first=True)]
        if not msgs:
            return await ctx.send("No messages found.")
        m = msgs[0]
        e = discord.Embed(description=f"[Jump to first message]({m.jump_url})", color=0x2b2d31)
        e.set_footer(text=f"Sent by {m.author.name} on {m.created_at.strftime('%b %d, %Y')}")
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def membercount(self, ctx):
        g = ctx.guild
        e = discord.Embed(color=0x2b2d31)
        e.set_author(name=g.name, icon_url=g.icon.url if g.icon else None)
        e.add_field(name="Members", value=g.member_count)
        e.add_field(name="Humans", value=sum(1 for m in g.members if not m.bot))
        e.add_field(name="Bots", value=sum(1 for m in g.members if m.bot))
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def botinfo(self, ctx):
        delta = datetime.datetime.utcnow() - self.bot.start_time
        h, rem = divmod(int(delta.total_seconds()), 3600)
        m, s = divmod(rem, 60)
        e = discord.Embed(color=0x2b2d31)
        e.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)
        e.add_field(name="Uptime", value=f"{h}h {m}m {s}s")
        e.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms")
        e.add_field(name="Servers", value=len(self.bot.guilds))
        await ctx.send(embed=e)

    @commands.hybrid_command()
    async def remind(self, ctx, time: str, *, reminder: str):
        unit = time[-1]
        if unit not in ('s', 'm', 'h'):
            return await ctx.send("Use s, m, or h. Example: `10m`")
        secs = int(time[:-1]) * {'s': 1, 'm': 60, 'h': 3600}[unit]
        await ctx.send(embed=discord.Embed(description=f"Reminder set for {time}.", color=0x57f287))
        await asyncio.sleep(secs)
        await ctx.send(f"{ctx.author.mention} reminder: {reminder}")

async def setup(bot):
    await bot.add_cog(Utility(bot))
