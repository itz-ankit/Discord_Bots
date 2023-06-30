import discord
from discord.ext import commands
import openai

openai.api_key = "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"  # Replace with your OpenAI API key

intents = discord.Intents.all()
intents.messages = True  # Enable listening to message events

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)  # Retrieve the bot's name from the user attribute
    print('------')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == 'quit()':
        await bot.close()  # Use bot.close() to stop the bot
        return

    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        # If the message starts with a command prefix, process it as a command
        await bot.process_commands(message)
    if message.content.startswith('Gpt!'):
        # Otherwise, send the user's message to OpenAI for processing
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.content}]
        )

        # Retrieve the reply from OpenAI response using a different approach
        reply = response['choices'][0]['message']['content']
        
        await message.channel.send(reply)

@bot.command()
async def hello(ctx):
    # Define a custom command using the @bot.command() decorator
    await ctx.send("Hello, I am your chatbot!")

bot.run('MTA5OTYwMjExMzIyODcyMjE3Ng.G3ZnYa.2YDcw5M99Zz27By65JKmmMm54VtSrkgDBrKe0Q')  # Replace with your Discord bot token
