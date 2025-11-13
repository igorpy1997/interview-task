# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_term_type_id = fields.Many2one(
        'delivery.term.type',
        string='Delivery Term Type',
        help='Select delivery term type to automatically calculate delivery date'
    )
    delivery_date = fields.Date(
        string='Delivery Date',
        compute='_compute_delivery_date',
        store=True,
        readonly=True,
        help='Automatically calculated delivery date based on selected term type'
    )

    @api.depends('delivery_term_type_id', 'date_order')
    def _compute_delivery_date(self):
        """Calculate delivery date based on delivery term type"""
        for order in self:
            if order.delivery_term_type_id:
                base_date = fields.Date.today()
                order.delivery_date = self.env['delivery.term.type'].calculate_delivery_date(
                    order.delivery_term_type_id.id,
                    base_date
                )
            else:
                order.delivery_date = False

    def recalculate_delivery_dates(self):
        """Recalculate delivery dates for non-confirmed orders

        This method is called by cron job to update delivery dates daily
        """
        non_confirmed_orders = self.search([
            ('state', 'in', ['draft', 'sent']),
            ('delivery_term_type_id', '!=', False)
        ])
        non_confirmed_orders._compute_delivery_date()
        return True
