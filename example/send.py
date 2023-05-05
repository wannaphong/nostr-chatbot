from nostr_chatbot import Chatbot

private_key = b""

recipient_pubkey = "npub..."

chat = Chatbot(private_key=private_key,recipient_pubkey=recipient_pubkey)

while True:
    bot = input("Text : ")
    if bot=="exit":
        chat.close()
        break
    chat.send(bot)
    while True:
        _temp = chat.receive()
        if _temp!=None:
            print("user : "+_temp)
            break