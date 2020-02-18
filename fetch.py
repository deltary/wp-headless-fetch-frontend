#!/usr/bin/env python3

from http.client import HTTPSConnection
from base64 import b64encode

from config import REPOSITORY_OWNER, REPOSITORY_NAME, USERNAME, ACCESS_TOKEN

auth = "{}:{}".format(USERNAME, ACCESS_TOKEN).encode()
authEncoded = b64encode(auth).decode("ascii")
headers = { "User-Agent": "https://delta.utu.fi", "Auhorization": "Basic {}".format(auth) }
print(authEncoded)
body = '"event_type": "release"'

connection = HTTPSConnection("api.github.com")

connection.request('POST', "/repos/{}/{}/dispatches".format(REPOSITORY_OWNER, REPOSITORY_NAME), headers=headers, body=body)

response = connection.getresponse()

print("status:", response.status, response.read())