# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot] Training
# // ---------------------------------------------------------------------

# // ---- Imports
from chatterbot import trainers
from . import filter

# // ---- Variables
conversations: list[list[str]] = []

# // ---- Functions
def saveConversation(conversation: list[str], reverse: bool = False):
    global conversations
    
    if reverse:
        conversation.reverse()
    
    conversations.append(conversation)

    return conversation

def train(listTrainer: trainers.ListTrainer):
    for convo in conversations:
        listTrainer.train(filter.filter(convo))