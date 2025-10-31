import frappe
from .app_registry import has_app

def ensure_insights_assets():
    if not has_app("insights"):
        return
    try:
        if not frappe.db.exists("Insights Dashboard", "Sirjna KPI"):
            frappe.get_doc({"doctype":"Insights Dashboard","dashboard_name":"Sirjna KPI"}).insert(ignore_permissions=True)
    except Exception:
        pass
