Daemon rucio-reaper
*******************
.. argparse::
   :module: rucio.clis.daemons.reaper.reaper
   :func: get_parser
   :prog: rucio-reaper

Description
-----------
The Reaper daemon is responsible for replica deletion. It deletes them by checking if there are replicas that are not locked and have a tombstone to indicate that they can be deleted.

Example
-------
Upload a file and prepare the rules and replicas for deletion by using the judge-cleaner daemon::

  $ rucio upload --rse MOCK --scope mock --name file filename.txt
  $ rucio add-rule mock:file 1 MOCK2 --lifetime 1
  $ rucio-judge-cleaner --run-once

Check if the replica was created::

  $ rucio list-file-replica mock:file
  +---------+--------+------------+-----------+---------------------------------------------------------+
  | SCOPE   | NAME   | FILESIZE   | ADLER32   | RSE: REPLICA                                            |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 1.542 kB   | 1268ee71  | MOCK: file://localhost:0/tmp/rucio_rse/mock/15/58/file  |
  +---------+--------+------------+-----------+---------------------------------------------------------+

Run the daemon::

  $ rucio-reaper --run-once

Check if the replica exists::

  $ rucio list-file-replica mock:file
  +---------+--------+------------+-----------+---------------------------------------------------------+
  | SCOPE   | NAME   | FILESIZE   | ADLER32   | RSE: REPLICA                                            |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  +---------+--------+------------+-----------+---------------------------------------------------------+
