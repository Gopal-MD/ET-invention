"""create normalized RegulaAI traceability schema"""
from alembic import op
from models import Base

revision = "0001_traceability"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    Base.metadata.create_all(op.get_bind())


def downgrade():
    Base.metadata.drop_all(op.get_bind())