#!/usr/bin/env python3

from http.client import HTTPSConnection
import time
import json
import urllib.request
from zipfile import ZipFile

from config import REPOSITORY_OWNER, REPOSITORY_NAME, WORKFLOW_NAME, ACCESS_TOKEN, EXTRACT_DIRECTORY

MAX_ATTEMPTS = 10
TIMEOUT = 60 # 1 minute

def send_repository_dispatch(headers, buildtime):
  connection = HTTPSConnection("api.github.com")
  body = '{"event_type": "repository_dispatch", "client_payload": { "buildtime": "' + buildtime + '" }}'

  uri = "/repos/{}/{}/dispatches".format(REPOSITORY_OWNER, REPOSITORY_NAME)
  connection.request("POST", uri, headers=headers, body=body)


def get_artifacts_url(headers):
  connection = HTTPSConnection("api.github.com")
  uri = "/repos/{}/{}/actions/workflows/{}/runs".format(REPOSITORY_OWNER, REPOSITORY_NAME, WORKFLOW_NAME)
  connection.request("GET", uri, headers=headers)

  response = connection.getresponse()

  result = json.loads(response.read().decode('utf-8'))
  artifacts_url = result['workflow_runs'][0]['artifacts_url']

  return artifacts_url


def get_latest_artifact(headers, url):
  connection = HTTPSConnection("api.github.com")
  connection.request("GET", url, headers=headers)

  response = connection.getresponse()

  artifacts = json.loads(response.read().decode('utf-8'))['artifacts']

  if not artifacts:
    return {
      "name": "no-artifact"
    }
  
  return artifacts[0]

def download_artifact(headers, url, filename):
  opener = urllib.request.build_opener()
  opener.addheaders = list(headers.items())
  urllib.request.install_opener(opener)
  urllib.request.urlretrieve(url, filename)


if __name__ == "__main__":
  HEADERS = {
    "User-Agent": "https://delta.utu.fi",
    "Authorization": "token " + ACCESS_TOKEN,
    "Accept": "application/vnd.github.everest-preview+json"
  }
  BUILDTIME = str(int(time.time())) # unix timestamp as a string

  send_repository_dispatch(HEADERS, BUILDTIME)
  artifact = None

  for attempt in range(MAX_ATTEMPTS):
    time.sleep(TIMEOUT)
    print("Attempting to fetch artifact, attempt number #" + str(attempt))
    artifacts_url = get_artifacts_url(HEADERS)
    artifact = get_latest_artifact(HEADERS, artifacts_url)
    name = artifact["name"]
    
    if name == "out-" + BUILDTIME:
      print("Found correct artifact, downloading now")
      break

    print("Found incorrect artifact {}, expected out-{}".format(name, BUILDTIME))
  else:
    raise "Build pipeline did not release correct artifact!"

  FILENAME = "out-{}.zip".format(BUILDTIME)
  download_artifact(HEADERS, artifact['archive_download_url'], FILENAME)

  with ZipFile(FILENAME, "r") as f:
    f.extractall(EXTRACT_DIRECTORY)