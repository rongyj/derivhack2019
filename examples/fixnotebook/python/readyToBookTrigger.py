# Copyright (c) 2019 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# A DAML trigger which automates the client process of listening for execution
# messages at EoD, and aggregating these together into a single block to be
# allocated by the broker, via the 'ReadyToBook' allocType.
#
# Running this process will print out aggregated lines to stdout whenever the
# broker creates new executions.
#
# These can be observed from the notebook in the last cell, "Proposed
# Allocations". The ready to book records will be designated as such under the
# 'allocType' column.

import dazl
from dazl.model.reading import ContractCreateEvent, InitEvent
import pandas as pd
import sys
import asyncio

# This expects ledger name to be "allocs"
clientHeader = { "Authorization" : """Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsZWRnZXJJZCI6ImFsbG9jcyIsImFwcGxpY2F0aW9uSWQiOiJhbGxvY3MiLCJwYXJ0eSI6ImNsaWVudCJ9.ayhBmc7qfT1kjF_1AM7RTTQ4ZXsjM9q1sP-CaMYExPg""" }

def parseArguments(args):
  """
    :param: args argument list.
    :returns: dict with the parsed arguments.
  """
  import argparse
  parser = argparse.ArgumentParser(description = "DAZL Bot")
  parser.add_argument("--host", default = "localhost")
  parser.add_argument("--port", default = "6865")
  return vars(parser.parse_args(args))

network = dazl.Network()
network.set_config(
  url = "http://{host}:{port}".format(**parseArguments(sys.argv[1:]))
)

client = network.aio_party("client")

execs = []

@client.ledger_init()
async def onInit(event: InitEvent):
  global execs
  execs = []

@client.ledger_created("Main.Execution")
async def onCreate(event: ContractCreateEvent):
  global execs
  execs.append(event.cdata["report"])

async def aggregateEveryMinute():

  """ In reality, this would be a method run at the end of the trading
  day to aggregate multiple orders into a single block trade. Here we
  just run it every 3 seconds to poll for new execs.  """

  import time
  from datetime import timedelta
  global execs
  while True:
    if len(execs) > 0:
      print("New executions found, aggregating as:")
      blocks = pd.DataFrame(execs).groupby("tradeDate", as_index = True).agg(
        quantity = ("cumQty", "sum"),
        avgPx = ("avgPx", "max"), # FIXME: weighted average
        ordAllocGrp = ("orderID", lambda ids: ids.to_list())
      )
      execs = []
      print(blocks)
      for (d, b) in blocks.iterrows():
        client.submit_create("Main.ProposeBilateralAllocation",
          { #FIXME  A lot of fields here are hard-coded
            "initiator" : "client",
            "responder" : "broker",
            "instruction" : {
              "allocID" : time.monotonic() * 1e+9,
              "allocTransType" : "New",
              "allocType" : "ReadyToBook" ,
              "refAllocID" : None,
              "allocCancReplaceReason" : None,
              "ordAllocGrp" : [ { "orderID" : i } for i in b["ordAllocGrp"]],
              "side" : "Buy",
              "instrument" : { 
                "symbol" : "BARC",
                "securityID" : "GB0031348658", 
                "securityIDSource" : "ISIN"
              },
              "avgPx" : b["avgPx"],
              "quantity" : b["quantity"],
              "tradeDate" : d.isoformat(), # Dates are represented as ISO strings
              "settlDate" : (d + timedelta(days=2)).isoformat(),
              "allocGrp" : [ {
                "allocAccount" : "Acc123",
                "allocPrice" : b["avgPx"],
                "allocQty" : b["quantity"],
                "parties" : [ 
                  { "partyID" : "client" , "partyIDSource" : "LEI" , "partyRole" : "ClientID" } , 
                  { "partyID" : "broker" , "partyIDSource" : "LEI" , "partyRole" : "ExecutingFirm" }
                ],
                "allocNetMoney" : b["avgPx"] * b["quantity"],
                "allocSettlCurrAmt" : b["avgPx"] * b["quantity"],
                "allocSettlCurr" : "GBX"
              } ]
            }
          }
      )
    await asyncio.sleep(3)

network.run_forever(aggregateEveryMinute())
