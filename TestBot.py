import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)
slash = SlashCommand(bot, sync_commands=True)  # Initialize SlashCommand with bot and sync_commands=True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
@bot.event
async def on_message(message):
    await bot.process_commands(message)

@slash.slash(
    name="ping",
    description="Check bot's ping"
)
async def ping(ctx: SlashContext):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)} ms')

@slash.slash(
    name="hello",
    description="Say hello to the bot"
)
async def hello(ctx: SlashContext):
    await ctx.send(f'Hello {ctx.author.name}!')

# Slash command error handling
@bot.event
async def on_slash_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Command not found.")
    else:
        await ctx.send(f"An error occurred: {error}")

bot.run("YOUR_BOT_TOKEN")

