Daemon rucio-judge-evaluator
****************************
.. argparse::
   :filename: bin/rucio-judge-evaluator
   :func: get_parser
   :prog: rucio-judge-evaluator

Description
-----------
The Judge-Evaluator daemon is responsible for execution and reevaluation of replication rules.
First it checks if there are DIDs that have changed content e.g. attached or deattched DIDs.
In case of a new attachment, the replication rule for the dataset has to be applied to the attached DID, too. If the attached DID has already a replica on a RSE that satisfies the RSE expression of the rule, then the lock counter of that replia gets increased.
If it does not have any replica satisfying the rule, then a new replica has to be created.
In case of a new dettachment, the replica has to be removed or the lock counter of the replica has to be decreased, depending on which RSE the replica exist.
If the DID is a dataset, its properties like size and length also get updated and also an entry is saved to mark a change for possible collection replicas which have to be updated by another daemon.

Example - Same RSEs
-------------------
Create a dataset with a replication rule and upload a file to the same RSE. Then attach it to the dataset::

  $ rucio add-dataset mock:dataset
  $ rucio add-rule mock:dataset 1 MOCK
  $ rucio upload --scope mock --rse MOCK --name file filename.txt
  $ rucio attach mock:dataset mock:file

Check the rules and locks for the dataset and the replica::

  $ rucio list-rules mock:dataset
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  ---------------  -------------------
  e95941c165d54e38b6e46990de06d3d4  root       mock:dataset  OK[0/0/0]               MOCK                     1                   2018-12-03 12:35:43

  $ rucio list-rule mock:file
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  ---------------  -------------------
  cfec9a944cdd4543b7267a34a2584631  root       mock:file     OK[1/0/0]               MOCK                     1                   2018-12-11 08:29:49

  $ python
  from rucio.db.sqla import session, models
  from rucio.core.rse import get_rse_id
  rse_id = get_rse_id('MOCK')
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().lock_cnt // 1

There is one rule for the dataset which we created before and one lock and one rule for the replica which got created with the upload of the file.

Run the daemon::

  $ rucio-judge-evaluator --run-once

Check the locks for the replica again::

  $ python
  from rucio.db.sqla import session, models
  from rucio.core.rse import get_rse_id
  rse_id = get_rse_id('MOCK')
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().lock_cnt // 2

The replica of the DID mock:file has now 2 locks on RSE MOCK, because it is protected by the replication rule of the dataset and the first replication rule

Example - Different RSEs
------------------------
Create a dataset with a replication rule and upload a file to another RSE. Then attach it to the dataset::

  $ rucio add-dataset mock:dataset
  $ rucio add-rule mock:dataset 1 MOCK
  $ rucio upload --scope mock --rse MOCK2 --name file filename.txt
  $ rucio attach mock:dataset mock:file

Check the rules and locks for the dataset and the replica::

  $ rucio list-rules mock:dataset
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  ---------------  -------------------
  e95941c165d54e38b6e46990de06d3d4  root       mock:dataset  OK[0/0/0]               MOCK                     1                   2018-12-03 12:35:43

  $ rucio list-rule mock:file
  ID                                ACCOUNT    SCOPE:NAME    STATE[OK/REPL/STUCK]    RSE_EXPRESSION      COPIES  EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ------------  ----------------------  ----------------  --------  ---------------  -------------------
  cfec9a944cdd4543b7267a34a2584631  root       mock:file     OK[1/0/0]               MOCK2                    1                   2018-12-11 08:29:49

  $ python
  from rucio.db.sqla import session, models
  from rucio.core.rse import get_rse_id
  rse_id = get_rse_id('MOCK2')
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock', rse_id=rse_id).first().lock_cnt // 1

There is one rule for the dataset which we created before and one lock and one rule for the replica which got created with the upload of the file.

Run the daemon::

  $ rucio-judge-evaluator --run-once

Check the replicas for the DID mock:file::

  $ python
  from rucio.db.sqla import session, models
  session.get_session().query(models.RSEFileAssociation).filter_by(name='file', scope='mock').first()
  // [{'name': 'file','lock_cnt': 1, 'state': COPYING, 'scope': 'mock', 'rse_id': 'f81f366593754c01b0c340fa5ea0ab90'},
  //  {'scope': 'mock', 'rse_id': '1330d5daee37474c88ba888101d7b859', 'name': 'file', 'state': AVAIABLE, 'lock_cnt': 1}]

The DID mock:file has now two replicas with one lock each.
As the file replica is attached to the dataset and the rule for the dataset specifies another RSE MOCK instead of the upload RSE, it has to be replicated to this RSE.
Therefor a second replica in state COPYING got created on RSE MOCK.
