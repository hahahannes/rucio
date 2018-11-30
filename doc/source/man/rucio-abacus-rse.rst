Daemon rucio-abacus-rse
***********************
.. argparse::
   :filename: bin/rucio-abacus-rse
   :func: get_parser
   :prog: rucio-abacus-rse

Description
-----------
The Abacus-RSE daemon is responsible for updating RSE usages. It checks if there are new entries in the UpdatedRSECounter table and updates the RSE counter in the RSECounter table by adding or substrating the amount of files and the size.

Example
-------
Upload a file to your RSE::

  $ rucio upload --rse MOCK --scope mock filename.txt

Check RSE usage::

  $ rucio list-rse-usage MOCK
  USAGE:
  ------
     files: 0
     used: 0.000 B
     rse: MOCK
     updated_at: 2018-11-30 14:28:34
     source: rucio
  ------

Run the daemon::

  $ rucio-abacus-rse --run-once

Check RSE usage again::

  $ rucio list-rse-usage MOCK
  USAGE:
  ------
      files: 1
      used: 213.481 kB
      rse: MOCK
      updated_at: 2018-12-03 08:58:33
      source: rucio
  ------
