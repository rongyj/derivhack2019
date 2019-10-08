import csv
import json
import logging
import os
from os.path import dirname, join

import dazl


dazl.setup_default_logger(logging.INFO)
alice = 'Alice'

def main():
    url = os.getenv('DAML_LEDGER_URL')

    partyNameMap = {}
    print("Fetching party map...")
    partyMapPath = join(dirname(__file__), 'partymap.csv')

    with open(partyMapPath) as csvFile:
      readCSV = csv.reader(csvFile, delimiter=',')
      for row in readCSV:
        partyName, party, _ = row
        partyNameMap[partyName] = party
      print("Done fetching party map!")

    party = partyNameMap.get(alice, None)

    print(f'Starting a ledger client for party {party!r} ({alice}) on {url}...')
    network = dazl.Network()
    network.set_config(url=url)
    client = network.aio_party(party)

    @client.ledger_ready()
    def ensure_setup(event):
        '''Once the ledger is ready, create a Sample:Greeter contract as client (Alice)
           in order to be able to greet parties.'''

        return dazl.create('Sample:Greeter', {'party': client.party})

    @client.ledger_created('Sample.HelloMessage') # note: this needs to have a '.' and not a ':'
    def on_message(event):
        '''When a contract of template Sample:HelloMessage is created then
           fetch the Sample:Greeter contract for client (Alice) and execute the SayHello
           choice to reply to the sender with another Sample:HelloMessage'''

        if (event.cdata['recipient'] == client.party) and (event.cdata['sender'] != client.party):
            return dazl.exercise_by_key('Sample.Greeter', client.party, 'SayHello', {
                'to': event.cdata['sender'],
                'message': f'Hello back! Thank you for telling me, \
                    {json.dumps(event.cdata["message"])}'
            })

    network.run_forever()


if __name__ == '__main__':
    main()
