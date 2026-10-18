"""Add animal patient profiles.

Revision ID: 0002_patients
Revises: 0001_initial_schema
Create Date: 2026-10-16 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0002_patients"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("species", sa.String(100), nullable=False),
        sa.Column("breed", sa.String(100), nullable=True),
        sa.Column("sex", sa.String(30), nullable=True),
        sa.Column("age_months", sa.Integer, nullable=True),
        sa.Column("weight_kg", sa.Float, nullable=True),
        sa.Column("owner_name", sa.String(255), nullable=False),
        sa.Column("owner_phone", sa.String(30), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("medical_notes", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_patients_id", "patients", ["id"])


def downgrade() -> None:
    op.drop_index("ix_patients_id", table_name="patients")
    op.drop_table("patients")
