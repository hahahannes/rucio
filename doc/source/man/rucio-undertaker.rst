Daemon rucio-undertaker
***********************
.. argparse::
   :filename: bin/rucio-undertaker
   :func: get_parser
   :prog: rucio-undertaker

Description
-----------
The Undertaker deamon is responsible for managing expired DIDs. It deletes DIDs, but not replicas by checking if there are DIDs where the 'expired_at' date property is older than the current timestamp.

Example
-------

Create a DID that is already expired by setting its lifetime to -1::

  $ python
  from rucio.db.sqla.constants import DIDType
  from rucio.client.didclient import DIDClient
  client = DIDClient()
  client.add_did(scope='mock', name='test', type=DIDType.DATASET, lifetime=-1)

Check if the DID exists::

  $ rucio list-dids mock:test
  +--------------+--------------+
  | SCOPE:NAME   | [DID TYPE]   |
  |--------------+--------------|
  | mock:test    | DATASET      |
  +--------------+--------------+

Run the daemon::

  $ rucio-undertaker --run-once

Check if the DID exists::

  $ rucio list-dids mock:test
  +--------------+--------------+
  | SCOPE:NAME   | [DID TYPE]   |
  |--------------+--------------|
  +--------------+--------------+
