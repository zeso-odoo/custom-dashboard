from odoo import api, models

class Board(models.AbstractModel):
    _inherit = 'board.board'

    
    @api.model
    def get_view(self,view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
            
        custom_view = self.env['ir.ui.view.custom'].sudo().search([('ref_id', '=', view_id)], limit=1)
        print('*************** ',custom_view)
        if custom_view and (custom_view.user_id.id == self.env.uid or (self.env.uid in custom_view.user_ids.ids)):
            res.update({'custom_view_id': custom_view.id,
                        'arch': custom_view.arch})
        res['arch'] = self._arch_preprocessing(res['arch'])
        print('*******res******',res)
        return res
    
    @api.model
    def _arch_preprocessing(self, arch):
        from lxml import etree

        def remove_unauthorized_children(node):
            for child in node.iterchildren():
                if child.tag == 'action' and child.get('invisible'):
                    node.remove(child)
                else:
                    remove_unauthorized_children(child)
            return node
        archnode = etree.fromstring(arch)
        archnode.set('js_class', 'board')
        return etree.tostring(remove_unauthorized_children(archnode), pretty_print=True, encoding='unicode')
    