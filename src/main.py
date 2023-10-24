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
import conversations
import conversationPresets

# // ---- Variables
# // Create chatbot
chatbot = chatterbot.ChatBot("Bob")

# // Chatbot Training
# Train Data
conversations.training.saveConversation(
    conversation = conversationPresets.online2.data,
    reverse = False
)

# Train the bot
listTrainer = trainers.ListTrainer(chatbot)
# conversations.training.train(listTrainer)

corpusTrainer = trainers.ChatterBotCorpusTrainer(chatbot)
corpusTrainer.train("chatterbot.corpus.english")

# // Create Discord Bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

# // ---- Main
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
    
    # Ignore message if not mentioned
    if not discordHelpers.utils.isMentioned(message.mentions, client.user):
        return
    
    # Ignore message if user is on cooldown
    if discordHelpers.cooldown.cooldown(message.author, config.chatCooldown, "chat"):
        return await message.add_reaction(":clock:")
    
    # Reply with a chatbot response
    response = chatbot.get_response(message.content)

    helpers.prettyprint.info(f"🧑 | Received a message from {discordHelpers.utils.formattedName(message.author)}: {message.content}")
    helpers.prettyprint.success(f"🤖| Reply: {response}")

    return await message.channel.send(
        embed = discord.Embed(
            description = f"> :robot: | {response}",
            color = discord.Colour.from_rgb(125, 255, 125)
        ),
        
        reference = message,
        mention_author = True
    )
    
# // Start the bot
client.run(config.botToken)