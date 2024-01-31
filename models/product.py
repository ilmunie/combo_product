# -*- coding: utf-8 -*-
from odoo import api, fields, models


class UomUom(models.Model):
    _inherit = "uom.uom"

    short_name = fields.Char(string="Nombre corto")

class ComboProduct(models.Model):
    _name = "product.combo"
    _description = "Product packs"

    @api.onchange('product_id')
    def product_id_name(self):
        self.name = self.product_id.display_name
    @api.onchange('product_id')
    def product_id_onchange(self):
        return {'domain': {'product_id': [('is_combo', '=', False)]}}

    name = fields.Char('name')
    product_template_id = fields.Many2one('product.template', 'Item')
    product_quantity = fields.Float('Quantity', default='1', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')
    price = fields.Float('Product_price')
    @api.model
    def name_get(self):
        res = []
        for rec in self:
            if rec.name:
                name = rec.name + ' (x' + str(rec.product_quantity) + ' ' + (rec.uom_id.short_name or rec.uom_id.name)+ ')'
            else:
                name = rec.product_id.display_name + ' (x' + str(rec.product_quantity) + ' ' + (rec.uom_id.short_name or rec.uom_id.name)+ ')'
            res.append((rec.id, name))
        return res

class ComboProductTemplate(models.Model):
    _inherit = "product.template"

    is_combo = fields.Boolean('Combo Product', default=False)
    combo_product_id = fields.One2many('product.combo', 'product_template_id', 'Combo Item')
    combo_prefix = fields.Char(default="Combo")
    no_update_name = fields.Boolean(string="No actualizar nombre")

    @api.onchange('combo_product_id','combo_product_id.product_id', 'combo_product_id.product_id', 'combo_product_id.product_quantity','combo_product_id.uom_id', 'combo_prefix')
    def compute_combo_product_name(self):
        for record in self:
            if record.combo_product_id and not record.no_update_name:
                name = record.combo_prefix + ": " + ' + '.join(record.combo_product_id.mapped('display_name'))
                record.name = name
