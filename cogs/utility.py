import discord, requests
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

async def setup(bot):
    await bot.add_cog(Utility(bot))
