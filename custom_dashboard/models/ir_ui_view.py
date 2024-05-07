from odoo import fields, models

class ViewCustom(models.Model):
    _inherit = 'ir.ui.view.custom'

    user_ids = fields.Many2many('res.users', ondelete='cascade')
