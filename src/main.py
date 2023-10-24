# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import chatterbot
from chatterbot import trainers
import discord

import config
from helpers import discord as discordHelpers
from helpers import general as helpers
import conversationPresets

# // ---- Variables
# // Chatbot
chatbot = chatterbot.ChatBot("Bob")

# // Chatbot Training
# Trainers
listTrainer = trainers.ListTrainer(chatbot)
corpusTrainer = trainers.ChatterBotCorpusTrainer(chatbot)

# // Discord Bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

# // ---- Functions
def trainFromPreset(preset: list[list[str]]):
    for convo in preset:
        listTrainer.train(convo)

# // ---- Main
# // Train Chatbot
corpusTrainer.train("chatterbot.corpus.english")

trainFromPreset(conversationPresets.online1.data)
trainFromPreset(conversationPresets.online2.data)

# // When the bot starts
@client.event
async def on_ready():
    # notify
    helpers.prettyprint.success(f"{discordHelpers.utils.formattedName(client.user)} has started.")

# // When a message is sent
@client.event
async def on_message(message: discord.Message):
    # Ignore messages sent by bots
    if message.author.bot:
        return

    # ignore self
    if message.author == client.user:
        return
    
    # Ignore message if not mentioned
    if not discordHelpers.utils.isMentioned(message.mentions, client.user):
        return
    
    # Ignore message if user is on cooldown
    if discordHelpers.cooldown.cooldown(message.author, config.chatCooldown, "chat"):
        return await message.add_reaction("🕰")
    
    # Send loading message
    sentMessage = await message.channel.send(
        embed = discord.Embed(
            description = f":clock:",
            color = discord.Colour.from_rgb(255, 125, 25)
        ),
        
        reference = message,
        mention_author = True
    )

    # Retrieve chatbot response
    response = chatbot.get_response(message.content)
    
    # Reply with the response
    helpers.prettyprint.info(f"🧑 | Received a message from {discordHelpers.utils.formattedName(message.author)}: {message.content}")
    helpers.prettyprint.success(f"🤖| Reply: {response}")

    await sentMessage.edit(
        embed = discord.Embed(
            description = f"> :robot: | **{response}**",
            color = discord.Colour.from_rgb(125, 255, 125)
        )
    )
    
# // Start the bot
client.run(config.botToken, log_handler = None)