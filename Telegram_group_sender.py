from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

import client


# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
#api_id = 119353
#api_hash = '70dd4c13d170a21233675e04f07a5fc3'


clients = client.Clients()

# Get api key
while True:
    api_id = input('Enter your Api Id: ')
    if api_id.strip() == '':
        break
    else:
        api_hash = input('Enter your Api Hash: ')
        clients.addApi(api_id, api_hash)

# Get telegram account
while True:
    phone = input('Enter your phone: ')
    if phone.strip() == '':
        break
    else:
        clients.addAccount(phone)


# Get channels
channels = []
client = clients.get_client()
client.connect()
while True:
    channel = input('Enter channel name: ')
    if channel.strip() == '':
        break
    else:
        channels.append(client.get_entity(channel))

offset = 0
limit = 200
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

# Reduce list of participant (remove double)
# all_participants = list(set(all_participants))

print('Number of participants:', len(all_participants))

# get messages
messages = []
while True:
    message = input('Enter your message: ')
    if message.strip() == '':
        break
    else:
        messages.append(message)
client.disconnect()

# Send whole messages to all participants
for index, participant in enumerate(all_participants):
    print('Send messages to', participant.username or participant.id, 'there are', len(all_participants) - index, 'participants left')
    clients.send_messages(participant, messages, 20)
