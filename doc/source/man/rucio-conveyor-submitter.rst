Daemon rucio-conveyor-submitter
*******************************
.. argparse::
   :filename: bin/rucio-conveyor-submitter
   :func: get_parser
   :prog: rucio-conveyor-submitter

Description
-----------
The Conveyor-Submitter daemon is responsible for managing non-tape file transfers.

Example
-------
Upload a file and create a replication rule::

  $ rucio upload --scope mock --rse MOCK --name file filename.txt
  $ rucio add-rule mock:file 1 MOCK2
  $ rucio-admin rse add-distance MOCK2 MOCK --distance 1 --ranking 1

The rule should replicate the file from RSE MOCK to RSE MOCK2. Therefor a distance between these RSEs is needed.

Check existing replicas of the file::

  $ rucio list-file-replicas mock:file
  +---------+--------+------------+-----------+---------------------------------------------------------+
  | SCOPE   | NAME   | FILESIZE   |   ADLER32 | RSE: REPLICA                                            |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 149.000 B  |    948240 | MOCK: file://localhost:0/tmp/rucio_rse/mock/fb/d1/file  |
  +---------+--------+------------+-----------+---------------------------------------------------------+

Run the daemon::

  $ rucio-conveyor-submitter --run-once

Check if the file got replicated::

  $ rucio list-file-replicas mock:file
  +---------+--------+------------+-----------+---------------------------------------------------------+
  | SCOPE   | NAME   | FILESIZE   |   ADLER32 | RSE: REPLICA                                            |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 149.000 B  |    948240 | MOCK: file://localhost:0/tmp/rucio_rse/mock/fb/d1/file  |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 149.000 B  |    948240 | MOCK2: file://localhost:0/tmp/rucio_rse/mock/fb/d1/file |
  +---------+--------+------------+-----------+---------------------------------------------------------+
