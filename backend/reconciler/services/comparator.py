from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re

from reconciler.models import SystemARecord, SystemBEntry


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


@dataclass
class Discrepancy:
    reason: str
    record_id: str
    location_id: str
    org_id: str
    value_a: str | None
    value_b: str | None


def compare_records():
    discrepancies = []

    system_a_records = list(
        SystemARecord.objects.select_related("location").all()
    )

    system_b_entries = list(
        SystemBEntry.objects.select_related("location").all()
    )

    b_by_reference = defaultdict(list)

    for entry in system_b_entries:
        normalized_ref = normalize_reference(entry.record_ref)

        if normalized_ref:
            b_by_reference[normalized_ref].append(entry)

    a_references = set()

    for record in system_a_records:
        normalized_id = normalize_reference(record.record_id)
        a_references.add(normalized_id)

        location_id = record.location.location_id if record.location else ""
        org_id = record.location.org_id if record.location else ""

        matching_entries = b_by_reference.get(normalized_id, [])

        if not matching_entries:
            discrepancies.append(
                Discrepancy(
                    reason="MISSING_IN_SYSTEM_B",
                    record_id=record.record_id,
                    location_id=location_id,
                    org_id=org_id,
                    value_a=record.total_value,
                    value_b=None,
                )
            )
            continue

        if len(matching_entries) > 1:
            for entry in matching_entries:
                discrepancies.append(
                    Discrepancy(
                        reason="DUPLICATE_IN_SYSTEM_B",
                        record_id=record.record_id,
                        location_id=location_id,
                        org_id=org_id,
                        value_a=record.total_value,
                        value_b=entry.value,
                    )
                )
            continue

        entry = matching_entries[0]

        value_a = safe_parse_decimal(record.total_value)
        value_b = safe_parse_decimal(entry.value)

        if value_a != value_b:
            discrepancies.append(
                Discrepancy(
                    reason="VALUE_MISMATCH",
                    record_id=record.record_id,
                    location_id=location_id,
                    org_id=org_id,
                    value_a=record.total_value,
                    value_b=entry.value,
                )
            )

    for entry in system_b_entries:
        normalized_ref = normalize_reference(entry.record_ref)

        if normalized_ref not in a_references:
            location_id = entry.location.location_id if entry.location else ""
            org_id = entry.location.org_id if entry.location else ""

            discrepancies.append(
                Discrepancy(
                    reason="ORPHAN_IN_SYSTEM_B",
                    record_id=entry.record_ref,
                    location_id=location_id,
                    org_id=org_id,
                    value_a=None,
                    value_b=entry.value,
                )
            )

    return discrepancies
    