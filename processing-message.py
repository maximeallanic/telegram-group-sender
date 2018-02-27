#!/usr/bin/env python3
'''
Copyright 2018 Redkeet ISC License
For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
Created by Maxime Allanic <maxime.allanic@redkeet.com> at 27/02/2018
'''

import json
import client

clients = client.Clients()

data_file_path = 'data.json'

# Get telegram account
with open(data_file_path, 'r', encoding="utf8") as data_file:
    data = json.load(data_file)

for phone, api in data['phones'].items():
    clients.add_account(phone, api['id'], api['hash'])

for group, messages in data['messages'].items():
    clients.send_messages(group, messages, 2)
    del data['messages'][group]

with open(data_file_path, 'w', encoding="utf8") as data_file:
    json.dump(data, data_file)