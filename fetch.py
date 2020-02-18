#!/usr/bin/env python3

from http.client import HTTPSConnection
from base64 import b64encode

from config import REPOSITORY_OWNER, REPOSITORY_NAME, ACCESS_TOKEN

headers = {
  'User-Agent': 'https://delta.utu.fi',
  'Authorization': 'token {}'.format(ACCESS_TOKEN),
  'Accept': 'application/vnd.github.everest-preview+json'
}

body = '{"event_type": "CUSTOM_ACTION_NAME_HERE"}'

connection = HTTPSConnection("api.github.com")

uri = "/repos/{}/{}/dispatches".format(REPOSITORY_OWNER, REPOSITORY_NAME)
connection.request('POST', uri, headers=headers, body=body)

response = connection.getresponse()

print("status:", response.status)