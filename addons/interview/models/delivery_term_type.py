
from calendar import monthrange
from datetime import datetime, timedelta

from odoo import api, fields, models


class DeliveryTermType(models.Model):
    _name = 'delivery.term.type'
    _description = 'Delivery Term Type'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        help='Delivery term name (e.g., "За три дня", "За неделю")'
    )

    term_type = fields.Selection([
        ('days', 'Days from today'),
        ('last_day_month', 'Last day of current month'),
        ('next_monday', 'Next Monday'),
        ('custom', 'Custom calculation')
    ], string='Term Type', required=True, default='days')

    days_offset = fields.Integer(
        string='Days Offset',
        default=1,
        help='Number of days to add from today (for days type)'
    )

    active = fields.Boolean(string='Active', default=True)

    def calculate_delivery_date(self, base_date=None):
        """Calculate delivery date based on term type"""
        if not base_date:
            base_date = datetime.now().date()

        if self.term_type == 'days':
            return base_date + timedelta(days=self.days_offset)

        if self.term_type == 'last_day_month':
            year = base_date.year
            month = base_date.month
            last_day = monthrange(year, month)[1]
            return base_date.replace(day=last_day)

        if self.term_type == 'next_monday':
            # Find next Monday (weekday 0 = Monday)
            days_until_monday = (7 - base_date.weekday()) % 7
            if days_until_monday == 0:  # If today is Monday, get next Monday
                days_until_monday = 7
            return base_date + timedelta(days=days_until_monday)

        # custom
        return base_date + timedelta(days=1)  # Default fallback


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_term_type_id = fields.Many2one(
        'delivery.term.type',
        string='Delivery Term Type',
        help='Select delivery term type'
    )

    delivery_date = fields.Date(
        string='Delivery Date',
        compute='_compute_delivery_date',
        store=True,
        readonly=True,
        help='Automatically calculated delivery date'
    )

    @api.depends('delivery_term_type_id')
    def _compute_delivery_date(self):
        """Compute delivery date based on selected term type"""
        for order in self:
            if order.delivery_term_type_id:
                order.delivery_date = order.delivery_term_type_id.calculate_delivery_date()
            else:
                order.delivery_date = False

    def recalculate_delivery_date(self):
        """Recalculate delivery date for cron job"""
        for order in self:
            if order.delivery_term_type_id and order.state in ['draft', 'sent']:
                order.delivery_date = order.delivery_term_type_id.calculate_delivery_date()
