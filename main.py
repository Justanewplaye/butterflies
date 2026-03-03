import discord, os, json, asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

def load_cfg():
    try:
        with open('config.json') as f:
            return json.load(f)
    except:
        return {
            'log_channel': None,
            'welcome_channel': None,
            'join_image': None,
            'leave_image': None,
            'booster_roles': {}
        }

def save_cfg():
    with open('config.json', 'w') as f:
        json.dump(bot.cfg, f)

bot.cfg = load_cfg()
bot.afk = {}
bot.save_cfg = save_cfg

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} online')

async def main():
    async with bot:
        for cog in ['cogs.config', 'cogs.moderation', 'cogs.utility', 'cogs.booster', 'cogs.events']:
            await bot.load_extension(cog)
        await bot.start(TOKEN)

asyncio.run(main())
