# // severely rushed thing to just format these raw json conversation datasets

# // ---- Imports
import json

# // ---- Functions
def handle(file_name: str):
    messages = []
    
    with open(file_name, "r") as file:
        content = file.read()
        data: dict = json.loads(content)
        
        for _, conversation in data.items():
            convo = []

            for talk in conversation.get("content"):
                convo.append(talk["message"])
                
            messages.append(convo)
                                
    with open(file_name.replace(".json", "_new.json"), "w") as f:
        f.write(json.dumps(messages, indent = 6))
        
    return messages

# // ---- Main
handle("test_freq.json")
handle("train.json")