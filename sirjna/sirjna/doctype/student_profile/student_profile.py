import frappe
from frappe.model.document import Document
class StudentProfile(Document):
    def before_insert(self):
        if not getattr(self,'user',None) and frappe.session.user:
            self.user = frappe.session.user
        if not getattr(self,'email',None) and frappe.session.user:
            self.email = frappe.db.get_value('User', frappe.session.user, 'email') or frappe.session.user