# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot] Discord Embeds
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

# // ---- Functions
def __setup(emoji: str, title: str, msg: str):
    return f"{emoji} | **{title}**\n> {msg}"

def success(msg: str):
    embed = discord.Embed(
        description = __setup(":white_check_mark:", "Success", msg), 
        color = discord.Colour.from_rgb(0, 255, 0)
    )

    return embed

def failure(msg: str):
    embed = discord.Embed(
        description = __setup(":x:", "Failure", msg), 
        color = discord.Colour.from_rgb(255, 0, 0)
    )

    return embed

def warning(msg: str):
    embed = discord.Embed(
        description = __setup(":warning:", "Warning", msg), 
        color = discord.Colour.from_rgb(255, 125, 0)
    )

    return embed