import discord, asyncio, datetime
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        await member.kick(reason=reason)
        await ctx.send(embed=discord.Embed(description=f"Kicked {member.mention}", color=0xed4245))

    @commands.hybrid_command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        await member.ban(reason=reason)
        await ctx.send(embed=discord.Embed(description=f"Banned {member.mention}", color=0xed4245))

    @commands.hybrid_command()
    @commands.has_permissions(ban_members=True)
    async def hardban(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        await member.ban(reason=reason, delete_message_days=7)
        await ctx.send(embed=discord.Embed(description=f"Hardbanned {member.mention} (messages cleared)", color=0xed4245))

    @commands.hybrid_command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: str):
        user = await self.bot.fetch_user(int(user_id))
        await ctx.guild.unban(user)
        await ctx.send(embed=discord.Embed(description=f"Unbanned {user.name}", color=0x57f287))

    @commands.hybrid_command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: str = None, *, reason: str = "No reason"):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            return await ctx.send("No 'Muted' role found.")
        await member.add_roles(role)
        await ctx.send(embed=discord.Embed(description=f"Muted {member.mention} ({time or 'perm'})", color=0x99aab5))
        if time:
            secs = int(time[:-1]) * (60 if time[-1] == 'm' else 3600)
            await asyncio.sleep(secs)
            if role in member.roles:
                await member.remove_roles(role)

    @commands.hybrid_command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(embed=discord.Embed(description=f"Cleared {amount} messages."), delete_after=5)

    @commands.hybrid_command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(embed=discord.Embed(description="Locked", color=0xed4245))

    @commands.hybrid_command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(embed=discord.Embed(description="Unlocked", color=0x57f287))

    @commands.hybrid_command(name="r")
    @commands.has_permissions(manage_roles=True)
    async def toggle_role(self, ctx, member: discord.Member, *, role: discord.Role):
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(embed=discord.Embed(description=f"Removed {role.mention} from {member.mention}", color=0xed4245))
        else:
            await member.add_roles(role)
            await ctx.send(embed=discord.Embed(description=f"Gave {role.mention} to {member.mention}", color=0x57f287))

    @commands.hybrid_command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, time: str, *, reason: str = "No reason"):
        unit = time[-1]
        if unit not in ('s', 'm', 'h'):
            return await ctx.send("Use s, m, or h. Example: `10m`")
        secs = int(time[:-1]) * {'s': 1, 'm': 60, 'h': 3600}[unit]
        until = discord.utils.utcnow() + datetime.timedelta(seconds=secs)
        await member.timeout(until, reason=reason)
        await ctx.send(embed=discord.Embed(description=f"Timed out {member.mention} for {time}.", color=0x99aab5))

    @commands.hybrid_command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        txt = f"Slowmode set to {seconds}s." if seconds else "Slowmode disabled."
        await ctx.send(embed=discord.Embed(description=txt, color=0x57f287))

    @commands.hybrid_command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, name: str = None):
        await member.edit(nick=name)
        txt = "Nickname cleared." if not name else f"Nickname set to **{name}**."
        await ctx.send(embed=discord.Embed(description=txt, color=0x57f287))

    @commands.hybrid_command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        gid, uid = str(ctx.guild.id), str(member.id)
        self.bot.warns.setdefault(gid, {}).setdefault(uid, []).append({'reason': reason, 'mod': ctx.author.name})
        self.bot.save_warns()
        count = len(self.bot.warns[gid][uid])
        await ctx.send(embed=discord.Embed(description=f"Warned {member.mention} ({count} total). Reason: {reason}", color=0xfaa61a))

    @commands.hybrid_command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        gid, uid = str(ctx.guild.id), str(member.id)
        warns = self.bot.warns.get(gid, {}).get(uid, [])
        if not warns:
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} has no warnings.", color=0x57f287))
        lines = "\n".join(f"`{i+1}.` {w['reason']} — by {w['mod']}" for i, w in enumerate(warns))
        await ctx.send(embed=discord.Embed(title=f"Warnings for {member.name}", description=lines, color=0xfaa61a))

    @commands.hybrid_command()
    @commands.has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member):
        gid, uid = str(ctx.guild.id), str(member.id)
        if gid in self.bot.warns and uid in self.bot.warns[gid]:
            self.bot.warns[gid].pop(uid)
            self.bot.save_warns()
        await ctx.send(embed=discord.Embed(description=f"Cleared warnings for {member.mention}.", color=0x57f287))

async def setup(bot):
    await bot.add_cog(Moderation(bot))
