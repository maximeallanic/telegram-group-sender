from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors.rpc_error_list import PeerFloodError, FloodWaitError

from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import InputChannel, PeerChannel, ChannelParticipantsSearch, InputPeerUser

import time
import random
import sys

class Clients():
    clients = []
    apis = []

    def addApi(self, api_id, api_hash):
        self.apis.append({
            'id': api_id,
            'hash': api_hash
        })

    def addAccount(self, phone):
        for api in self.apis:
            client = Client(phone, api['id'], api['hash'])
            self.clients.append(client)

    def get_client(self):
        while True:
            pos = random.randrange(0, len(self.clients), 1)
            client = self.clients[pos]
            if client.is_available():
                return client

    def send_message(self, id, message):
        client = self.get_client()
        client.send_message(id, message)

    def send_messages(self, id, messages, tempo):
        client = self.get_client()
        try:
            client.send_messages(id, messages, tempo)
        except FloodWaitError:
            print(client.phone, 'is temporary unusable')
            client.disconnect()
            self.send_messages(id, messages, tempo)
        except PeerFloodError:
            print(client.phone, 'is disable')
            client.disconnect()
            self.send_messages(id, messages, tempo)
        except:
            client.disconnect()
            self.send_messages(id, messages, tempo)

class Client():
    def __init__(self, phone, api_id, api_hash):
        self.phone = phone
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

    def send_messages(self, id, messages, tempo):
        self.client.connect()
        for message in messages:
            self.client.send_message(id, message)
            time.sleep(tempo or 0)
        self.client.disconnect()

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def is_available(self):
        return self.available

    def get_entity(self, entity):
        return self.client.get_entity(entity)

    def invoke(self, request):
        return self.client.invoke(request)