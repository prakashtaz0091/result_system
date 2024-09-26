from django.db import models
from nepalicalendar import NepDate
from datetime import date


class NepaliDateField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10  # adjust the max length as needed
        super(NepaliDateField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """Convert the date from the database (AD) to Nepali date (BS)."""
        if value is None:
            return value
        try:
            return NepDate.from_ad(value)
        except Exception:
            return value

    def to_python(self, value):
        """Convert the value to a Nepali date when loading from the database or input."""
        if isinstance(value, NepDate):
            return value
        if value is None:
            return value
        try:
            return NepDate.from_ad(value)
        except Exception:
            return value

    def get_prep_value(self, value):
        """Convert Nepali date (BS) to Gregorian (AD) before saving to the database."""
        if value is None:
            return None  # Ensure None values are handled
        if isinstance(value, NepDate):
            return value.ad  # NepDate instance has `ad` property (which is a Python `date` object)
        if isinstance(value, date):
            return value  # If it's already a date object (Gregorian date)
        return value
