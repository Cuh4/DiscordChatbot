# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot] Filter
# // ---------------------------------------------------------------------

# // ---- Functions
def filter(data: list):
    # setup
    new = []
    
    # general character filtering
    for _, text in enumerate(data):
        # remove if this value contains a backslash
        if text.find("\\") != -1:
            continue
        
        # remove some common unicode (?, forgot the term) characters
        text = text.encode("ascii", "ignore")
        text = text.decode()
        
        new.append(text)

    # return
    return new