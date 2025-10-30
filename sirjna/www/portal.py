
import frappe
def get_context(context):
    user = frappe.session.user
    profile = frappe.get_all("Student Profile", fields=["name","full_name"], filters={"user": user}, limit=1)
    steps = frappe.get_all("Application Step",
        fields=["name","title","status","due_date"],
        filters={"owner_user": user}, order_by="due_date asc", limit=5)
    total = frappe.db.count("Application Step", {"owner_user": user})
    completed = frappe.db.count("Application Step", {"owner_user": user, "status": "Completed"})
    progress = int((completed / total) * 100) if total else 0
    settings = frappe.get_single("Sirjna Settings")
    context.profile = profile[0] if profile else None
    context.steps = steps
    context.progress = progress
    context.banner = settings.portal_banner_text if settings else ""
    context.no_cache = 1
