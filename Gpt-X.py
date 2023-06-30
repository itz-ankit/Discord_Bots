import discord
from discord.ext import commands
import openai

openai.api_key = "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"  # Replace with your OpenAI API key

intents = discord.Intents.all()
intents.messages = True  # Enable listening to message events

bot = commands.Bot(command_prefix='Gpt!', intents=intents)

conversation_history = {}

def process_message(message):
    if message.content == 'quit()':
        return True, None

    channel_id = message.channel.id
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []

    conversation_history[channel_id].append({"role": "user", "content": message.content})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}] + conversation_history[channel_id]
    )

    reply = response['choices'][0]['message']['content']
    conversation_history[channel_id].append({"role": "assistant", "content": reply})

    return False, reply

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)  # Retrieve the bot's name from the user attribute
    print('------')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!'):
        # If the message starts with a command prefix, process it as a command
        await bot.process_commands(message)
    elif message.content.startswith('Gpt!'):
        # Otherwise, send the user's message to OpenAI for processing
        should_quit, reply = process_message(message)

        if should_quit:
            await message.channel.send("Chat ended. Goodbye!")
            return

        await message.channel.send(reply)

@bot.command()
async def hello(ctx):
    # Define a custom command using the @bot.command() decorator
    await ctx.send("Hello, I am your chatbot!")

bot.run('MTA5OTYwMjExMzIyODcyMjE3Ng.G3ZnYa.2YDcw5M99Zz27By65JKmmMm54VtSrkgDBrKe0Q')  # Replace with your Discord bot token
