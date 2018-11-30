Daemon rucio-necromancer
************************
.. argparse::
   :filename: bin/rucio-necromancer
   :func: get_parser
   :prog: rucio-necromancer

Description
-----------
The Necromancer daemon is responsible for managing bad replicas. If a replica that got declared bad has other replicas, it will try to recover it by requesting a new transfer. If there are no replicas anymore, then the file gets marked as lost.

Example - lost replica
----------------------
In this example the file gets uploaded and will have only this replica as there are no replication rules. If it gets declared bad, there will be no replica to recover from.
Therefor the replica gets marked as lost.

Upload a file::

  $ rucio upload --scope mock --rse MOCK --name file filename.txt

Check replicas::

  $ rucio list-file-replicas mock:file
  +---------+--------+------------+-----------+---------------------------------------------------------+
  | SCOPE   | NAME   | FILESIZE   |   ADLER32 | RSE: REPLICA                                            |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 149.000 B  |    948240 | MOCK: file://localhost:0/tmp/rucio_rse/mock/fb/d1/file  |
  +---------+--------+------------+-----------+---------------------------------------------------------+

Declare it as bad::

  $ rucio-admin replicas declare-bad file://localhost:0/tmp/rucio_rse/mock/fb/d1/file --reason 'bad'

Run the daemon::

  $ rucio-necromancer --run-once

Check replicas again::

  $ rucio list-file-replicas mock:file
  +---------+--------+------------+-----------+----------------+
  | SCOPE   | NAME   | FILESIZE   | ADLER32   | RSE: REPLICA   |
  |---------+--------+------------+-----------+----------------|
  +---------+--------+------------+-----------+----------------+

Example - bad replica
---------------------
In this example the file gets uploaded and will have two replica. If it gets declared bad, then the daemon will try to recover it from the second replica.

Upload a file and replicate it::

  $ rucio upload --scope mock --rse MOCK filename.txt
  $ rucio add-rule mock:file 1 MOCK2
  $ rucio-conveyor-submitter --run-once

Check replicas::

  $ rucio list-file-replicas mock:file
  +---------+--------+------------+-----------+---------------------------------------------------------+
  | SCOPE   | NAME   | FILESIZE   |   ADLER32 | RSE: REPLICA                                            |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 149.000 B  |    948240 | MOCK: file://localhost:0/tmp/rucio_rse/mock/fb/d1/file  |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 149.000 B  |    948240 | MOCK2: file://localhost:1/tmp/rucio_rse/mock/fb/d1/file |
  +---------+--------+------------+-----------+---------------------------------------------------------+

Declare one replica as bad::

  $ rucio-admin replicas declare-bad file://localhost:1/tmp/rucio_rse/mock/fb/d1/file --reason 'bad'

Run the daemon::

  $ rucio-necromancer --run-once

Check replicas again::

  $ rucio list-file-replicas mock:file
  +---------+--------+------------+-----------+---------------------------------------------------------+
  | SCOPE   | NAME   | FILESIZE   |   ADLER32 | RSE: REPLICA                                            |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 149.000 B  |    948240 | MOCK: file://localhost:0/tmp/rucio_rse/mock/fb/d1/file  |
  |---------+--------+------------+-----------+---------------------------------------------------------|
  | mock    | file   | 149.000 B  |    948240 | MOCK2: file://localhost:1/tmp/rucio_rse/mock/fb/d1/file |
  +---------+--------+------------+-----------+---------------------------------------------------------+
