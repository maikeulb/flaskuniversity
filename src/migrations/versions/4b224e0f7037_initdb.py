"""initdb

Revision ID: 4b224e0f7037
Revises: 
Create Date: 2018-03-21 22:55:55.831385

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4b224e0f7037'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instructors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('hire_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('enrollment_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('budget', sa.Numeric(precision=8, scale=2), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('instructor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('office_assignments',
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('instructor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ),
    sa.PrimaryKeyConstraint('location')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('credits', sa.Integer(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_assignments',
    sa.Column('instructor_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ),
    sa.PrimaryKeyConstraint('instructor_id', 'course_id')
    )
    op.create_table('enrollments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('grade', postgresql.ENUM('A', 'B', 'C', 'D', 'F', name='grade_enum'), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('enrollments')
    op.drop_table('course_assignments')
    op.drop_table('courses')
    op.drop_table('office_assignments')
    op.drop_table('departments')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('students')
    op.drop_table('instructors')
    # ### end Alembic commands ###
