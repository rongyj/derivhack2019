# Copyright (c) 2019 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import requests
import uuid

owner = "Alice"
tokenHeader = { "Authorization" : """Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsZWRnZXJJZCI6ImhlbGxvY2RtIiwiYXBwbGljYXRpb25JZCI6ImZvb2JhciIsInBhcnR5IjoiQWxpY2UifQ.SY9x-Eh_mnPJwKzn4UXvHgtDSbFCRWZFqv0HgaGeXNI"""} #TODO: send meta static time
epoch = 0 # millis from epoch
host = "localhost"
port = "7575"
endpoint = "http://{}:{}".format(host, port)
metadataFileName = "../../resources/CDM.json"

def loadCDMFile(fileName):

  """Opens a file containing a CDM JSON instance, and decodes into a Python
     dictionary."""

  with open(fileName) as cdmJsonString:
    return json.load(cdmJsonString)

def convertCDMJsonToDAMLJson(cdmDict):

  """Given a CDM dict, convert it into a dict that can be understood by the
     DAML HTTP REST service"""

  from message_integration.metadata.cdm.cdmMetaDataReader import CdmMetaDataReader
  from message_integration.metadata.damlTypes import Record
  from message_integration.strategies.jsonCdmDecodeStrategy import JsonCdmDecodeStrategy
  from message_integration.strategies.jsonCdmEncodeStrategy import JsonCdmEncodeStrategy

  with open(metadataFileName) as metadataRaw:
    metadata = CdmMetaDataReader().fromJSON(json.load(metadataRaw))
    return JsonCdmDecodeStrategy(metadata).decode(cdmDict, Record("Event"))

def writeDAMLJsonToLedger(damlDict, contractName, signatoryName, httpEndpointPrefix):

  """Given a dict containing a DAML contract, load to the ledger via the HTTP
     REST service. Return resulting HTTP response."""

  return requests.post(
    httpEndpointPrefix + "/command/create",
    headers = tokenHeader,
    json = {
      "templateId" : {
        "moduleName": "Main",
        "entityName": contractName
      },
      "meta" : {
        "ledgerEffectiveTime": epoch # Wall time unsupported on DABL
      },
      "argument": {
        "event": damlDict,
        "owner": signatoryName,
        "obs": signatoryName
      }
    }
  )

def readDAMLJsonFromLedger(contractName, signatoryName, httpEndpointPrefix):

  """Given the contract name, query ledger for all such contracts, returning
     the HTTP response, with a monkey patched `contract` accessor."""

  response = requests.post(
    httpEndpointPrefix + "/contracts/search",
    headers = tokenHeader,
    json = {
      "%templates" : [
        {
          "moduleName" : "Main",
          "entityName" : contractName
        }
      ]
    }
  )

  if response.status_code == 200:
    response.contract = response.json()["result"][0]["argument"]
    response.contractId = response.json()["result"][0]["contractId"]

  return response

def exerciseChoice(contractIdToExerciseOn, choiceName, choiceArguments, httpEndpointPrefix):

  """Exercises 'SayHello' on a CashTransfer contract.
  This sets the `contract.eventIdentifier.assignedIdentifier.identifier.value`
  to the given text, and increments the `version` by one.
  Return the updated contract:
  """

  return requests.post(
    httpEndpointPrefix + "/command/exercise",
    headers = tokenHeader,
    json = {
      "meta" : {
        "ledgerEffectiveTime": epoch # Wall time unsupported on DABL
      },
      "templateId" : {
        "moduleName" : "Main",
        "entityName" : "Transfer",
      },
      "contractId": contractIdToExerciseOn,
      "choice": choiceName,
      "argument": choiceArguments,
    }
  )

if __name__ == '__main__' :
  print("#### Loading CDM JSON from 'CashTransfer.json' ####")
  cdmJson = loadCDMFile("CashTransfer.json")
  cdmJson["meta"]["globalKey"] = str(uuid.uuid4()) # We overwrite the globalKey, to avoid DAML key clashes, allowing us to reload the same contract many times.
  print("Loaded the following JSON object:")
  print(cdmJson)

  print("#### Converting to DAML JSON, wrapping in an 'Transfer' contract ####")
  damlJson = convertCDMJsonToDAMLJson(cdmJson)
  print("Resulting JSON object:")
  print(damlJson)

  print("#### Sending Transfer contract to ledger ####")
  httpCreateResponse = writeDAMLJsonToLedger(damlJson, "Transfer", owner, endpoint)
  print("HTTP service responded: {}".format(httpCreateResponse))

  if httpCreateResponse.status_code == 200:
    print("#### Reading back Transfer contracts from Ledger ####")
    httpContractsResponse = readDAMLJsonFromLedger("Transfer", owner, endpoint)
    print("HTTP service responded: {}".format(httpContractsResponse))

    if httpContractsResponse.status_code == 200:
      print("#### Exercising `SayHello` on the first `CashTransfer` contract ####")
      httpExerciseResponse = exerciseChoice(httpContractsResponse.contractId, "SayHello", { "whomToGreet" : "world!" }, endpoint)
      print("HTTP service responded: {}".format(httpExerciseResponse))
      if httpExerciseResponse.status_code != 200:
        print(httpExerciseResponse.json())

    else:
      print("#### Failed trying to fetch the new contract ###")
      print(httpContractsResponse.json())

  else:
    print("There was a problem creating the contract:")
    print(httpCreateResponse.json())
