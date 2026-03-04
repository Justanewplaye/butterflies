import discord, os, json, asyncio, datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents, help_command=None)

def load_cfg():
    try:
        with open('config.json') as f:
            return json.load(f)
    except:
        return {}

def save_cfg():
    with open('config.json', 'w') as f:
        json.dump(bot.cfg, f)

def gcfg(guild_id):
    gid = str(guild_id)
    bot.cfg.setdefault(gid, {
        'log_channel': None,
        'welcome_channel': None,
        'join_image': None,
        'leave_image': None,
        'booster_roles': {}
    })
    return bot.cfg[gid]

def load_warns():
    try:
        with open('warns.json') as f:
            return json.load(f)
    except:
        return {}

def save_warns():
    with open('warns.json', 'w') as f:
        json.dump(bot.warns, f)

bot.cfg = load_cfg()
bot.afk = {}
bot.snipe = {}
bot.warns = load_warns()
bot.save_cfg = save_cfg
bot.save_warns = save_warns
bot.gcfg = gcfg

@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.utcnow()
    await bot.tree.sync()
    print(f'{bot.user} online')

async def main():
    async with bot:
        for cog in ['cogs.config', 'cogs.moderation', 'cogs.utility', 'cogs.booster', 'cogs.events', 'cogs.fun', 'cogs.social']:
            await bot.load_extension(cog)
        await bot.start(TOKEN)

asyncio.run(main())
