"""
Demo data seeder — creates fictional but realistic BRAC AISP test data.

This module is imported by app/main.py at startup (when SEED_DEMO_DATA=true)
and can also be run standalone:

    python -m scripts.seed_demo_data

It is idempotent: re-running it will not create duplicate records.
All data is fictional and intended for demonstration only.
"""
from __future__ import annotations

import asyncio
import sys
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Allow running standalone from the backend/ directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.attachment import Attachment
from app.models.consultation import Consultation
from app.models.consultation_response import ConsultationResponse
from app.models.doctor import Doctor
from app.models.doctor_zone_assignment import DoctorZoneAssignment
from app.models.notification import Notification
from app.models.user import User
from app.models.zone import Zone


NOW = datetime.now(timezone.utc)


async def seed(db: AsyncSession) -> None:
    """Idempotent seed: skips if admin user already exists."""
    existing = await db.execute(select(User).where(User.email == "admin@brac-aisp.org"))
    if existing.scalar_one_or_none() is not None:
        return  # Already seeded

    # ── Users ──────────────────────────────────────────────────────────────
    admin = User(
        email="admin@brac-aisp.org",
        hashed_password=hash_password("Admin@1234"),
        full_name="AISP Administrator",
        role="admin",
    )

    dr_rahman = User(
        email="dr.rahman@brac-aisp.org",
        hashed_password=hash_password("Doctor@1234"),
        full_name="Dr. Kamal Rahman",
        role="doctor",
    )
    dr_begum = User(
        email="dr.begum@brac-aisp.org",
        hashed_password=hash_password("Doctor@1234"),
        full_name="Dr. Fatema Begum",
        role="doctor",
    )
    dr_hossain = User(
        email="dr.hossain@brac-aisp.org",
        hashed_password=hash_password("Doctor@1234"),
        full_name="Dr. Anwar Hossain",
        role="doctor",
    )
    dr_chowdhury = User(
        email="dr.chowdhury@brac-aisp.org",
        hashed_password=hash_password("Doctor@1234"),
        full_name="Dr. Nadia Chowdhury",
        role="doctor",
    )

    for u in [admin, dr_rahman, dr_begum, dr_hossain, dr_chowdhury]:
        db.add(u)
    await db.flush()

    # ── Zones ──────────────────────────────────────────────────────────────
    zones_data = [
        Zone(name="Dhaka Central", erp_region_code="DHK-C", description="Dhaka city central zone"),
        Zone(name="Dhaka North", erp_region_code="DHK-N", description="Dhaka city north zone"),
        Zone(name="Chittagong Port", erp_region_code="CTG-P", description="Chittagong port and surroundings"),
        Zone(name="Sylhet Tea Belt", erp_region_code="SYL-T", description="Sylhet tea estate region"),
        Zone(name="Rajshahi Agro", erp_region_code="RJH-A", description="Rajshahi agricultural zone"),
        Zone(name="Barisal South", erp_region_code="BSL-S", description="Barisal southern coastal zone"),
    ]
    for z in zones_data:
        db.add(z)
    await db.flush()

    dhaka_c, dhaka_n, ctg, sylhet, rajshahi, barisal = zones_data

    # ── Doctor Profiles ────────────────────────────────────────────────────
    doc_rahman = Doctor(
        user_id=dr_rahman.id,
        registration_number="VET-BD-001",
        specialization="Large Animal Medicine",
        qualification="BVSc & AH, MVSc (Medicine)",
        phone="+880-1711-000001",
        bio="Dr. Kamal Rahman has 12 years of experience treating cattle and goats across rural Bangladesh.",
        is_emergency_doctor=False,
        is_available=True,
    )
    doc_begum = Doctor(
        user_id=dr_begum.id,
        registration_number="VET-BD-002",
        specialization="Poultry Medicine",
        qualification="BVSc & AH, PhD (Poultry Pathology)",
        phone="+880-1711-000002",
        bio="Dr. Fatema Begum specialises in poultry diseases and biosecurity protocols.",
        is_emergency_doctor=False,
        is_available=True,
    )
    doc_hossain = Doctor(
        user_id=dr_hossain.id,
        registration_number="VET-BD-003",
        specialization="Emergency Veterinary Care",
        qualification="BVSc & AH, MVPH",
        phone="+880-1711-000003",
        bio="Dr. Anwar Hossain handles emergency and after-hours cases 24/7.",
        is_emergency_doctor=True,
        is_available=True,
    )
    doc_chowdhury = Doctor(
        user_id=dr_chowdhury.id,
        registration_number="VET-BD-004",
        specialization="Small Ruminants & Aquaculture",
        qualification="BVSc & AH, MSc (Aquaculture)",
        phone="+880-1711-000004",
        bio="Dr. Nadia Chowdhury covers goats, sheep, and fish pond health management.",
        is_emergency_doctor=False,
        is_available=True,
    )

    for d in [doc_rahman, doc_begum, doc_hossain, doc_chowdhury]:
        db.add(d)
    await db.flush()

    # ── Zone Assignments ───────────────────────────────────────────────────
    assignments = [
        DoctorZoneAssignment(doctor_id=doc_rahman.id, zone_id=dhaka_c.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_rahman.id, zone_id=dhaka_n.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_begum.id, zone_id=ctg.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_begum.id, zone_id=sylhet.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_chowdhury.id, zone_id=rajshahi.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_chowdhury.id, zone_id=barisal.id, assigned_by="Administrator"),
        # Emergency doctor covers all zones
        DoctorZoneAssignment(doctor_id=doc_hossain.id, zone_id=dhaka_c.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_hossain.id, zone_id=ctg.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_hossain.id, zone_id=sylhet.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_hossain.id, zone_id=rajshahi.id, assigned_by="Administrator"),
        DoctorZoneAssignment(doctor_id=doc_hossain.id, zone_id=barisal.id, assigned_by="Administrator"),
    ]
    for a in assignments:
        db.add(a)
    await db.flush()

    # ── Consultations ──────────────────────────────────────────────────────
    consultations_data = [
        # Pending
        Consultation(
            aisp_reference="AISP-2024-0001",
            zone_id=dhaka_c.id,
            field_worker_name="Rahim Mia",
            field_worker_phone="+880-1812-100001",
            animal_species="Cattle",
            animal_breed="Shahiwal",
            animal_age_months=36,
            animal_weight_kg=280.0,
            animal_temperature_celsius=39.8,
            animal_owner_name="Haji Abdul Karim",
            symptoms="Reduced feed intake, nasal discharge, mild cough for 3 days. Animal appears lethargic.",
            remarks="Owner reports similar symptoms in neighbouring cattle 2 weeks ago.",
            priority="urgent",
            status="pending",
            submitted_at=NOW - timedelta(hours=5),
            sla_deadline=NOW + timedelta(hours=1),
        ),
        Consultation(
            aisp_reference="AISP-2024-0002",
            zone_id=ctg.id,
            field_worker_name="Sumaiya Akter",
            field_worker_phone="+880-1812-100002",
            animal_species="Poultry",
            animal_breed="Sonali",
            animal_age_months=4,
            animal_weight_kg=1.2,
            animal_temperature_celsius=41.5,
            animal_owner_name="Mrs. Rehana Parvin",
            symptoms="Mass mortality in flock — 15 birds died overnight. Survivors show difficulty breathing.",
            remarks="Flock size was 200. Vaccination record not available.",
            priority="emergency",
            status="pending",
            submitted_at=NOW - timedelta(hours=1),
            sla_deadline=NOW + timedelta(minutes=30),
        ),
        # In Progress
        Consultation(
            aisp_reference="AISP-2024-0003",
            zone_id=sylhet.id,
            field_worker_name="Mohammed Jamal",
            field_worker_phone="+880-1812-100003",
            animal_species="Goat",
            animal_breed="Black Bengal",
            animal_age_months=18,
            animal_weight_kg=22.0,
            animal_temperature_celsius=40.2,
            animal_owner_name="Md. Shafiqul Islam",
            symptoms="Swollen lymph nodes under jaw, difficulty swallowing, drooling.",
            remarks="Animal was purchased at market 10 days ago.",
            priority="normal",
            status="in_progress",
            submitted_at=NOW - timedelta(days=1, hours=3),
            sla_deadline=NOW + timedelta(hours=5),
        ),
        # Responded
        Consultation(
            aisp_reference="AISP-2024-0004",
            zone_id=dhaka_n.id,
            field_worker_name="Rashida Khanam",
            field_worker_phone="+880-1812-100004",
            animal_species="Cattle",
            animal_breed="Friesian Cross",
            animal_age_months=48,
            animal_weight_kg=400.0,
            animal_temperature_celsius=38.5,
            animal_owner_name="Nur Islam",
            symptoms="Milk production drop by 40% over 1 week. Udder appears normal on palpation.",
            remarks="No recent feed changes. Currently in 3rd lactation.",
            priority="normal",
            status="responded",
            submitted_at=NOW - timedelta(days=3),
            responded_at=NOW - timedelta(days=2, hours=6),
            sla_deadline=NOW - timedelta(days=2, hours=8),
        ),
        # Overdue
        Consultation(
            aisp_reference="AISP-2024-0005",
            zone_id=rajshahi.id,
            field_worker_name="Belal Hossain",
            field_worker_phone="+880-1812-100005",
            animal_species="Duck",
            animal_breed="Khaki Campbell",
            animal_age_months=6,
            animal_weight_kg=1.8,
            animal_temperature_celsius=None,
            animal_owner_name="Komola Begum",
            symptoms="Twisted neck, loss of balance, inability to stand. Condition spreading in flock.",
            remarks="Approximately 30% of 50-bird flock affected.",
            priority="urgent",
            status="overdue",
            submitted_at=NOW - timedelta(hours=10),
            sla_deadline=NOW - timedelta(hours=2),
        ),
        # Additional responded cases
        Consultation(
            aisp_reference="AISP-2024-0006",
            zone_id=barisal.id,
            field_worker_name="Tariq Ahmed",
            field_worker_phone="+880-1812-100006",
            animal_species="Fish",
            animal_breed="Rui (Labeo rohita)",
            animal_age_months=8,
            animal_weight_kg=None,
            animal_temperature_celsius=None,
            animal_owner_name="Sirajul Haque",
            symptoms="Fish found floating at pond surface. Fins showing haemorrhagic spots. Mortality ~5%.",
            remarks="Recent heavy rainfall. Pond area: 0.5 acre.",
            priority="normal",
            status="responded",
            submitted_at=NOW - timedelta(days=5),
            responded_at=NOW - timedelta(days=4),
            sla_deadline=NOW - timedelta(days=4, hours=2),
        ),
        Consultation(
            aisp_reference="AISP-2024-0007",
            zone_id=dhaka_c.id,
            field_worker_name="Amina Sultana",
            field_worker_phone="+880-1812-100007",
            animal_species="Cattle",
            animal_breed="Local",
            animal_age_months=24,
            animal_weight_kg=190.0,
            animal_temperature_celsius=41.1,
            animal_owner_name="Abdul Mannan",
            symptoms="High fever, swollen face and throat, sudden onset. Animal showing signs of extreme distress.",
            remarks="No recent vaccination record found.",
            priority="emergency",
            status="responded",
            submitted_at=NOW - timedelta(days=7),
            responded_at=NOW - timedelta(days=7, hours=-2),
            sla_deadline=NOW - timedelta(days=7, hours=-3),
        ),
        Consultation(
            aisp_reference="AISP-2024-0008",
            zone_id=ctg.id,
            field_worker_name="Rubel Khan",
            field_worker_phone="+880-1812-100008",
            animal_species="Poultry",
            animal_breed="Layer",
            animal_age_months=12,
            animal_weight_kg=1.9,
            animal_temperature_celsius=42.0,
            animal_owner_name="Jahanara Begum",
            symptoms="Egg production fell from 85% to 40%. Pale comb, reduced appetite.",
            remarks="Farm size: 500 birds. Last deworming: 3 months ago.",
            priority="normal",
            status="pending",
            submitted_at=NOW - timedelta(hours=8),
            sla_deadline=NOW + timedelta(hours=4),
        ),
    ]

    for c in consultations_data:
        db.add(c)
    await db.flush()

    # ── Attachments (demo — pointing to placeholder paths) ─────────────────
    attachments = [
        Attachment(
            consultation_id=consultations_data[0].id,
            file_name="cattle_nasal_discharge.jpg",
            file_type="photo",
            mime_type="image/jpeg",
            storage_path="/demo/attachments/cattle_nasal_discharge.jpg",
            file_size_bytes=245_000,
        ),
        Attachment(
            consultation_id=consultations_data[1].id,
            file_name="poultry_mortality_report.jpg",
            file_type="photo",
            mime_type="image/jpeg",
            storage_path="/demo/attachments/poultry_mortality_report.jpg",
            file_size_bytes=312_000,
        ),
        Attachment(
            consultation_id=consultations_data[1].id,
            file_name="field_audio_note.mp3",
            file_type="audio",
            mime_type="audio/mpeg",
            storage_path="/demo/attachments/field_audio_note.mp3",
            file_size_bytes=1_200_000,
        ),
        Attachment(
            consultation_id=consultations_data[3].id,
            file_name="udder_inspection.jpg",
            file_type="photo",
            mime_type="image/jpeg",
            storage_path="/demo/attachments/udder_inspection.jpg",
            file_size_bytes=198_000,
        ),
    ]
    for a in attachments:
        db.add(a)
    await db.flush()

    # ── Responses ──────────────────────────────────────────────────────────
    responses = [
        ConsultationResponse(
            consultation_id=consultations_data[3].id,
            doctor_id=doc_rahman.id,
            diagnosis=(
                "Subclinical mastitis and possible nutritional deficiency. "
                "Milk SCC likely elevated. Recommend California Mastitis Test."
            ),
            treatment_plan=(
                "1. Perform CMT on all 4 quarters immediately.\n"
                "2. Collect milk sample for culture and sensitivity.\n"
                "3. Supplement diet with vitamin E and selenium.\n"
                "4. Intramammary treatment if CMT positive (pending culture result)."
            ),
            medications="Vitamin E-Selenium injection (1 mL/50 kg SC). Pending culture for antibiotic selection.",
            follow_up_instructions="Reassess milk production in 7 days. Report CMT result within 48 hours.",
            is_emergency_referral=False,
        ),
        ConsultationResponse(
            consultation_id=consultations_data[5].id,
            doctor_id=doc_chowdhury.id,
            diagnosis=(
                "Bacterial haemorrhagic septicaemia consistent with Aeromonas hydrophila infection, "
                "aggravated by water quality deterioration post-rainfall."
            ),
            treatment_plan=(
                "1. Immediately apply lime (CaO) 50 kg/bigha to raise pH.\n"
                "2. Reduce feed quantity by 50% for 3 days.\n"
                "3. Add potassium permanganate (2-3 ppm) for water disinfection.\n"
                "4. Oxytetracycline bath treatment if mortality continues."
            ),
            medications="Potassium permanganate 2 ppm. Oxytetracycline 5 g per 100L if required.",
            follow_up_instructions="Monitor DO levels daily. Report mortality counts each morning.",
            is_emergency_referral=False,
        ),
        ConsultationResponse(
            consultation_id=consultations_data[6].id,
            doctor_id=doc_hossain.id,
            diagnosis=(
                "Suspected Haemorrhagic Septicaemia (HS) caused by Pasteurella multocida. "
                "Notifiable disease — local authority must be informed."
            ),
            treatment_plan=(
                "1. IMMEDIATE ISOLATION of all cattle in the herd.\n"
                "2. Administer Oxytetracycline LA 20 mg/kg IM stat.\n"
                "3. Notify Upazila Livestock Officer urgently.\n"
                "4. Emergency HS vaccination for all exposed animals.\n"
                "5. Do NOT move animals off premises."
            ),
            medications=(
                "Oxytetracycline LA 20% — 9 mL/100 kg IM once. "
                "Anti-inflammatory: Flunixin meglumine 2 mg/kg IV once."
            ),
            follow_up_instructions=(
                "This is a notifiable disease. Field worker must contact Upazila Livestock Office "
                "immediately. Follow-up visit required within 24 hours."
            ),
            is_emergency_referral=True,
        ),
    ]
    for r in responses:
        db.add(r)
    await db.flush()

    # ── Notifications ──────────────────────────────────────────────────────
    notifications = [
        Notification(
            user_id=dr_rahman.id,
            consultation_id=consultations_data[0].id,
            title="New Urgent Consultation",
            body="Case AISP-2024-0001 requires your attention within 1 hour.",
            notification_type="new_case",
            is_read=False,
        ),
        Notification(
            user_id=dr_begum.id,
            consultation_id=consultations_data[1].id,
            title="⚠️ Emergency Case",
            body="Emergency poultry mortality reported in Chittagong Port zone.",
            notification_type="emergency",
            is_read=False,
        ),
        Notification(
            user_id=dr_chowdhury.id,
            consultation_id=consultations_data[4].id,
            title="SLA Overdue",
            body="Consultation AISP-2024-0005 passed its SLA deadline 2 hours ago.",
            notification_type="overdue",
            is_read=False,
        ),
        Notification(
            user_id=dr_rahman.id,
            consultation_id=consultations_data[3].id,
            title="Response Confirmed",
            body="Your response for AISP-2024-0004 was delivered successfully.",
            notification_type="info",
            is_read=True,
        ),
    ]
    for n in notifications:
        db.add(n)

    await db.commit()


if __name__ == "__main__":
    async def main() -> None:
        from app.db.session import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            await seed(db)
        print("✓ Demo data seeded successfully.")

    asyncio.run(main())
