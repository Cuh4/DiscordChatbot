# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import chatterbot
from chatterbot import trainers
import discord
import threading
import asyncio

import config
import training
from helpers import discord as discordHelpers
from helpers import general as helpers
import conversationPresets

# // ---- Variables
# // Chatbot
chatbot = chatterbot.ChatBot(
    name = "Bob",
    read_only = True
)

response, completed = "", False

# // Chatbot Training
# Trainers
listTrainer = trainers.ListTrainer(chatbot, show_training_progress = False)
corpusTrainer = trainers.ChatterBotCorpusTrainer(chatbot, show_training_progress = False)

# // Discord Bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(
    intents = intents,
    
    status = discord.Status.do_not_disturb,
    activity = discord.Activity(
        type = discord.ActivityType.watching,
        name = config.activityText
    )
)

# // ---- Functions
def trainFromPreset(name: str, preset: list[list[str]]):
    for index, convo in enumerate(preset):
        training.train(f"{name}.{index}", listTrainer, helpers.filter.filter(convo))
        
async def getChatbotResponse(content: str, callback):
    # getting the chatbot response
    def chatbotResponse():
        global response
        global completed
        
        # default
        response, completed = "", False
    
        # get response
        response, completed = chatbot.get_response(content), True
        
    # do this in a separate thread
    threading.Thread(
        target = chatbotResponse
    ).start()
    
    # delay until response is retrieved/time out
    maxChecks = 10
    checks = 1
    
    while True:
        await asyncio.sleep(config.responseTimeout / maxChecks)
        checks += 1

        # timeout
        if checks > maxChecks:
            break
        
        # not completed yet, so keep waiting
        if completed:
            break
    
    # response was either retrieved, or just timed out
    await callback(response, completed)

# // ---- Main
# // Train Chatbot
training.train("corpus.english", corpusTrainer, "chatterbot.corpus.english")

# source: https://github.com/alexa/Topical-Chat/tree/master/conversations
trainFromPreset("online1", conversationPresets.online1.data)
trainFromPreset("online2", conversationPresets.online2.data)
trainFromPreset("online3", conversationPresets.online3.data)
trainFromPreset("online4", conversationPresets.online4.data)

# source: https://www.kaggle.com/datasets/projjal1/human-conversation-training-data
training.train("online5", listTrainer, helpers.filter.filter(conversationPresets.online5.data))

# // When the bot starts
@client.event
async def on_ready():    
    # notify
    helpers.prettyprint.success(f"{discordHelpers.utils.formattedName(client.user)} has started.")

# // When a message is sent
@client.event
async def on_message(message: discord.Message):
    global processingResponse
    
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
    
    # remove mentions from message content
    content = message.content

    for user in message.mentions:
        content = content.replace(f"<@{user.id}>", "")
    
    # Send loading message
    sentMessage = await message.channel.send(
        embed = discord.Embed(
            description = config.loadingEmoji,
            color = discord.Colour.from_rgb(255, 125, 25)
        ),
        
        reference = message,
        mention_author = True
    )

    helpers.prettyprint.info(f"🧑| Received a message from {discordHelpers.utils.formattedName(message.author)}: {content}")

    # Get chatbot response
    helpers.prettyprint.info(f"💻| Processing.")

    # Send chatbot response once ready
    async def handler(response: str, successful: bool):
        # successful
        if successful:
            helpers.prettyprint.success(f"🤖| Reply to {discordHelpers.utils.formattedName(message.author)}: {response}")

            return await sentMessage.edit( # using return statement to prevent running timeout code below
                embed = discord.Embed(
                    description = f"> :robot: :white_check_mark: | **{response}**",
                    color = discord.Colour.from_rgb(125, 255, 125)
                )
            )
        else:
            # unsuccessful (timed out)
            helpers.prettyprint.error(f"🤖| Reply to {discordHelpers.utils.formattedName(message.author)} timed out.")
        
            return await sentMessage.edit(
                embed = discord.Embed(
                    description = f"> :robot: :x: | **I took too long to respond. Sorry!**",
                    color = discord.Colour.from_rgb(255, 125, 125)
                )
            )
        
    await getChatbotResponse(message.content, handler)
    
# // Start the bot
client.run(config.botToken, log_handler = None)