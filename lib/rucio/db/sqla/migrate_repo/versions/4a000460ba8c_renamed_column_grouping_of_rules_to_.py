# Copyright 2013-2019 CERN for the benefit of the ATLAS collaboration.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# - Hannes Hansen <hannes.jakob.hansen@cern.ch>, 2019

''' renamed column grouping of rules to rule_grouping '''

from alembic import context
from alembic.op import (create_check_constraint, drop_constraint, alter_column)

from rucio.db.sqla.constants import RuleGrouping

# Alembic revision identifiers
revision = '4a000460ba8c'
down_revision = 'b8caac94d7f0'


constraint_name = 'RULES_GROUPING_NN'
table_name = 'rules'
schema = context.get_context().version_table_schema + '.' if context.get_context().version_table_schema else ''
old_column_name = 'grouping'
new_column_name = 'rule_grouping'


def upgrade():
    '''
    Upgrade the database to this revision
    '''

    if context.get_context().dialect.name in ['oracle', 'postgresql']:
        drop_constraint(constraint_name, table_name, type_='check', schema=schema)
        create_check_constraint(constraint_name, table_name, 'RULE_GROUPING IS NOT NULL', schema=schema)
        alter_column(table_name, old_column_name, new_column_name=new_column_name)

    if context.get_context().dialect.name == 'mysql':
        # constraints are parsed but ignored in mysql, so drop is not possible
        create_check_constraint(constraint_name, table_name, 'RULE_GROUPING IS NOT NULL', schema=schema)
        alter_column(table_name, old_column_name, new_column_name=new_column_name, existing_type=RuleGrouping.db_type(name='RULES_GROUPING_CHK'), existing_server_default='A', existing_nullable=False)


def downgrade():
    '''
    Downgrade the database to the previous revision
    '''

    if context.get_context().dialect.name in ['oracle', 'postgresql']:
        drop_constraint(constraint_name, table_name, type_='check', schema=schema)
        create_check_constraint(constraint_name, table_name, 'GROUPING IS NOT NULL', schema=schema)
        alter_column(table_name, new_column_name, new_column_name=old_column_name)

    if context.get_context().dialect.name == 'mysql':
        alter_column(table_name, new_column_name, new_column_name=old_column_name, existing_type=RuleGrouping.db_type(name='RULES_GROUPING_CHK'), existing_server_default='A', existing_nullable=False)
