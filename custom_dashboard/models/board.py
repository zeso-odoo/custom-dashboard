from odoo import api, models

class Board(models.AbstractModel):
    _inherit = 'board.board'

    
    @api.model
    def get_view(self,view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        team_leader_id = self.env.uid
        sales_teams = self.env['crm.team'].search([('user_id', '=', team_leader_id)])
        print('sales team : ',sales_teams)
        user_list = set()
        for i in sales_teams:
            for j in i.member_ids.ids:
                user_list.add(j)
        user_list = list(user_list)
        
        print(user_list)

        # print(team_leader_id)
        # team_member_id = self.env['res.users'].search([('','=', self.env.uid)]).id
        # # print('************',team_member_id)
        custom_view = self.env['ir.ui.view.custom'].sudo().search(['|', ('user_id', '=', self.env.uid), ('user_ids', 'in' , [[sales_teams]]), ('ref_id', '=', view_id)], limit=1)
        print(custom_view, len(custom_view), 'kkkkkkkkkk')
        # custom_view = []
        # for i in custom_view1:
        #     print(i.id)
        #     print(i.user_ids)
        #     if 6 in i.user_ids.ids:
        #         custom_view.append(i)
        # print(custom_view)
        if custom_view:
            res.update({'custom_view_id': custom_view.id,
                        'arch': custom_view.arch})
            res['arch'] = self._arch_preprocessing(res['arch'])
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