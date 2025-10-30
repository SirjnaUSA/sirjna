
import frappe
WELCOME_SUBJECT = "Welcome to Udaan - your portal is ready"
WELCOME_BODY = "Hi {{ full_name or user }},\n\nYour payment is confirmed and your Udaan portal is ready.\n\nAccess it here: {{ base_url }}/portal\n\n- Sirjna Team"
def _assign_role(user, role_name="Udaan Student"):
    if not frappe.db.exists("User", user):
        return
    if not frappe.db.exists({"doctype":"Has Role","parent":user,"role":role_name}):
        ur = frappe.new_doc("Has Role")
        ur.role = role_name
        ur.parent = user
        ur.parenttype = "User"
        ur.parentfield = "roles"
        ur.insert(ignore_permissions=True)
def handle_payment_request_update(doc, method=None):
    if (doc.get("status") or "").lower() != "paid":
        return
    payer_email = (doc.get("email_to") or doc.get("party_email") or doc.get("contact_email") or "").strip()
    if not payer_email:
        return
    user = frappe.db.get_value("User", {"email": payer_email}) or payer_email
    _assign_role(user)
    try:
        base_url = frappe.utils.get_url()
        full_name = frappe.db.get_value("User", user, "full_name")
        body = frappe.render_template(WELCOME_BODY, {"full_name": full_name, "user": user, "base_url": base_url})
        frappe.sendmail(recipients=[payer_email], subject=WELCOME_SUBJECT, message=body)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Udaan Welcome Email Failed")
