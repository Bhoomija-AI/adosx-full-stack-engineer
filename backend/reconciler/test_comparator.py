from django.test import TestCase

from reconciler.models import Location, SystemARecord, SystemBEntry
from reconciler.services.comparator import compare_records


class ComparatorTests(TestCase):

    def setUp(self):
        self.location = Location.objects.create(
            location_id="LOC1",
            org_id="ORG1",
            location_name="Test Location",
        )

    def test_missing_in_system_b(self):
        SystemARecord.objects.create(
            record_id="REC001",
            location=self.location,
            total_value="100",
        )

        discrepancies = compare_records()

        self.assertTrue(
            any(d.reason == "MISSING_IN_SYSTEM_B" for d in discrepancies)
        )

    def test_orphan_in_system_b(self):
        SystemBEntry.objects.create(
            entry_id="ENTRY001",
            record_ref="REC999",
            location=self.location,
            value="100",
        )

        discrepancies = compare_records()

        self.assertTrue(
            any(d.reason == "ORPHAN_IN_SYSTEM_B" for d in discrepancies)
        )

    def test_duplicate_in_system_b(self):
        SystemARecord.objects.create(
            record_id="REC001",
            location=self.location,
            total_value="100",
        )

        SystemBEntry.objects.create(
            entry_id="ENTRY001",
            record_ref="REC001",
            location=self.location,
            value="100",
        )

        SystemBEntry.objects.create(
            entry_id="ENTRY002",
            record_ref="REC001",
            location=self.location,
            value="100",
        )

        discrepancies = compare_records()

        self.assertTrue(
            any(d.reason == "DUPLICATE_IN_SYSTEM_B" for d in discrepancies)
        )

    def test_value_mismatch(self):
        SystemARecord.objects.create(
            record_id="REC001",
            location=self.location,
            total_value="100",
        )

        SystemBEntry.objects.create(
            entry_id="ENTRY001",
            record_ref="REC001",
            location=self.location,
            value="150",
        )

        discrepancies = compare_records()

        self.assertTrue(
            any(d.reason == "VALUE_MISMATCH" for d in discrepancies)
        )
