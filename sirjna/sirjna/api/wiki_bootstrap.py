import frappe
from .app_registry import has_app

def ensure_student_wiki():
    try:
        if not has_app("wiki"):
            return
        if not frappe.db.exists("Wiki Space", {"space":"sirjna-handbook"}):
            ws = frappe.get_doc({
                "doctype":"Wiki Space",
                "space":"sirjna-handbook",
                "title":"Sirjna Student Handbook",
                "public":1
            })
            ws.insert(ignore_permissions=True)
    except Exception:
        pass
