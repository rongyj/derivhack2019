# Copyright (c) 2019 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import dazl
from dazl.model.reading import ContractCreateEvent, InitEvent
import sys

tokenHeader = { "Authorization" : """Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsZWRnZXJJZCI6ImhlbGxvY2RtIiwiYXBwbGljYXRpb25JZCI6ImZvb2JhciIsInBhcnR5IjoiQWxpY2UifQ.SY9x-Eh_mnPJwKzn4UXvHgtDSbFCRWZFqv0HgaGeXNI"""} #TODO: send meta static time

host = "localhost"
port = "6865" #Note DAZL talks directly to the Ledger; NOT the HTTP adapter.
network = dazl.Network()
network.set_config(
  url = "http://{}:{}".format(host,port)
)
user = network.aio_party("Alice")

@user.ledger_init()
async def onInit(event: InitEvent):
  print("Ready & listening for new `Transfer` contracts ... ")

@user.ledger_created("Main.Transfer")
async def onCreate(event: ContractCreateEvent):
  allContracts = user.find(template = "Main.Transfer")
  for contract in allContracts:
    print(contract.cdata["event"]["eventIdentifier"][0]["assignedIdentifier"][0]["identifier"]["value"])
    if contract.cdata["event"]["eventIdentifier"][0]["assignedIdentifier"][0]["identifier"]["value"] == "Hello, CDM!":
      print("I have already greeted contract #{}, ignoring.".format(contract.cid))
    else:
      print("Greeting (exercising choice) on contract # {}".format(contract.cid))
      user.submit_exercise(contract.cid, "SayHello", { "whomToGreet" : "CDM"})

network.run_forever()
