Daemon rucio-hermes
*******************
.. argparse::
   :filename: bin/rucio-hermes
   :func: get_parser
   :prog: rucio-hermes

Description
-----------
The Hermes daemon is responsible for delivering messages via STOMP to a messagebroker and via SMTP as email.

Example
-------
Create a message::

  $ python
  from rucio.core.message import add_message
  add_message(event_type='NEW_DID', payload='There is a new DID')

Run the daemon::

  $ rucio-hermes --run-once
