import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.author.id in self.bot.afk:
            del self.bot.afk[message.author.id]
            await message.channel.send(embed=discord.Embed(description=f"Welcome back {message.author.mention}.", color=0x57f287))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            self.bot.snipe[message.channel.id] = message
        cfg = self.bot.gcfg(message.guild.id)
        if not cfg['log_channel'] or message.author.bot: return
        ch = self.bot.get_channel(cfg['log_channel'])
        if not ch: return
        e = discord.Embed(title="Message Deleted", color=0xed4245)
        e.add_field(name="User", value=message.author.mention)
        e.add_field(name="Content", value=message.content or "No text")
        await ch.send(embed=e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        cfg = self.bot.gcfg(before.guild.id)
        if not cfg['log_channel'] or before.author.bot: return
        if before.content == after.content: return
        ch = self.bot.get_channel(cfg['log_channel'])
        if not ch: return
        e = discord.Embed(title="Message Edited", color=0xfaa61a)
        e.add_field(name="User", value=before.author.mention)
        e.add_field(name="Channel", value=before.channel.mention)
        e.add_field(name="Before", value=before.content or "No text", inline=False)
        e.add_field(name="After", value=after.content or "No text", inline=False)
        await ch.send(embed=e)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        cfg = self.bot.gcfg(member.guild.id)
        if not cfg['log_channel']: return
        ch = self.bot.get_channel(cfg['log_channel'])
        if not ch: return
        if before.channel is None and after.channel:
            await ch.send(embed=discord.Embed(description=f"{member.mention} joined **{after.channel.name}**", color=0x57f287))
        elif before.channel and after.channel is None:
            await ch.send(embed=discord.Embed(description=f"{member.mention} left **{before.channel.name}**", color=0xed4245))
        elif before.channel != after.channel:
            await ch.send(embed=discord.Embed(description=f"{member.mention} moved from **{before.channel.name}** to **{after.channel.name}**", color=0xfaa61a))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cfg = self.bot.gcfg(member.guild.id)
        if cfg['log_channel']:
            ch = self.bot.get_channel(cfg['log_channel'])
            if ch:
                await ch.send(embed=discord.Embed(description=f"{member.mention} joined.", color=0x57f287))
        if cfg['welcome_channel']:
            ch = self.bot.get_channel(cfg['welcome_channel'])
            if ch:
                e = discord.Embed(description=f"Welcome {member.mention}!", color=0x5865f2)
                if cfg['join_image']: e.set_image(url=cfg['join_image'])
                await ch.send(embed=e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        cfg = self.bot.gcfg(member.guild.id)
        uid = str(member.id)
        if uid in cfg['booster_roles']:
            role_id = cfg['booster_roles'].get(uid)
            role = member.guild.get_role(int(role_id)) if role_id else None
            if role:
                try: await role.delete()
                except: pass
            cfg['booster_roles'].pop(uid, None)
            self.bot.save_cfg()
        if cfg['log_channel']:
            ch = self.bot.get_channel(cfg['log_channel'])
            if ch:
                await ch.send(embed=discord.Embed(description=f"{member.name} left.", color=0xed4245))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since and not after.premium_since:
            cfg = self.bot.gcfg(after.guild.id)
            uid = str(after.id)
            if uid in cfg['booster_roles']:
                role_id = cfg['booster_roles'].get(uid)
                role = after.guild.get_role(int(role_id)) if role_id else None
                if role:
                    try: await role.delete()
                    except: pass
                cfg['booster_roles'].pop(uid, None)
                self.bot.save_cfg()

async def setup(bot):
    await bot.add_cog(Events(bot))
