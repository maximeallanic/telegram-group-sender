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

class Clients():
    clients = []
    def add(self, client):
        self.clients.append(client)

    def get_client(self):
        while True:
            pos = random.randrange(0, len(self.clients), 1)
            client = self.clients[pos]
            if client.is_available()
                return client

    def send_message(self, id, message):
        client = self.get_client()
        client.send_message(id, message)

    def send_messages(self, id, messages, tempo):
        client = self.get_client()
        for message in messages:
            client.send_message(id, message)
            time.sleep(tempo or 0)



class Client(phone):
    def __init__(self):
        self.available = True
        self.client = TelegramClient(phone, api_id, api_hash)
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(phone)
            self.client.sign_in(phone, input('Enter the code: '))  # Put whatever code you received here.
        self.client.disconnect()
    def send_message(self, id, message):
        try:
            self.client.connect()
            self.client.send_message(id, message)
            self.client.disconnect()
        except FloodWaitError:
            self.available = False
        except PeerFloodError:
            self.available = False
        except:
            self.client.disconnect()
    def is_available(self):
        return self.available

clients = Clients()

while True:
    phone = input('Enter your phone: ')
    if phone.strip() == '':
        break
    else:
        client = Client(phone)
        clients.add(client)


channels = []
client = clients.getClient()
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