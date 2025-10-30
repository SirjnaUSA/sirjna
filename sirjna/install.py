
import frappe
def after_install():
    for r in ["Udaan Student", "Mentor", "Website Manager", "Program Manager"]:
        if not frappe.db.exists("Role", r):
            role = frappe.new_doc("Role")
            role.role_name = r
            role.save()
    if frappe.db.exists("DocType", "Sirjna Settings") and not frappe.db.exists("Sirjna Settings"):
        s = frappe.new_doc("Sirjna Settings")
        s.brand_primary = "#0A2342"
        s.brand_accent = "#D4AF37"
        s.brand_bg = "#FFFFFF"
        s.portal_banner_text = "Welcome to Udaan - your guided path to US/Canada engineering programs."
        s.insert(ignore_permissions=True)
    try:
        ps = frappe.get_single("Portal Settings")
        ps.default_portal_home = "/portal"
        ps.allow_guest = 0
        ps.allow_signup = 0
        ps.save()
    except Exception:
        pass
    if "wiki" in frappe.get_installed_apps():
        if not frappe.db.exists("Wiki Page", "Udaan Knowledge Base"):
            page = frappe.new_doc("Wiki Page")
            page.title = "Udaan Knowledge Base"
            page.route = "kb"
            page.content = "Welcome to the Udaan Knowledge Base."
            page.published = 1
            page.insert(ignore_permissions=True)
