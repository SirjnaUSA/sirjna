
import frappe
def sirjna_settings():
    try:
        return {
            "stripe_payment_link": frappe.db.get_single_value("Sirjna Settings", "stripe_payment_link"),
            "calendly_url": frappe.db.get_single_value("Sirjna Settings", "calendly_url"),
            "tally_intake_url": frappe.db.get_single_value("Sirjna Settings", "tally_intake_url"),
            "ga4_measurement_id": frappe.db.get_single_value("Sirjna Settings", "ga4_measurement_id"),
            "support_email": frappe.db.get_single_value("Sirjna Settings", "support_email"),
            "support_phone": frappe.db.get_single_value("Sirjna Settings", "support_phone"),
        }
    except Exception:
        return {}
def user_has_paid():
    try:
        if frappe.session.user == "Guest":
            return False
        return bool(frappe.get_all("Udaan Order", filters={"owner": frappe.session.user, "status": "Paid"}, limit=1))
    except Exception:
        return False
