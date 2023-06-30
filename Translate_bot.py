import discord
from discord.ext import commands
from googletrans import Translator

# Initialize the Discord bot and the translator
bot = commands.Bot(command_prefix='!')
translator = Translator(service_urls=['translate.google.com'])

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name} ({bot.user.id})')

# Command for translation
@bot.command()
async def translate(ctx, source_lang, target_lang, *, text):
    translation = translator.translate(text, src=source_lang, dest=target_lang)
    translated_text = translation.text
    await ctx.send(f"**Translated Text ({target_lang}):** {translated_text}")

# Run the bot
bot.run('YOUR_BOT_TOKEN')
