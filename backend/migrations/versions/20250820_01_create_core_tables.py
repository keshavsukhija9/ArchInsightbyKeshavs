"""
Create core tables: users, projects, analyses
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '20250820_01'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(64), unique=True, nullable=False),
        sa.Column('email', sa.String(128), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(256), nullable=False),
        sa.Column('full_name', sa.String(128)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(128), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('repository_url', sa.String(512)),
        sa.Column('language', sa.String(64)),
        sa.Column('status', sa.String(32), server_default='active'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )
    
    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('analysis_type', sa.String(32), server_default='dependency'),
        sa.Column('status', sa.String(32), server_default='pending'),
        sa.Column('progress', sa.Integer, server_default=0),
        sa.Column('results', postgresql.JSON),
        sa.Column('error_message', sa.Text),
        sa.Column('options', postgresql.JSON),
        sa.Column('started_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

def downgrade():
    op.drop_table('analyses')
    op.drop_table('projects')
    op.drop_table('users')
