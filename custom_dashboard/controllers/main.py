
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree as ElementTree
from odoo.addons.board.controllers import main
from odoo.http import route, request


class Board(main.Board):

    @route('/custom_dashboard/add_to_deaprtment_dashboard', type='json', auth='user')
    def add_to_deaprtment_dashboard(self, action_id, context_to_save, domain, view_mode, name=''):
        # Retrieve the 'My Dashboard' action from its xmlid
        action = request.env.ref('custom_dashboard.open_custom_dashboard_dash_action').sudo()
        # team_member_id = self.env['res.users'].search([('user_id','=', self.env.uid)]).id
        
        if action and action['res_model'] == 'board.board' and action['views'][0][1] == 'form' and action_id:
            # Maybe should check the content instead of model board.board ?
            view_id = action['views'][0][0]
            board_view = request.env['ir.ui.view.custom'].get_view(view_id, 'form')
            if board_view and 'arch' in board_view:
                board_arch = ElementTree.fromstring(board_view['arch'])
                column = board_arch.find('./board/column')
                if column is not None:
                    # We don't want to save allowed_company_ids
                    # Otherwise on dashboard, the multi-company widget does not filter the records
                    if 'allowed_company_ids' in context_to_save:
                        context_to_save.pop('allowed_company_ids')
                    new_action = ElementTree.Element('action', {
                        'name': str(action_id),
                        'string': name,
                        'view_mode': view_mode,
                        'context': str(context_to_save),
                        'domain': str(domain)
                    })
                    column.insert(0, new_action)
                    arch = ElementTree.tostring(board_arch, encoding='unicode')

                    team_leader_id = request.env.uid
                    sales_teams = request.env['crm.team'].search([('user_id', '=', team_leader_id)])
                    print('sales team : ',sales_teams)
                    user_list = set()
                    for i in sales_teams:
                        for j in i.member_ids.ids:
                            user_list.add(j)
                    user_list = list(user_list)
                    print(user_list, 'testingggggggggggg')
                    
                    request.env['ir.ui.view.custom'].sudo().create({
                        'user_id': request.session.uid,
                        'user_ids': [(6, 0, user_list)],
                        'ref_id': view_id,
                        'arch': arch
                    })
                    return True

        return False
