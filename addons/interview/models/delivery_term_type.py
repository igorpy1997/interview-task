# -*- coding: utf-8 -*-

from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class DeliveryTermType(models.Model):
    _name = 'delivery.term.type'
    _description = 'Delivery Term Type'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        help='Delivery term type name (e.g., "In 3 days", "Next week")'
    )
    calculation_type = fields.Selection([
        ('days', 'Fixed Number of Days'),
        ('next_weekday', 'Next Specific Weekday'),
        ('end_of_month', 'End of Current Month'),
        ('end_of_next_month', 'End of Next Month'),
    ], string='Calculation Type', required=True, default='days',
       help='Method to calculate the delivery date')

    days_offset = fields.Integer(
        string='Days Offset',
        default=0,
        help='Number of days to add to current date (for "days" type)'
    )
    weekday = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Weekday',
       help='Target weekday (for "next_weekday" type)')

    @api.model
    def calculate_delivery_date(self, term_type_id, base_date=None):
        """Calculate delivery date based on term type configuration

        Args:
            term_type_id: ID of delivery.term.type record
            base_date: Base date for calculation (defaults to today)

        Returns:
            date: Calculated delivery date
        """
        if not term_type_id:
            return None

        term = self.browse(term_type_id)
        if not term.exists():
            return None

        if base_date is None:
            base_date = fields.Date.today()

        if term.calculation_type == 'days':
            return base_date + timedelta(days=term.days_offset)

        elif term.calculation_type == 'next_weekday':
            if not term.weekday:
                return None
            target_weekday = int(term.weekday)
            current_weekday = base_date.weekday()
            days_ahead = (target_weekday - current_weekday) % 7
            if days_ahead == 0:
                days_ahead = 7  # Next occurrence, not today
            return base_date + timedelta(days=days_ahead)

        elif term.calculation_type == 'end_of_month':
            # Last day of current month
            next_month = base_date + relativedelta(months=1)
            return next_month.replace(day=1) - timedelta(days=1)

        elif term.calculation_type == 'end_of_next_month':
            # Last day of next month
            next_month = base_date + relativedelta(months=2)
            return next_month.replace(day=1) - timedelta(days=1)

        return None
