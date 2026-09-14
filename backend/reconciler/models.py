from django.db import models


class Location(models.Model):
    location_id = models.CharField(max_length=50, unique=True)
    org_id = models.CharField(max_length=50)
    location_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.location_id} - {self.location_name}"


class SystemARecord(models.Model):
    record_id = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    event_date = models.CharField(max_length=100, blank=True)
    category_code = models.CharField(max_length=100, blank=True)
    actor_id = models.CharField(max_length=100, blank=True)
    base_value = models.CharField(max_length=100, blank=True)
    adjustment = models.CharField(max_length=100, blank=True)
    total_value = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.record_id


class SystemBEntry(models.Model):
    entry_id = models.CharField(max_length=100, unique=True)
    record_ref = models.CharField(max_length=100, blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    recorded_on = models.CharField(max_length=100, blank=True)
    value = models.CharField(max_length=100, blank=True)
    label = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.entry_id
        