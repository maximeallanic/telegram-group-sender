from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import InputChannel, PeerChannel, ChannelParticipantsSearch

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 161336
api_hash = '09f059989761a635cf317636d019fedd'
phone = input('Enter Phone number: ')

client = TelegramClient('session_name', api_id, api_hash)
client.connect()

# If you already have a previous 'session_name.session' file, skip this.
# client.sign_in(phone=phone)
if not client.is_user_authorized():
    client.send_code_request(phone)
    me = client.sign_in(phone, input('Enter the code: '))  # Put whatever code you received here.

channel = client.get_entity(input('Enter group name: '))
offset = 0
limit = 100
all_participants = []

while True:
    participants = client.invoke(GetParticipantsRequest(
        channel, ChannelParticipantsSearch(''), offset, limit, hash=0
    ))
    if not participants.users:
        break
    all_participants.extend(participants.users)
    offset += len(participants.users)
    # sleep(1)  # This line seems to be optional, no guarantees!

message = input('Enter your message: ')

for participant in all_participants:
    if participant.id:
        client.send_message(participant.id, message)