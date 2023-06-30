import random
import os
import discord
from discord.ext import commands

# Define the game constants
WIDTH = 10
HEIGHT = 10
DRAGON =  "\u2654"
TREASURE = "T"
OBSTACLE = "X"
EMPTY = " "
WINNING_SCORE = 5



intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def start_game(ctx):
    
    # Initialize the game state
    game_map = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
    dragon_x = random.randint(0, WIDTH - 1)
    dragon_y = random.randint(0, HEIGHT - 1)
    treasure_x = random.randint(0, WIDTH - 1)
    treasure_y = random.randint(0, HEIGHT - 1)
    obstacle_x = random.randint(0, WIDTH - 1)
    obstacle_y = random.randint(0, HEIGHT - 1)
    score = 0
    
    # Main game loop
    while True:
        # Draw the game map
        game_board = ""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if x == dragon_x and y == dragon_y:
                    game_board += DRAGON + " "
                elif x == treasure_x and y == treasure_y:
                    game_board += TREASURE + " "
                elif x == obstacle_x and y == obstacle_y:
                    game_board += OBSTACLE + " "
                else:
                    game_board += EMPTY + " "
            game_board += "\n"
        game_board += "Score: " + str(score)

        await ctx.send("```\n" + game_board + "```")

        # Get player input
        def check(msg):
            return msg.author == ctx.author and msg.content.lower() in ["w", "a", "s", "d"]

        try:
            move_msg = await bot.wait_for("message", check=check, timeout=30)
        except TimeoutError:
            await ctx.send("Game timed out.")
            return

        move = move_msg.content.lower()

        # Update game state based on player input
        os.system('cls')
        if move == "w" and dragon_y > 0:
            dragon_y -= 1
        elif move == "a" and dragon_x > 0:
            dragon_x -= 1
        elif move == "s" and dragon_y < HEIGHT - 1:
            dragon_y += 1
        elif move == "d" and dragon_x < WIDTH - 1:
            dragon_x += 1

        # Check for collision with treasure
        if dragon_x == treasure_x and dragon_y == treasure_y:
            score += 1
            await ctx.send("You found treasure!")
            treasure_x, treasure_y = get_random_position()

        # Check for collision with obstacle
        if dragon_x == obstacle_x and dragon_y == obstacle_y:
            score -= 1
            await ctx.send("You ran into an obstacle!")
            obstacle_x, obstacle_y = get_random_position()


        # Check for winning condition
        if score >= WINNING_SCORE:
            await ctx.send("Congratulations, you won!")
            break
        
        def get_random_position():
            return random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)

bot.run("MTExNzg1OTUxMzI4Mjg2NzI1MQ.GNpN27.8lPAkP0qb8hZzfl07hbKW2Wmpd3_Z9yEtUlzUk")
