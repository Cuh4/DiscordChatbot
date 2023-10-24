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
# // Chatbot
chatbot = chatterbot.ChatBot("Bob")

# // Chatbot Training
# Training Data
conversations.training.saveConversation(
    conversation = conversationPresets.online2.data,
    reverse = False
)

# Trainers
listTrainer = trainers.ListTrainer(chatbot)
corpusTrainer = trainers.ChatterBotCorpusTrainer(chatbot)

# // Discord Bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

# // Other vars
userConvos = {}

# // ---- Main
# // Train Chatbot
# conversations.training.train(listTrainer) # detailed
corpusTrainer.train("chatterbot.corpus.english")

# // When the bot starts
@client.event
async def on_ready():
    # notify
    helpers.prettyprint.success(f"{discordHelpers.utils.formattedName(client.user)} has started.")

# // When a message is sent
@client.event
async def on_message(message: discord.Message):
    global userConvos
    
    # Ignore messages sent by bots
    if message.author.bot:
        return
    
    # Ignore message if not mentioned
    if not discordHelpers.utils.isMentioned(message.mentions, client.user):
        return
    
    # Ignore message if user is on cooldown
    if discordHelpers.cooldown.cooldown(message.author, config.chatCooldown, "chat"):
        return await message.add_reaction("🕰")
    
    # Send loading message
    message = await message.channel.send(
        embed = discord.Embed(
            description = f"> **Please wait..**",
            color = discord.Colour.from_rgb(255, 125, 25)
        ),
        
        reference = message,
        mention_author = True
    )
    
    # Save user message
    conversationFromUser: list = userConvos.get(message.author.id, [])
    conversationFromUser.append(message.content)
    
    if len(conversationFromUser) > config.messageHistoryLimit:
        conversationFromUser.pop(0)
    
    # Retrieve chatbot response
    userConvoConcatenated = "\n".join(conversationFromUser)
    response = chatbot.get_response(userConvoConcatenated)
    
    conversationFromUser.append(response)
    userConvos[message.author.id] = conversationFromUser # save

    # Reply with the response
    helpers.prettyprint.info(f"🧑 | Received a message from {discordHelpers.utils.formattedName(message.author)}: {message.content}")
    helpers.prettyprint.success(f"🤖| Reply: {response}")

    await message.edit(
        embed = discord.Embed(
            description = f"> :robot: | **{response}**",
            color = discord.Colour.from_rgb(125, 255, 125)
        )
    )
    
    # Finally, learn from this interaction
    # listTrainer.train(conversationFromUser)
    
# // Start the bot
client.run(config.botToken, log_handler = None)