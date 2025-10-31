import frappe
from random import shuffle

@frappe.whitelist()
def generate_shortlist(student: str):
    try:
        unis = frappe.get_all("University Program",
                              fields=["name","risk_bucket","university","program_name"])
        safe = [u for u in unis if (u.get("risk_bucket") or "") == "Safe"]
        target = [u for u in unis if (u.get("risk_bucket") or "") == "Target"]
        reach = [u for u in unis if (u.get("risk_bucket") or "") == "Reach"]
        shuffle(safe); shuffle(target); shuffle(reach)
        chosen = (safe[:5] + target[:5] + reach[:5])
        if not chosen:
            frappe.throw("No University Program records to pick from.")
        sl = frappe.get_doc({"doctype":"Shortlist","student": student})
        sl.insert(ignore_permissions=True)
        for u in chosen:
            row = sl.append("entries", {})
            row.university_program = u["name"]
            row.tier = u["risk_bucket"]
            row.rationale = "Auto-generated; please review."
        sl.save()
        return sl.name
    except Exception as e:
        frappe.throw(f"Shortlist generation failed: {e}")
