#!/usr/bin/env python3
'''
Copyright 2018 Redkeet ISC License
For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
Created by Maxime Allanic <maxime.allanic@redkeet.com> at 27/02/2018
'''

from telethon import TelegramClient
import json
import sys
import os
from client import Client

data_file_path = 'data.json'
if len(sys.argv) > 1:
    data_file_path = sys.argv[1]



# Read database
try:
    with open(data_file_path, 'r', encoding="utf8") as data_file:
        data = json.load(data_file)
except:
    data = {
        'phones': {}
    }

# Initialize form
phone = input('Enter your phone: ')
api_id = input('Enter your Api Id: ')
api_hash = input('Enter your Api Hash: ')

# Connect in telegram to prefill login
Client(phone, api_id, api_hash)


# Enter it in database
data['phones'][phone] = {
    'id': api_id,
    'hash': api_hash
}

# Save database
with open(data_file_path, 'w', encoding="utf8") as data_file:
    json.dump(data, data_file)