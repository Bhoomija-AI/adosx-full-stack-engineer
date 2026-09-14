import csv
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from reconciler.models import Location, SystemARecord, SystemBEntry


def normalize_reference(value):
    if not value:
        return ""

    value = re.sub(r"[^a-zA-Z0-9]", "", str(value)).lower()

    if value.startswith("rec"):
        value = value[3:]

    return value


def safe_parse_decimal(value):
    if value is None:
        return None

    value = str(value).strip()

    if not value or value.upper() in {"N/A", "NA", "NULL", "NONE", "-"}:
        return None

    value = value.replace(",", "")
    value = re.sub(r"[₹$€£]", "", value).strip()

    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


class Command(BaseCommand):
    help = "Import reconciliation CSV data into the database."

    def handle(self, *args, **options):
        data_dir = Path(settings.BASE_DIR).parent / "data"

        locations_file = data_dir / "locations.csv"
        system_a_file = data_dir / "system_a.csv"
        system_b_file = data_dir / "system_b.csv"

        self.stdout.write("Starting data import...")

        self.import_locations(locations_file)
        self.import_system_a(system_a_file)
        self.import_system_b(system_b_file)

        self.stdout.write(
            self.style.SUCCESS("Data import completed successfully.")
        )

    def import_locations(self, file_path):
        count = 0

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                Location.objects.update_or_create(
                    location_id=row["location_id"].strip(),
                    defaults={
                        "org_id": row["org_id"].strip(),
                        "location_name": row["location_name"].strip(),
                    },
                )
                count += 1

        self.stdout.write(f"Locations imported: {count}")

    def import_system_a(self, file_path):
        count = 0

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                location = Location.objects.filter(
                    location_id=row.get("location_id", "").strip()
                ).first()

                SystemARecord.objects.update_or_create(
                    record_id=row["record_id"].strip(),
                    defaults={
                        "location": location,
                        "event_date": row.get("event_date", "").strip(),
                        "category_code": row.get("category_code", "").strip(),
                        "actor_id": row.get("actor_id", "").strip(),
                        "base_value": row.get("base_value", "").strip(),
                        "adjustment": row.get("adjustment", "").strip(),
                        "total_value": row.get("total_value", "").strip(),
                        "state": row.get("state", "").strip(),
                    },
                )

                count += 1

        self.stdout.write(f"System A records imported: {count}")

    def import_system_b(self, file_path):
        count = 0

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                location = Location.objects.filter(
                    location_id=row.get("location_id", "").strip()
                ).first()

                SystemBEntry.objects.update_or_create(
                    entry_id=row["entry_id"].strip(),
                    defaults={
                        "record_ref": row.get("record_ref", "").strip(),
                        "location": location,
                        "recorded_on": row.get("recorded_on", "").strip(),
                        "value": row.get("value", "").strip(),
                        "label": row.get("label", "").strip(),
                    },
                )

                count += 1

        self.stdout.write(f"System B entries imported: {count}")
        