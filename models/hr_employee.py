
from datetime import datetime, timedelta, date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    allowed_loan_limit = fields.Float(string='Allowed Loan Limit')
    total_loan_amount = fields.Float(compute='get_total_loan_amount')
    loans = fields.One2many('employee.loans','employee_id',domain=[('state','=','confirmed')])





    def get_total_loan_amount(self):
        for rec in self:
          loans = rec.env['employee.loans'].search([('employee_id','=',self.id),('state','=','confirmed')])
          if loans:
              for loan in loans:
                  rec.total_loan_amount += loan.amount
                  rec.loans =[(4,loan.id)]
          else:
              rec.total_loan_amount =0
