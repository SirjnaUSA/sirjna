import frappe
from frappe.utils import format_datetime
@frappe.whitelist()
def get_slots(date=None):
    filters = {"status": "Available"}
    if date:
        filters.update({ "start": (">=", f"{date} 00:00:00"), "end": ("<=", f"{date} 23:59:59") })
    slots = frappe.get_all(
        "Sirjna Appointment Slot",
        filters=filters,
        fields=["name", "start", "end", "appointment_type", "status"],
        order_by="start asc"
    )
    for s in slots:
        s["start_fmt"] = format_datetime(s["start"], "hh:mm a, MMM d")
        s["end_fmt"] = format_datetime(s["end"], "hh:mm a")
    return slots
@frappe.whitelist()
def book_slot(slot, full_name, email, phone=None):
    slot_doc = frappe.get_doc("Sirjna Appointment Slot", slot)
    if slot_doc.status != "Available":
        frappe.throw("This slot is no longer available.")
    atype = slot_doc.appointment_type
    appt = frappe.get_doc({
        "doctype": "Sirjna Appointment",
        "appointment_type": atype,
        "slot": slot_doc.name,
        "full_name": full_name,
        "email": email,
        "phone": phone or "",
        "status": "Booked",
        "provider": "None"
    }).insert(ignore_permissions=True)
    if (slot_doc.capacity or 1) <= 1:
        slot_doc.status = "Full"
    slot_doc.booked_count = (slot_doc.booked_count or 0) + 1
    slot_doc.save(ignore_permissions=True)
    return {"appointment": appt.name}