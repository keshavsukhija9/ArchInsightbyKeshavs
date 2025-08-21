"""
Create core tables: users, projects, analyses
"""
from alembic import op
import sqlalchemy as sa

revision = '20250821_01'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String(64), unique=True, nullable=False),
        sa.Column('email', sa.String(128), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(256), nullable=False),
        sa.Column('full_name', sa.String(128), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(128), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('repository_url', sa.String(512), nullable=True),
        sa.Column('language', sa.String(64), nullable=True),
        sa.Column('status', sa.String(32), nullable=False, default='active'),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )
    
    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('analysis_type', sa.String(32), nullable=False, default='dependency'),
        sa.Column('status', sa.String(32), nullable=False, default='pending'),
        sa.Column('progress', sa.Integer, nullable=False, default=0),
        sa.Column('results', sa.JSON, nullable=True),
        sa.Column('error_message', sa.Text, nullable=True),
        sa.Column('options', sa.JSON, nullable=True),
        sa.Column('started_at', sa.DateTime, nullable=False),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    
    # Create indexes for better performance
    op.create_index('ix_users_username', 'users', ['username'])
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_projects_name', 'projects', ['name'])
    op.create_index('ix_projects_owner_id', 'projects', ['owner_id'])
    op.create_index('ix_analyses_project_id', 'analyses', ['project_id'])
    op.create_index('ix_analyses_status', 'analyses', ['status'])

def downgrade():
    # Drop indexes first
    op.drop_index('ix_analyses_status', 'analyses')
    op.drop_index('ix_analyses_project_id', 'analyses')
    op.drop_index('ix_projects_owner_id', 'projects')
    op.drop_index('ix_projects_name', 'projects')
    op.drop_index('ix_users_email', 'users')
    op.drop_index('ix_users_username', 'users')
    
    # Drop tables in reverse order (due to foreign key constraints)
    op.drop_table('analyses')
    op.drop_table('projects')
    op.drop_table('users')
