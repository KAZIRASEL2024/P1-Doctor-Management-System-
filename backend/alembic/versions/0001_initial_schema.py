"""Initial schema — all tables.

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2024-01-01 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── users ──────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id",              sa.Integer,     primary_key=True),
        sa.Column("email",           sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name",       sa.String(255), nullable=False),
        sa.Column("role",            sa.String(50),  nullable=False, server_default="doctor"),
        sa.Column("is_active",       sa.Boolean,     nullable=False, server_default="true"),
        sa.Column("created_at",      sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("last_login_at",   sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"])

    # ── zones ──────────────────────────────────────────────────────────────
    op.create_table(
        "zones",
        sa.Column("id",              sa.Integer,     primary_key=True),
        sa.Column("name",            sa.String(255), nullable=False),
        sa.Column("erp_region_code", sa.String(50),  nullable=True, unique=True),
        sa.Column("description",     sa.Text,        nullable=True),
        sa.Column("is_active",       sa.Boolean,     nullable=False, server_default="true"),
    )

    # ── doctors ────────────────────────────────────────────────────────────
    op.create_table(
        "doctors",
        sa.Column("id",                   sa.Integer,     primary_key=True),
        sa.Column("user_id",              sa.Integer,     sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("registration_number",  sa.String(100), nullable=False, unique=True),
        sa.Column("specialization",       sa.String(255), nullable=False),
        sa.Column("qualification",        sa.String(255), nullable=False),
        sa.Column("phone",                sa.String(30),  nullable=False),
        sa.Column("bio",                  sa.Text,        nullable=True),
        sa.Column("avatar_url",           sa.String(500), nullable=True),
        sa.Column("is_emergency_doctor",  sa.Boolean,     nullable=False, server_default="false"),
        sa.Column("is_available",         sa.Boolean,     nullable=False, server_default="true"),
    )

    # ── doctor_zone_assignments ────────────────────────────────────────────
    op.create_table(
        "doctor_zone_assignments",
        sa.Column("id",          sa.Integer,  primary_key=True),
        sa.Column("doctor_id",   sa.Integer,  sa.ForeignKey("doctors.id"), nullable=False),
        sa.Column("zone_id",     sa.Integer,  sa.ForeignKey("zones.id"),   nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("assigned_by", sa.String(255), nullable=True),
    )
    op.create_index("ix_dza_doctor",  "doctor_zone_assignments", ["doctor_id"])
    op.create_index("ix_dza_zone",    "doctor_zone_assignments", ["zone_id"])

    # ── consultations ──────────────────────────────────────────────────────
    op.create_table(
        "consultations",
        sa.Column("id",                       sa.Integer,     primary_key=True),
        sa.Column("aisp_reference",           sa.String(100), nullable=True),
        sa.Column("zone_id",                  sa.Integer,     sa.ForeignKey("zones.id"), nullable=True),
        sa.Column("field_worker_name",        sa.String(255), nullable=False),
        sa.Column("field_worker_phone",       sa.String(30),  nullable=True),
        sa.Column("animal_species",           sa.String(100), nullable=False),
        sa.Column("animal_breed",             sa.String(100), nullable=True),
        sa.Column("animal_age_months",        sa.Integer,     nullable=True),
        sa.Column("animal_weight_kg",         sa.Float,       nullable=True),
        sa.Column("animal_temperature_celsius", sa.Float,     nullable=True),
        sa.Column("animal_owner_name",        sa.String(255), nullable=True),
        sa.Column("symptoms",                 sa.Text,        nullable=False),
        sa.Column("remarks",                  sa.Text,        nullable=True),
        sa.Column("priority",                 sa.String(20),  nullable=False, server_default="normal"),
        sa.Column("status",                   sa.String(30),  nullable=False, server_default="pending"),
        sa.Column("submitted_at",             sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("responded_at",             sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at",                sa.DateTime(timezone=True), nullable=True),
        sa.Column("sla_deadline",             sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_consultations_aisp_ref", "consultations", ["aisp_reference"])

    # ── attachments ────────────────────────────────────────────────────────
    op.create_table(
        "attachments",
        sa.Column("id",              sa.Integer,     primary_key=True),
        sa.Column("consultation_id", sa.Integer,     sa.ForeignKey("consultations.id"), nullable=False),
        sa.Column("file_name",       sa.String(255), nullable=False),
        sa.Column("file_type",       sa.String(20),  nullable=False),
        sa.Column("mime_type",       sa.String(100), nullable=False),
        sa.Column("storage_path",    sa.String(500), nullable=False),
        sa.Column("file_size_bytes", sa.Integer,     nullable=False, server_default="0"),
        sa.Column("uploaded_at",     sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_attachments_consultation", "attachments", ["consultation_id"])

    # ── consultation_responses ─────────────────────────────────────────────
    op.create_table(
        "consultation_responses",
        sa.Column("id",                    sa.Integer, primary_key=True),
        sa.Column("consultation_id",       sa.Integer, sa.ForeignKey("consultations.id"), nullable=False),
        sa.Column("doctor_id",             sa.Integer, sa.ForeignKey("doctors.id"),       nullable=False),
        sa.Column("diagnosis",             sa.Text,    nullable=False),
        sa.Column("treatment_plan",        sa.Text,    nullable=False),
        sa.Column("medications",           sa.Text,    nullable=True),
        sa.Column("follow_up_instructions",sa.Text,    nullable=True),
        sa.Column("is_emergency_referral", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at",  sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at",  sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_responses_consultation", "consultation_responses", ["consultation_id"])
    op.create_index("ix_responses_doctor",       "consultation_responses", ["doctor_id"])

    # ── notifications ──────────────────────────────────────────────────────
    op.create_table(
        "notifications",
        sa.Column("id",                sa.Integer,     primary_key=True),
        sa.Column("user_id",           sa.Integer,     sa.ForeignKey("users.id"),         nullable=False),
        sa.Column("consultation_id",   sa.Integer,     sa.ForeignKey("consultations.id"), nullable=True),
        sa.Column("title",             sa.String(255), nullable=False),
        sa.Column("body",              sa.Text,        nullable=False),
        sa.Column("notification_type", sa.String(50),  nullable=False, server_default="info"),
        sa.Column("is_read",           sa.Boolean,     nullable=False, server_default="false"),
        sa.Column("created_at",        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("read_at",           sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_notifications_user", "notifications", ["user_id"])

    # ── audit_logs ─────────────────────────────────────────────────────────
    op.create_table(
        "audit_logs",
        sa.Column("id",            sa.Integer,     primary_key=True),
        sa.Column("user_id",       sa.Integer,     sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action",        sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id",   sa.Integer,     nullable=True),
        sa.Column("details",       sa.Text,        nullable=True),
        sa.Column("ip_address",    sa.String(45),  nullable=True),
        sa.Column("created_at",    sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("notifications")
    op.drop_table("consultation_responses")
    op.drop_table("attachments")
    op.drop_table("consultations")
    op.drop_table("doctor_zone_assignments")
    op.drop_table("doctors")
    op.drop_table("zones")
    op.drop_table("users")
