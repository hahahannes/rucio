Daemon rucio-judge-cleaner
**************************
.. argparse::
   :filename: bin/rucio-judge-cleaner
   :func: get_parser
   :prog: rucio-judge-cleaner

Description
-----------
The Judge-Cleaner daemon is responsible for cleaning expired replication rules. It deletes rules by checking if the 'expired_at' date property is older than the current timestamp.
If the rule is expired, it will first remove one lock for the replica and parent datasets if the DID belongs to any. Then it will set a tombstone to the replica to mark it as deletable if there are no rules protecting the replica. After these steps, the rule gets deleted.

Example
-------
Upload a file to your RSE::

  $ rucio upload --rse MOCK --scope mock --name file filename.txt

Set a replication rule for the file with a lifetime of one second::

  $ rucio add-rule mock:file 1 MOCK2 --lifetime 1

Check the replication rules and the replicas::

  $ rucio list-rules mock:file
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)        CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  -------------------  -------------------
  c273c7ed75724143ad21c667e659456b  root       mock:file     REPLICATING[0/1/0]      MOCK2                    1  2018-12-03 09:53:09  2018-12-03 09:53:08
  06f012771b0546dca0c908441c048964  root       mock:file     OK[1/0/0]               MOCK                     1                       2018-12-03 09:52:19

  $ python
  from rucio.db.sqla import session, models
  from rucio.core.rse import get_rse_id
  rse_id = get_rse_id('MOCK2')
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().tombstone // None
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().lock_cnt // 1

The first rule was created with an expiration date of one second after the creation date.

Run the daemon::

  $ rucio-judge-cleaner --run-once

Check the replication rules and the replicas::

  $ rucio list-rules mock:file
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  ---------------  -------------------
  06f012771b0546dca0c908441c048964  root       mock:file     OK[1/0/0]               MOCK                     1                   2018-12-03 09:52:19

  $ python
  from rucio.db.sqla import session, models
  from rucio.core.rse import get_rse_id
  rse_id = get_rse_id('MOCK2')
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().tombstone // datetime.datetime(1970, 1, 1, 0, 0)
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().lock_cnt // 0

The rule we created before was deleted and the replica of the file on RSE MOCK2 got a tombstone because there is no protecting rule anymore.
