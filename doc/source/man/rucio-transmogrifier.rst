Daemon rucio-transmogrifier
***************************
.. argparse::
   :filename: bin/rucio-transmogrifier
   :func: get_parser
   :prog: rucio-transmogrifier

Description
-----------
The Transmogrifier daemon is responsible for the creation of replication rules for DIDs matching a subscription.

Example
-------
Create a DID::

  $ python
  from rucio.core.did import add_did
  from rucio.db.sqla.constants import DIDType
  add_did(scope='mock', name='test', type=DIDType.DATASET, account='root', meta={'project': 'test_project'})

Create a subscription that matches the DID::

  $ rucio-admin subscription add test '{"scope": ["mock"], "project": ["test_project"]}' '[{"copies": 1, "rse_expression": "MOCK", "activity": "User Subscriptions"}]' 'df'

Check if there are rules for the DID::

  $ rucio list-rules mock:test
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  ---------------  -------------------

Run the daemon::

  $ rucio-transmogrifier --run-once

Check again if there are rules for the DID::

  $ rucio list-rules mock:test
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  ---------------  -------------------
  e658f6f47f444326aad624dabef7b785  root       mock:test     OK[0/0/0]               MOCK                     1                   2018-12-03 14:01:19
