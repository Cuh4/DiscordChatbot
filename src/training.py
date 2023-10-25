# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot] Training
# // ---------------------------------------------------------------------

# // ---- Imports
import os
import json
from chatterbot import trainers

from helpers import general as helpers

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

def train(name: str, trainer: trainers.Trainer, *args, trainRegardless: bool = False, **kwargs):
    # get data
    content = __read()
    
    # check if chatbot has already been trained
    if content.get(name, None) == True and not trainRegardless:
        return helpers.prettyprint.warn(f"The chatbot has already trained {name}.")
    
    # train the chatbot
    helpers.prettyprint.info(f"🔽| Training {name}.")
    trainer.train(*args, **kwargs) # train the chatbot
    helpers.prettyprint.success(f"✅| Trained {name}.")
    
    # for the future, save that we trained the chatbot
    content[name] = True
    __write(content)