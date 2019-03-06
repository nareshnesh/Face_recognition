    # -*- coding: utf-8 -*-
# Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
# Copyright (C) 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DbsAtmProjectExtn(models.Model):
    _inherit = "project.project"

    floor_area = fields.Char(string="Floor Area")
    project_pc_code = fields.Char(string="Project PC Code")
    ownership =  fields.Selection([
        ('owned','Owned'),                   
        ('leased', 'Leased'),
        
       ], 
        string='Ownership')
    tenure = fields.Char(string="Tenure")
    cresa_program_lead = fields.Many2one('res.users', string='CRESA Program Lead (Cresa PMO)')
    cbg_coo_oic= fields.Many2one('res.users', string='CBG COO OIC')
    pi_lead1 = fields.Many2one('res.users', string='PI-1 Lead')
    pi_lead2 = fields.Many2one('res.users', string='PI-2 Lead')
    
    program_management_office = fields.Many2one('res.users', string='Program Management Office (PMO)')
    project_management_lead = fields.Many2one('res.users', string='Project Management Lead (PML)')
    project_manager = fields.Many2one('res.users', string='Project Manager (PM)', width="50%")
    interior_designer = fields.Many2one('res.users', string='Interior Designer (ID)')
    mep_consultant = fields.Many2one('res.users', string='MEP Consultant (MEP)')
    qualified_person_archi = fields.Many2one('res.users', string='Qualified Person (Archi)')
    qualified_person_structural = fields.Many2one('res.users', string='Qualified Person (Structural)',width="50%")
    consultant1 = fields.Many2one('res.users', string='Consultant 1 (for initial Test-fit)')
    consultant2 = fields.Many2one('res.users', string='Consultant 2')
    consultant3 = fields.Many2one('res.users', string='Consultant 3')
    consultant4 = fields.Many2one('res.users', string='Consultant 4')
    parent_id = fields.Many2one('project.task', string='Parent Task', 
            index=True, domain="[('parent_id','=', parent_id)]", Invisible=True)
    
    
    
    main_contractor = fields.Many2one('res.users', string='Main Contractor: Tarkus')
    mep_contractor = fields.Many2one('res.users', string='MEP Contractor')
    supplier = fields.Many2many('res.partner',string="Vendors") 
    is_a_project_template = fields.Boolean(string="Is a Template Project") 
    
    name = fields.Char("Name", index=True, required=True, track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='Project Manager')
    privacy_visibility = fields.Selection([
            ('followers', 'On invitation only'),
            ('employees', 'Visible by all employees'),
            ('portal', 'Visible by following customers'),
        ],
        string='Privacy',
        default='portal',
        help="Holds visibility of the tasks or issues that belong to the current project:\n"
                "- On invitation only: Employees may only see the followed project, tasks or issues\n"
                "- Visible by all employees: Employees may see all project, tasks or issues\n"
                "- Visible by following customers: employees see everything;\n"
                "   if website is activated, portal users may see project, tasks or issues followed by\n"
                "   them or by someone of their company\n")

    

    @api.multi
    def template_override(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
#             default['name'] =("%s (copy)") % (self.name)
#             del default["lang"]
#             del default["uid"]
#             print(default,'defaulttttt')
            default['is_a_project_template']=False
            print(default,'defaulttttt')
        
#         project = super(DbsAtmProjectExtn, self).copy(default)
	new_pro=self.env['project.project']
        for rec in self:
            pro_vals = {
                 'name': rec.name+'copy',
                 'floor_area': rec.floor_area,
                 'interior_designer': rec.interior_designer.id,
                'project_pc_code': rec.project_pc_code,
                 'ownership': rec.ownership,
                 'tenure': rec.tenure,
                 'cresa_program_lead': rec.cresa_program_lead.id,
                 'pi_lead1': rec.pi_lead1.id,
                 'pi_lead2': rec.pi_lead2.id,
                 'program_management_office': rec.program_management_office.id,
                 'project_management_lead': rec.project_management_lead.id,
                 'mep_consultant': rec.mep_consultant.id,
                 'qualified_person_archi': rec.qualified_person_archi.id,
                 'qualified_person_structural': rec.qualified_person_structural.id,
                 'consultant1': rec.consultant1.id,
                 'consultant2': rec.consultant2.id,
                 'consultant3': rec.consultant3.id,
                 'consultant4': rec.consultant4.id,
                 'main_contractor': rec.main_contractor.id,
                 'mep_contractor': rec.mep_contractor.id,
                 'mep_contractor': rec.mep_contractor.id,
                 'analytic_account_id': rec.analytic_account_id.id,
                 'supplier': rec.supplier.id,
                 'sequence': rec.sequence,
                 'resource_calendar_id': rec.resource_calendar_id.id,

            }
            new_pro = self.env['project.project'].create(pro_vals)
            
            task_rec = self.env['project.task'].search([('project_id', '=', rec.id)])
                
            for task in task_rec:
                task_vals = {
                   'project_id': new_pro.id,
                   'name': task.name,
                   'budgeted_cost': task.budgeted_cost,
                   'parent_id': task.parent_id.id,
                   'assigned_torole': task.assigned_torole.id,
                   'user_id': task.user_id.id,
                   'work_assigned': task.work_assigned.id,
                   'planned_work': task.planned_work,
                   'actual_work': task.actual_work,
                   'work_variance': task.work_variance,
                   'variance': task.variance,
                   'is_paid': task.is_paid,
                   'complete': task.complete,
                   'actual_cost': task.actual_cost,
                   'budget_variance': task.budget_variance,
                   'plan_start': task.plan_start,
                   'plan_finish': task.plan_finish,
                   'duration': task.duration,
                   'actual_finish': task.actual_finish,
                   'tag_ids': task.tag_ids,
                   'timesheet_ids': task.timesheet_ids,
                   'planned_hours': task.planned_hours,
                   'subtask_planned_hours': task.subtask_planned_hours,
                   'progress': task.progress,
                   'sequence': task.sequence,
                    'email_from': task.email_from,
                    'email_cc': task.email_cc,
                    'displayed_image_id': task.displayed_image_id,
                    'progress': task.progress,
                    'date_assign': task.date_assign,
                    'date_last_stage_update': task.date_last_stage_update,
                    'working_hours_close': task.working_hours_close,
                    'working_days_close': task.working_days_close,
                    'description': task.description,
                     }

                new_task = self.env['project.task'].create(task_vals)
            
            
                info_recvalues = self.env['project.task.info'].search([('task_id', '=', task.id)])  
                new_task_rec = self.env['project.task'].search([('project_id', '=', new_pro.id)])
                timesheet_account = self.env['account.analytic.line'].search([('task_id', '=', task.id)])
                pred_rec = self.env['project.task.predecessor'].search([('task_id', '=', task.id)])
#                 analytic_account = self.env['account.analytic.account'].search([('task_id', '=', task.id)])
                new_parent=self.env['project.task.predecessor']
#                 for new_task in new_task_rec:
#                 print(new_parent,'NEW PARENTT')    
                    
                for predecessor_idrec in pred_rec:
                    
                    #for taskid in pred_rec:
                    #   if not taskid.parent_task_id:
                    #        new_parent=taskid    
                            
                    #for subtask in pred_rec:
                    #    if subtask.id!=new_parent.id:
                    #        subtask.write({'parent_task_id':new_parent.id})
                            
		    predecessor_vals = {

		    'lag_type': predecessor_idrec.lag_type,
		    'parent_task_id': predecessor_idrec.parent_task_id.id,
		    'task_id': new_task.id,
		    'type': predecessor_idrec.type,

		    }


		    predecessor_rec = self.env['project.task.predecessor'].create(predecessor_vals)
		    print(predecessor_vals,'predecessor_vals')     



#                                 print(subtask,'SUBBBB')
#                                 print(new_task_rec,'new_task_rec')

                    

#                     print(predecessor_vals,'predecessor_vals')     
#                 
        
                for item in info_recvalues:
                    info_vals = {
                        'name': item.name,
                        'start': item.start,    
                        'task_id':new_task.id,
                        'end': item.end,
                        'left_up': item.left_up,
                        'left_down': item.left_down,
                        'right_down': item.right_down,
                        'right_up': item.right_up,
                        'show': item.show,
                        
                        }
                    info_account = self.env['project.task.info'].create(info_vals)
	new_task_rec = self.env['project.task'].search([('project_id', '=', new_pro.id)])
	for taskid in new_task_rec:
	   if not taskid.parent_task_id:
              new_parent=taskid    
                            
        for subtask in new_task_rec:
           if subtask.id!=new_parent.id:
              subtask.write({'parent_task_id':new_parent.id})
#                     print(info_vals,'info_vals')     
                    
#                 for timesheet in timesheet_account:
#                     timesheet_vals = {
#                                 
#                         'date': timesheet.date,
#                         'employee_id': timesheet.employee_id.id,
#                         'name': timesheet.name,
#                         'task_id': new_task.id,
#                         'account_id': timesheet.account_id.id, 
# #                         'product_uom_id': timesheet.product_uom_id.id,
# #                             'unit_amount': unit_amount.name,
#                         }
#                       
#                     timesheet_account_value = self.env['account.analytic.line'].create(timesheet_vals)
# #                     analytic_account_value = self.env['account.analytic.line'].create(acc_vals)
#                     print('timesheet_vals',timesheet_vals)
#                    




# 
#      
#                 timesheet_rec = self.env['project.task'].search([('project_id', '=', new_pro.id)])
#                 print('timesheet_rec',timesheet_rec)
#                 timesheet_account = self.env['account.analytic.line'].search([('task_id', '=', task.id)])                     
#                 print('timesheet_account',timesheet_account)
#                 for tm in timesheet_rec:
#                     for timesheet in timesheet_account:
#                         timesheet_vals = {
#                                 
#                             'date': timesheet.date,
#                             'employee_id': timesheet.employee_id.id,
#                             'name': timesheet.name,
#                             'task_id': tm.id,
#                              'account_id': timesheet.account_id.id,
# #                             'unit_amount': unit_amount.name,
#                                 
#                             }
#                         print('timesheet_vals',timesheet_vals)
#                         timesheet_account_value = self.env['account.analytic.line'].create(timesheet_vals)


            
#                 info_rec = self.env['project.task'].search([('project_id', '=', new_pro.id)])
#                 info_recvalues = self.env['project.task.info'].search([('task_id', '=', task.id)])
#                 for infos in info_rec:
#                     for item in info_recvalues:
#                         info_vals = {
#                             'name': item.name,
#                             'start': item.start,    
#                             'task_id': infos.id,
#                             'end': item.end,
#                             'left_up': item.left_up,
#                             'left_down': item.left_down,
#                             'right_down': item.right_down,
#                             'right_up': item.right_up,
#                             'show': item.show,
#                             
#                             }
#                         info_account = self.env['project.task.info'].create(info_vals)
#                         print(info_vals,'info_vals')     


        #parenttask subtask
        
        tasks = self.env['project.task'].search([('project_id','=',new_pro.id)])
        new_parent=self.env['project.task']
        
        for taskid in tasks:
            if not taskid.parent_id:
                new_parent=taskid    
                
            
        for subtask in tasks:
            if subtask.id!=new_parent.id:
                subtask.write({'parent_id':new_parent.id})
#          
#          
#         for follower in self.message_follower_ids:
#             project.message_subscribe(partner_ids=follower.partner_id.ids, subtype_ids=follower.subtype_ids.ids)
# #         if 'tasks' not in default:
# #             self.map_tasks(project.id)
#         return DbsAtmProjectExtn
#          
#         if default_plannedhours is None:
#             default_plannedhours = {}
#         if not default_plannedhours.get('planned_hours'):
#             default_plannedhours['planned_hours'] =("%s (copy)") % (self.planned_hours)
#              
#             default_plannedhours['is_a_project_template']=False
#              
#          
#         if default_email_cc is None:
#             default_email_cc = {}
#         if not default_email_cc.get('email_cc'):
#             default_email_cc['email_cc'] =("%s (copy)") % (self.email_cc)
#             print(default_email_cc,'email_cc')
#             default_email_cc['is_a_project_template']=False
#             print(default_email_cc,'email_cc')
#  
#         if default_progress is None:
#             default_progress = {}
#         if not default_progress.get('progress'):
#             default_progress['progress'] =("%s (copy)") % (self.progress)
#              
#             default_progress['is_a_project_template']=False
#             
#         
#         if default_description is None:
#             default_description = {}
#         if not default_description.get('description'):
#             default_description['description'] =("%s (copy)") % (self.description)
#              
#             default_description['is_a_project_template']=False
#              
#             print(project.name,'projctnameeee')
