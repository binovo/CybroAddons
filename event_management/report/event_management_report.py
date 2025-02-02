# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ReportHotelManagement(models.AbstractModel):
    """Class for fetch and carry off pdf data to template"""
    _name = "report.event_management.report_event_management"
    _description = "Event Management Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """ Gets report values """
        form_data = data['form']
        where = '1=1'
        if form_data['date_from'] and form_data['date_to'] \
                and form_data['date_from'] > form_data['date_to']:
            raise ValidationError(_('From Date must be less than To Date'))
        if form_data["partner_id"]:
            where += f"""AND e.partner_id = '{form_data['partner_id'][0]}'"""
        if form_data['date_from']:
            where += f"""AND e.date>='{form_data['date_from']}'"""
        if form_data['date_to']:
            where += f"""AND e.date <= '{form_data['date_to']}'"""
        if form_data['type_event_ids']:
            event_list = data['event_types']
            event_ids = f"({event_list[0]})" if len(event_list) == 1 else tuple(
                event_list)
            where += f"""AND e.type_of_event_id IN {event_ids}"""
        if form_data['event_state']:
            where += f"""AND e.state = '{form_data['event_state']}'"""
        self.env.cr.execute(f"""
                SELECT e.name as event, t.name as type, r.name as partner, 
                e.state, e.date,
                e.start_date, e.end_date
                from event_management e inner join 
                res_partner r on e.partner_id = r.id
                inner join event_management_type t on 
                e.type_of_event_id = t.id
                where {where} order by e.date""")
        return {
            'docs': self.env.cr.dictfetchall(),
            'docs2': form_data,
            'today_date': fields.Datetime.now()
        }
