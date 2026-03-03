import discord, random, asyncio, html, requests
from discord.ext import commands

responses = [
    "yes", "no", "maybe", "absolutely not", "definitely",
    "ask again later", "don't count on it", "signs point to yes",
    "outlook not so good", "obviously", "no chance", "for sure"
]

EMPTY = "\u200b"

def check_winner(board):
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] != None:
            return board[r][0]
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] != None:
            return board[0][c]
    if board[0][0] == board[1][1] == board[2][2] != None: return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None: return board[0][2]
    return None

class TTTButton(discord.ui.Button):
    def __init__(self, r, c):
        super().__init__(style=discord.ButtonStyle.secondary, label=EMPTY, row=r)
        self.r = r
        self.c = c

    async def callback(self, interaction: discord.Interaction):
        v = self.view
        if interaction.user.id != v.players[v.turn].id:
            return await interaction.response.send_message("Not your turn.", ephemeral=True)
        mark = "X" if v.turn == 0 else "O"
        v.board[self.r][self.c] = mark
        self.label = mark
        self.style = discord.ButtonStyle.danger if mark == "X" else discord.ButtonStyle.primary
        self.disabled = True
        winner = check_winner(v.board)
        if winner:
            for item in v.children: item.disabled = True
            v.stop()
            return await interaction.response.edit_message(content=f"{v.players[v.turn].mention} wins!", view=v)
        if all(v.board[r][c] for r in range(3) for c in range(3)):
            for item in v.children: item.disabled = True
            v.stop()
            return await interaction.response.edit_message(content="Tie!", view=v)
        v.turn = 1 - v.turn
        mark2 = "X" if v.turn == 0 else "O"
        await interaction.response.edit_message(content=f"{v.players[v.turn].mention}'s turn ({mark2})", view=v)

class TTTView(discord.ui.View):
    def __init__(self, p1, p2):
        super().__init__(timeout=60)
        self.players = [p1, p2]
        self.turn = 0
        self.board = [[None]*3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                self.add_item(TTTButton(r, c))

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

    @commands.hybrid_command()
    async def trivia(self, ctx):
        try:
            data = requests.get("https://opentdb.com/api.php?amount=1&type=multiple").json()['results'][0]
        except:
            return await ctx.send("Couldn't fetch a question, try again.")
        q = html.unescape(data['question'])
        correct = html.unescape(data['correct_answer'])
        answers = [html.unescape(a) for a in data['incorrect_answers']] + [correct]
        random.shuffle(answers)
        letters = ['A', 'B', 'C', 'D']
        correct_letter = letters[answers.index(correct)]
        opts = "\n".join(f"**{letters[i]}** {answers[i]}" for i in range(len(answers)))
        e = discord.Embed(title=q, description=opts, color=0x5865f2)
        e.set_footer(text=f"{data['category']} | {data['difficulty']}")
        await ctx.send(embed=e)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() in letters
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=15)
            if msg.content.upper() == correct_letter:
                await ctx.send(embed=discord.Embed(description=f"Correct! The answer was **{correct}**.", color=0x57f287))
            else:
                await ctx.send(embed=discord.Embed(description=f"Wrong. The answer was **{correct}**.", color=0xed4245))
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(description=f"Time's up. The answer was **{correct}**.", color=0x99aab5))

    @commands.hybrid_command()
    async def tictactoe(self, ctx, member: discord.Member):
        if member == ctx.author:
            return await ctx.send("You can't play against yourself.")
        view = TTTView(ctx.author, member)
        await ctx.send(content=f"{ctx.author.mention}'s turn (X)", view=view)

    @commands.hybrid_command()
    async def color(self, ctx, hex: str):
        try:
            hex = hex.strip('#')
            val = int(hex, 16)
            r, g, b = (val >> 16) & 255, (val >> 8) & 255, val & 255
        except:
            return await ctx.send("Bad hex. Use something like `ff5733`.")
        e = discord.Embed(color=val)
        e.add_field(name="Hex", value=f"#{hex.upper()}")
        e.add_field(name="RGB", value=f"{r}, {g}, {b}")
        await ctx.send(embed=e)

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx, time: str, *, prize: str):
        unit = time[-1]
        if unit not in ('s', 'm', 'h'):
            return await ctx.send("Use s, m, or h. Example: `10m`")
        secs = int(time[:-1]) * {'s': 1, 'm': 60, 'h': 3600}[unit]
        e = discord.Embed(title="🎉 Giveaway", description=f"**{prize}**\nReact with 🎉 to enter!\nEnds in {time}.", color=0xfaa61a)
        e.set_footer(text=f"Hosted by {ctx.author.name}")
        msg = await ctx.send(embed=e)
        await msg.add_reaction("🎉")
        await asyncio.sleep(secs)
        msg = await ctx.channel.fetch_message(msg.id)
        reaction = discord.utils.get(msg.reactions, emoji="🎉")
        users = [u async for u in reaction.users() if not u.bot]
        if not users:
            return await ctx.send(embed=discord.Embed(description="No entries, no winner.", color=0xed4245))
        winner = random.choice(users)
        await ctx.send(embed=discord.Embed(description=f"🎉 {winner.mention} won **{prize}**!", color=0x57f287))

async def setup(bot):
    await bot.add_cog(Fun(bot))
