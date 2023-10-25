# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot] Training
# // ---------------------------------------------------------------------

# // ---- Imports
import os
import json
import chatterbot
from chatterbot import trainers

# // ---- Variables
fileName = "trained.json"

# // ---- Main
def __createFile():
    if not os.path.exists(fileName):
        with open(fileName, "w") as f:
            f.write(json.dumps({}))
            
def __read() -> dict:
    __createFile()
    
    with open(fileName, "r") as f :
        return json.loads(f.read())
    
def __write(content: dict):
    __createFile()
    
    with open(fileName, "w") as f:
        f.write(json.dumps(
            obj = content,
            indent = 6
        ))

def train(name: str, trainer: trainers.Trainer, *args, **kwargs):
    trainer.train(*args, **kwargs) # train the chatbot
    
    content = __read() # for the future, save somewhere that we trained the chatbot
    content[name] = True
    __write(content)