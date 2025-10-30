
import frappe
@frappe.whitelist()
def next_step():
    if frappe.session.user == "Guest":
        return "Login to start"
    doc = frappe.get_all("Application Step",
                         filters={"owner": frappe.session.user, "status":["!=", "Completed"]},
                         fields=["title"], order_by="creation asc", limit=1)
    return doc[0].get("title") if doc else "Complete your profile"
