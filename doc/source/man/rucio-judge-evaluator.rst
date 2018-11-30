Daemon rucio-judge-evaluator
****************************
.. argparse::
   :filename: bin/rucio-judge-evaluator
   :func: get_parser
   :prog: rucio-judge-evaluator

Description
-----------
The Judge-Evaluator is responsible for execution and reevaluation of replication rules.
First it checks if there are DIDs that have changed.
In case of a new attachment, the replication rule for the dataset has to be applied to the attached DID, too.
If the DID is a dataset, its properties like size and length get updated and also an entry is saved to mark a change for possible collection replicas which have to be updated, too.

Example
-------
Create a dataset with a replication rule and upload a file which gets attached to the dataset::

  $ rucio add-dataset mock:dataset
  $ rucio add-rule mock:dataset 1 MOCK
  $ rucio upload --scope mock --rse MOCK --name file filename.txt
  $ rucio attach mock:dataset mock:file

Check the rules and locks for the dataset and the file::

  $ rucio list-rules mock:dataset
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  ---------------  -------------------
  e95941c165d54e38b6e46990de06d3d4  root       mock:dataset  OK[0/0/0]               MOCK                     1                   2018-12-03 12:35:43

  $ python
  from rucio.db.sqla import session, models
  from rucio.core.rse import get_rse_id
  rse_id = get_rse_id('MOCK')
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().lock_cnt // 1

There is one rule for the dataset which we created before and one lock for the file which got created with the upload.

Run the daemon::

  $ rucio-judge-evaluator --run-once

Check the locks for the file again::

  $ python
  from rucio.db.sqla import session, models
  from rucio.core.rse import get_rse_id
  rse_id = get_rse_id('MOCK')
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().lock_cnt // 2
