Daemon rucio-abacus-account
***************************
.. argparse::
   :filename: bin/rucio-abacus-account
   :func: get_parser
   :prog: rucio-abacus-account

Description
-----------
The Abacus-Account daemon updates the account usages. It checks if there are new entries in the UpdatedAccountCounter table and updates the account counters in the AccountCounter table by adding or substrating the amount of files and the size for each RSE.

Example
-------
Upload a file::

  $ rucio upload --rse MOCK --scope mock filename.txt

Check account usage::

  $ rucio list-account-usage username
  +-------+---------+---------+--------------+
  | RSE   | USAGE   | LIMIT   | QUOTA LEFT   |
  |-------+---------+---------+--------------|
  +-------+---------+---------+--------------+

Run the daemon::

  $ rucio-abacus-account --run-once

Check account usage again::

  $ rucio list-account-usage username
  +-------+------------+---------+--------------+
  | RSE   | USAGE      | LIMIT   | QUOTA LEFT   |
  |-------+------------+---------+--------------|
  | MOCK  | 211.724 kB | 0.000 B | 0.000 B      |
  +-------+------------+---------+--------------+
