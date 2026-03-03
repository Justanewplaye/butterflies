import discord
from discord import app_commands
from discord.ext import commands

def _get_role(guild, role_id):
    return guild.get_role(int(role_id)) if role_id else None

async def remove_booster_role(guild, uid, bot):
    role = _get_role(guild, bot.cfg['booster_roles'].get(uid))
    if role:
        try: await role.delete()
        except: pass
    bot.cfg['booster_roles'].pop(uid, None)
    bot.save_cfg()

class BoosterGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="br", description="Booster role commands")

    @app_commands.command(name="create", description="Create your booster role")
    async def create(self, interaction: discord.Interaction, name: str, color: str):
        bot = interaction.client
        if not interaction.user.premium_since:
            return await interaction.response.send_message("You need to be boosting.", ephemeral=True)
        uid = str(interaction.user.id)
        if uid in bot.cfg['booster_roles']:
            return await interaction.response.send_message("You already have one. Delete it first with `/br delete`.", ephemeral=True)
        try:
            c = discord.Color(int(color.strip('#'), 16))
        except:
            return await interaction.response.send_message("Bad color, use hex like `ff0000`.", ephemeral=True)
        role = await interaction.guild.create_role(name=name, color=c)
        bot.cfg['booster_roles'][uid] = str(role.id)
        bot.save_cfg()
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"Created {role.mention}.", ephemeral=True)

    @app_commands.command(name="color", description="Change your booster role color")
    async def color(self, interaction: discord.Interaction, color: str):
        bot = interaction.client
        uid = str(interaction.user.id)
        role = _get_role(interaction.guild, bot.cfg['booster_roles'].get(uid))
        if not role:
            return await interaction.response.send_message("You don't have a booster role.", ephemeral=True)
        try:
            c = discord.Color(int(color.strip('#'), 16))
        except:
            return await interaction.response.send_message("Bad color, use hex like `ff0000`.", ephemeral=True)
        await role.edit(color=c)
        await interaction.response.send_message("Color updated.", ephemeral=True)

    @app_commands.command(name="name", description="Rename your booster role")
    async def rename(self, interaction: discord.Interaction, name: str):
        bot = interaction.client
        uid = str(interaction.user.id)
        role = _get_role(interaction.guild, bot.cfg['booster_roles'].get(uid))
        if not role:
            return await interaction.response.send_message("You don't have a booster role.", ephemeral=True)
        await role.edit(name=name)
        await interaction.response.send_message(f"Renamed to **{name}**.", ephemeral=True)

    @app_commands.command(name="give", description="Give your booster role to someone")
    async def give(self, interaction: discord.Interaction, member: discord.Member):
        bot = interaction.client
        uid = str(interaction.user.id)
        role = _get_role(interaction.guild, bot.cfg['booster_roles'].get(uid))
        if not role:
            return await interaction.response.send_message("You don't have a booster role.", ephemeral=True)
        await member.add_roles(role)
        await interaction.response.send_message(f"Gave {role.mention} to {member.mention}.", ephemeral=True)

    @app_commands.command(name="take", description="Take your booster role back from someone")
    async def take(self, interaction: discord.Interaction, member: discord.Member):
        bot = interaction.client
        uid = str(interaction.user.id)
        role = _get_role(interaction.guild, bot.cfg['booster_roles'].get(uid))
        if not role:
            return await interaction.response.send_message("You don't have a booster role.", ephemeral=True)
        await member.remove_roles(role)
        await interaction.response.send_message(f"Took {role.mention} from {member.mention}.", ephemeral=True)

    @app_commands.command(name="delete", description="Delete your booster role so you can make a new one")
    async def delete(self, interaction: discord.Interaction):
        bot = interaction.client
        uid = str(interaction.user.id)
        if uid not in bot.cfg['booster_roles']:
            return await interaction.response.send_message("You don't have a booster role.", ephemeral=True)
        await remove_booster_role(interaction.guild, uid, bot)
        await interaction.response.send_message("Deleted. You can create a new one.", ephemeral=True)

async def setup(bot):
    bot.tree.add_command(BoosterGroup())
