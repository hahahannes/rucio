Daemon rucio-conveyor-submitter
*******************************
.. argparse::
   :filename: bin/rucio-conveyor-submitter
   :func: get_parser
   :prog: rucio-conveyor-submitter

Description
-----------
The Conveyor-Submitter is responsible for managing non-tape file transfers.

Example
-------
Upload a file and create a replication rule::

  $ rucio upload --scope mock --rse MOCK --name file filename.txt
  $ rucio add-rule mock:file 1 MOCK2
  $ rucio-admin rse add-distance MOCK2 MOCK

The rule should replicate the file from RSE MOCK to RSE MOCK2. Therefor a distance between these RSEs is needed.

Run the daemon::

  $ rucio-conveyor-submitter --run-once

Check if the file got replicated::

  $ rucio list-file-replicas mock:file
