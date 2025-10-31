import frappe

def has_app(appname: str) -> bool:
    try:
        return appname in frappe.get_installed_apps()
    except Exception:
        return False
