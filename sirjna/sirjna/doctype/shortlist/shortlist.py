import frappe
from frappe.model.document import Document
class Shortlist(Document):
    def before_insert(self):
        if not getattr(self,'owner_user',None) and frappe.session.user:
            self.owner_user = frappe.session.user