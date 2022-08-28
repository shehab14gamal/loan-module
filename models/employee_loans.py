# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError


class EmployeeLoans(models.Model):
    _name = 'employee.loans'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee',domain=[('contract_ids.state','=','open')], required=1)
    # has_running_contract = fields.Boolean(compute='get_running_contracts')
    start_date = fields.Date(required=1)
    end_date = fields.Date()
    amount= fields.Float(string='Amount',required=1)
    state = fields.Selection([('draft','Draft'),
                               ('confirmed','Confirmed'),
                               ('ended','Ended'),
                               ('canceled','Canceled')],default='draft')
    last_change_status_by = fields.Many2one('res.users')


    @api.constrains('amount')
    def check_loan_limited_amount(self):
           employee = self.env['hr.employee'].search([('id','=',self.employee_id.id)])
           if self.amount + employee.total_loan_amount > employee.allowed_loan_limit:
               raise ValidationError("Sorry! total loan amount exceeded the allowed loan limit which equal "+str(employee.allowed_loan_limit))

    @api.onchange('start_date')
    def empty_end_date(self):
        self.end_date = ''


    def change_state(self):
        if self.state == 'draft':
            self.state = 'confirmed'
        elif self.state == 'confirmed':
            self.state = 'ended'
            self.end_date = datetime.today()
        self.last_change_status_by = self.env.user.id
    def cancel_state(self):
        self.state = 'canceled'
        self.last_change_status_by = self.env.user.id

    @api.constrains('end_date')
    def check_end_date(self):
        if self.end_date and self.state == 'confirmed':
            self.state = 'ended'
            self.last_change_status_by = self.env.user.id
        if self.end_date:
            if self.end_date < self.start_date:
               raise ValidationError("please! end date must be greate than or equal start date")


