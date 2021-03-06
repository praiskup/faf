# Copyright (C) 2014  ABRT Team
# Copyright (C) 2014  Red Hat, Inc.
#
# This file is part of faf.
#
# faf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# faf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with faf.  If not, see <http://www.gnu.org/licenses/>.

"""
ACL permissions

Revision ID: 47cf82727ed1
Revises: 2e5f6d8b68f5
Create Date: 2015-01-29 13:51:42.674771
"""

from alembic.op import get_bind, add_column, drop_constraint, create_primary_key, drop_column
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "47cf82727ed1"
down_revision = "2e5f6d8b68f5"


def upgrade():
    enum = postgresql.ENUM("watchbugzilla", "commit", name="permission_type", create_type=False)
    enum.create(get_bind(), checkfirst=False)
    add_column("opsysreleasescomponentsassociates",
               sa.Column("permission", enum, nullable=False, server_default="commit", primary_key=True))
    drop_constraint(
        "opsysreleasescomponentsassociates_pkey",
        "opsysreleasescomponentsassociates"
        )
    create_primary_key(
        "opsysreleasescomponentsassociates_pkey",
        "opsysreleasescomponentsassociates",
        ["opsysreleasecompoents_id", "associatepeople_id", "permission"]
        )


def downgrade():
    drop_column("opsysreleasescomponentsassociates", "permission")
    postgresql.ENUM(name="permission_type").drop(get_bind(), checkfirst=False)
    drop_constraint(
        "opsysreleasescomponentsassociates_pkey",
        "opsysreleasescomponentsassociates"
        )
    create_primary_key(
        "opsysreleasescomponentsassociates_pkey",
        "opsysreleasescomponentsassociates",
        ["opsysreleasecompoents_id", "associatepeople_id"]
        )
