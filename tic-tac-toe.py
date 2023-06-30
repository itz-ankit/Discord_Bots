import discord
from discord.ext import commands

# Define required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

# Game Constants
EMPTY = ' '
PLAYER1 = 'X'
PLAYER2 = 'O'

# Game Board
board = [EMPTY, EMPTY, EMPTY,
         EMPTY, EMPTY, EMPTY,
         EMPTY, EMPTY, EMPTY]

# Discord bot setup
bot = commands.Bot(command_prefix='$', intents=intents)

# Global Variables
current_player = PLAYER1

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.command()
async def play(ctx, position: int):
    if ctx.author == bot.user:
        return

    if not is_valid_move(position):
        await ctx.send("Invalid move! Please choose a number between 1 and 9.")
        return

    make_move(position, current_player)

    if check_winner(current_player):
        await display_board(ctx)
        await ctx.send(f"Player {current_player} wins!")
        reset_board()
        return

    if is_board_full():
        await ctx.send("It's a draw!")
        reset_board()
        return

    await display_board(ctx)
    switch_player()

def is_valid_move(position):
    return position in range(1, 10) and board[position - 1] == EMPTY

def is_board_full():
    if all(cell != EMPTY for cell in board):
        reset_board()
        return True
    return False

def make_move(position, player):
    board[position - 1] = player

def check_winner(player):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] == player:
            return True

    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == player:
            return True

    # Check diagonals
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True

    return False

def reset_board():
    global board
    board = [EMPTY] * 9

async def display_board(ctx):
    lines = ['```']
    for i in range(0, 9, 3):
        row = ' | '.join(board[i:i + 3])
        lines.append(row)
        lines.append('-' * 9)
    lines.pop()
    lines.append('```')
    board_str = '\n'.join(lines)
    await ctx.send(board_str)

def switch_player():
    global current_player
    current_player = PLAYER2 if current_player == PLAYER1 else PLAYER1

# Replace 'YOUR_TOKEN' with your Discord bot token
bot.run('MTA5ODg4MTQ4Mjk5NjU4MDM4Mg.GevNj2.vjIIn0-WQmuCwqzzLcBVdl-lC04qFoFsQHj9Uk')
