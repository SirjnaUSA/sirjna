from frappe.model.document import Document
class DocumentInstance(Document):
    def before_insert(self):
        import frappe
        if not getattr(self,'owner_user',None) and frappe.session.user:
            self.owner_user = frappe.session.user
