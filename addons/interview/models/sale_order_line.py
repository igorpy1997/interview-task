# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    width = fields.Float(
        string='Width (cm)',
        digits=(10, 2),
        help='Width in centimeters'
    )
    height = fields.Float(
        string='Height (cm)',
        digits=(10, 2),
        help='Height in centimeters'
    )
    square_meters = fields.Float(
        string='Square Meters',
        compute='_compute_square_meters',
        store=True,
        digits=(10, 4),
        help='Calculated area in square meters based on width and height'
    )

    @api.depends('width', 'height')
    def _compute_square_meters(self):
        """Calculate square meters from width and height in centimeters"""
        for line in self:
            if line.width and line.height:
                # Convert from cm² to m² (divide by 10000)
                line.square_meters = (line.width * line.height) / 10000
            else:
                line.square_meters = 0.0

    @api.constrains('width', 'height')
    def _check_dimensions_positive(self):
        """Ensure width and height are positive values"""
        for line in self:
            if line.width < 0:
                raise ValidationError('Width must be a positive value.')
            if line.height < 0:
                raise ValidationError('Height must be a positive value.')
