"""initial doctor service tables

Revision ID: cce01462edbb
Revises: 
Create Date: 2018-06-06 08:52:33.826716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cce01462edbb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        """
        CREATE TABLE doctor (
        id SERIAL PRIMARY KEY
        name TEXT NOT NULL);

        CREATE UNIQUE INDEX doctor__name on doctor(name);

        CREATE TABLE doctor_location (
        id SERIAL PRIMARY KEY
        doctor_id REFERENCES doctor(id)
        name TEXT NOT NULL);

        CREATE UNIQUE INDEX doctor_locations__name on doctor_location(name);

        CREATE TABLE doctor_schedule (
        id SERIAL PRIMARY KEY
        doctor_id REFERENCE doctor(id)
        location_id REFERENCE location(id)
        day TEXT NOT NULL
        start_time TIME WITH TIME ZONE
        end_time TIME WITH TIME ZONE
        );

        """


    )


def downgrade():
    pass
