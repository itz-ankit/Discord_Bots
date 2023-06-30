import discord
import random

# Define required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

# Define the game board as a dictionary with snakes and ladders
board = {
    2: 38,
    7: 14,
    8: 31,
    15: 26,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    78: 98,
    87: 94,
}

# Define a dictionary to keep track of player positions
player_positions = {}

# Define a function to print the game board
def print_board():
    board_str = ""
    for i in range(100, 0, -1):
        if i in board.values():
            board_str += "S" if list(board.keys())[list(board.values()).index(i)] > i else "L"
        else:
            board_str += " "
        board_str += str(i) if i != 1 else " 1"
        if i % 10 == 1:
            board_str += "\n"
        else:
            board_str += "|"
    print(board_str)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!snl'):
        # Check if the player is already registered
        if message.author.id in player_positions:
            await message.channel.send('You are already registered for the game.')
            return

        # Add the player to the game
        player_positions[message.author.id] = 1
        await message.channel.send('{0.author.mention} has joined the game!'.format(message))
        print_board()

    elif message.content.startswith('!roll'):
        # Check if the player is registered
        if message.author.id not in player_positions:
            await message.channel.send('You are not registered for the game. Type !snl to join.')
            return

        # Roll the dice and update the player position
        dice_roll = random.randint(1, 6)
        player_positions[message.author.id] += dice_roll

        # Check if the player has landed on a snake or ladder
        if player_positions[message.author.id] in board:
            player_positions[message.author.id] = board[player_positions[message.author.id]]
            if player_positions[message.author.id] > 100:
                player_positions[message.author.id] = 100

        # Check if the player has won the game
        if player_positions[message.author.id] == 100:
            await message.channel.send('{0.author.mention} has won the game!'.format(message))
            del player_positions[message.author.id]
            print_board()
            return

        await message.channel.send('{0.author.mention} rolled a {1} and landed on square {2}.'.format(message, dice_roll, player_positions[message.author.id]))
        print_board()

client.run('YOUR_DISCORD_BOT_TOKEN_HERE')
