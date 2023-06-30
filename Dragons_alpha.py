import random
import os
import discord
from discord.ext import commands

# Define the game constants
WIDTH = 15
HEIGHT = 15
DRAGON = "\u2654"
TREASURE = "T"
OBSTACLE = "X"
EMPTY = " "
WINNING_SCORE = 5
NUM_OBSTACLES = 6

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
    score = 0
    dragon_x, dragon_y, treasure_x, treasure_y, obstacles = initialize_game_state()

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
                elif (x, y) in obstacles:
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
            obstacles = generate_obstacles(dragon_x, dragon_y, treasure_x, treasure_y) 

        # Check for collision with obstacle
        if (dragon_x, dragon_y) in obstacles:
            score -= 1
            await ctx.send("You ran into an obstacle!")

        # Check for winning condition
        if score >= WINNING_SCORE:
            await ctx.send("Congratulations, you won!")
            break

def initialize_game_state():
    dragon_x, dragon_y = get_random_position()
    treasure_x, treasure_y = get_random_position()
    obstacles = generate_obstacles(dragon_x, dragon_y, treasure_x, treasure_y)

    return dragon_x, dragon_y, treasure_x, treasure_y, obstacles


def get_random_position():
    return random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)

def generate_obstacles(dragon_x, dragon_y, treasure_x, treasure_y):
    obstacles = []
    while len(obstacles) < NUM_OBSTACLES:
        obstacle_x, obstacle_y = get_random_position()
        if (obstacle_x, obstacle_y) not in obstacles and (obstacle_x != dragon_x or obstacle_y != dragon_y) and (obstacle_x != treasure_x or obstacle_y != treasure_y):
            obstacles.append((obstacle_x, obstacle_y))
    
    return obstacles


bot.run("MTExNzg1OTUxMzI4Mjg2NzI1MQ.GNpN27.8lPAkP0qb8hZzfl07hbKW2Wmpd3_Z9yEtUlzUk")

