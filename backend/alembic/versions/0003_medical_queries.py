"""Add human patient profiles and medical queries.

Revision ID: 0003_medical_queries
Revises: 0002_patients
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_medical_queries"
down_revision = "0002_patients"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patient_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("gender", sa.String(50), nullable=False),
        sa.Column("contact_details", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_patient_profiles_user_id"),
    )
    op.create_index("ix_patient_profiles_id", "patient_profiles", ["id"])
    op.create_table(
        "medical_queries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=True),
        sa.Column("status", sa.String(20), server_default="Pending", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_medical_queries_id", "medical_queries", ["id"])
    op.create_index("ix_medical_queries_patient_id", "medical_queries", ["patient_id"])
    op.create_index("ix_medical_queries_doctor_id", "medical_queries", ["doctor_id"])


def downgrade() -> None:
    op.drop_index("ix_medical_queries_doctor_id", table_name="medical_queries")
    op.drop_index("ix_medical_queries_patient_id", table_name="medical_queries")
    op.drop_index("ix_medical_queries_id", table_name="medical_queries")
    op.drop_table("medical_queries")
    op.drop_index("ix_patient_profiles_id", table_name="patient_profiles")
    op.drop_table("patient_profiles")
