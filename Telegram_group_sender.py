from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import InputChannel, PeerChannel, ChannelParticipantsSearch, InputPeerUser
import time
import random
import sys

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 119353
api_hash = '70dd4c13d170a21233675e04f07a5fc3'

clients = []

def getClient():
    pos = random.randrange(0, len(clients), 1)
    client = clients[pos]
    client.connect()
    return client

while True:
    phone = input('Enter your phone: ')
    if phone.strip() == '':
        break
    else:
        try:
            client = TelegramClient(phone, api_id, api_hash)
            client.connect()
            if not client.is_user_authorized():
                client.send_code_request(phone)
                client.sign_in(phone, input('Enter the code: '))  # Put whatever code you received here.
            client.disconnect()
            clients.append(client)
        except:
            break


channels = []
client = getClient()
while True:
    group = input('Enter group name: ')
    if group.strip() == '':
        break
    else:
        channels.append(client.get_entity(group))

offset = 0
limit = 100
all_participants = []

for channel in channels:
    while True:
        participants = client.invoke(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(''), offset, limit, hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
        # sleep(1)  # This line seems to be optional, no guarantees
all_participants = list(set(all_participants))
print('Number of participants:', len(all_participants))

messages = []
while True:
    message = input('Enter your message: ')
    if message.strip() == '':
        break
    else:
        messages.append(message)
client.disconnect()

def sendMessage(userId, message):
    client = getClient()
    try:
        client.send_message(userId, message)
        client.disconnect()
    except:
        print('Error with', sys.exc_info()[0])
        client.disconnect()
        sendMessage(userId, message)

for participant in all_participants:
    for message in messages:
        sendMessage(participant.id, message)
        time.sleep(20)

#toChannel = client.get_entity(input('Enter group name to add members: '))

#for participant in all_participants:
#    client(AddChatUserRequest(
#        toChannel,
#        participant.id,
#        fwd_limit=10  # allow the user to see the 10 last messages
#    ))