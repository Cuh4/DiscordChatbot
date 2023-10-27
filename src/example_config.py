# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot] Config
# // ---------------------------------------------------------------------

botToken = "" # token of your discord bot. create a bot here: https://discord.com/developers/applications'
chatCooldown = 4 # cooldown given to each user. if a user tries to talk to the bot twice in {chatCooldown} seconds, the query will not be processed
activityText = "you." # in discord, this becomes: "Watching you."
responseTimeout = 10 # in seconds. if the bot takes over {responseTimeout} seconds to respond, the response will be cancelled
loadingEmoji = "<a:loading:1167333599213789224>" # emoji to use for loading response message. use "\:(emoji name):" in a discord channel to get an emoji's id

# [!!] Rename to config.py [!!]