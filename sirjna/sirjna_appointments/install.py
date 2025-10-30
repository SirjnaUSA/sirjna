
import frappe
from frappe.utils import add_to_date, now_datetime
def upsert(doctype, name=None, **kwargs):
    if name and frappe.db.exists(doctype, name):
        doc = frappe.get_doc(doctype, name)
        for k, v in kwargs.items():
            setattr(doc, k, v)
        doc.save(ignore_permissions=True)
        return doc
    doc = frappe.get_doc({"doctype": doctype, **kwargs})
    if name:
        doc.name = name
    doc.insert(ignore_permissions=True)
    return doc
def ensure_module_def():
    if not frappe.db.exists("Module Def", "Sirjna"):
        upsert("Module Def", "Sirjna", app_name="sirjna", module_name="Sirjna")
def ensure_roles():
    for role in ("Udaan Student", "Mentor"):
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)
def create_doctypes():
    if not frappe.db.exists("DocType", "Sirjna Zoom Settings"):
        upsert("DocType", name="Sirjna Zoom Settings", module="Sirjna", custom=1, is_single=1,
            fields=[{"fieldname":"api_token","fieldtype":"Password","label":"API Token"},
                    {"fieldname":"topic_prefix","fieldtype":"Data","label":"Topic Prefix","default":"Sirjna Advisory Call"}],
            permissions=[{"role":"System Manager","read":1,"write":1}])
    if not frappe.db.exists("DocType", "Sirjna Appointment Type"):
        upsert("DocType", name="Sirjna Appointment Type", module="Sirjna", custom=1,
            fields=[{"fieldname":"title","fieldtype":"Data","label":"Title","reqd":1},
                    {"fieldname":"duration","fieldtype":"Int","label":"Duration (minutes)","default":25},
                    {"fieldname":"active","fieldtype":"Check","label":"Active","default":1},
                    {"fieldname":"description","fieldtype":"Small Text","label":"Description"}],
            permissions=[{"role":"System Manager","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Mentor","read":1,"write":1,"create":1,"delete":1}])
    if not frappe.db.exists("DocType", "Sirjna Appointment Slot"):
        upsert("DocType", name="Sirjna Appointment Slot", module="Sirjna", custom=1,
            fields=[{"fieldname":"appointment_type","fieldtype":"Link","label":"Appointment Type","options":"Sirjna Appointment Type","reqd":1},
                    {"fieldname":"start","fieldtype":"Datetime","label":"Start","reqd":1},
                    {"fieldname":"end","fieldtype":"Datetime","label":"End","reqd":1},
                    {"fieldname":"capacity","fieldtype":"Int","label":"Capacity","default":1},
                    {"fieldname":"booked_count","fieldtype":"Int","label":"Booked Count","default":0,"read_only":1},
                    {"fieldname":"status","fieldtype":"Select","label":"Status","options":"Available\nFull\nClosed","default":"Available"}],
            permissions=[{"role":"System Manager","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Mentor","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Udaan Student","read":1}])
    if not frappe.db.exists("DocType", "Sirjna Appointment"):
        upsert("DocType", name="Sirjna Appointment", module="Sirjna", custom=1,
            fields=[{"fieldname":"appointment_type","fieldtype":"Link","label":"Appointment Type","options":"Sirjna Appointment Type","reqd":1},
                    {"fieldname":"slot","fieldtype":"Link","label":"Slot","options":"Sirjna Appointment Slot","reqd":1},
                    {"fieldname":"full_name","fieldtype":"Data","label":"Full Name","reqd":1},
                    {"fieldname":"email","fieldtype":"Data","label":"Email","reqd":1},
                    {"fieldname":"phone","fieldtype":"Data","label":"Phone"},
                    {"fieldname":"provider","fieldtype":"Select","label":"Provider","options":"None\nJitsi\nGoogle Meet\nZoom","default":"None"},
                    {"fieldname":"video_link","fieldtype":"Data","label":"Join URL"},
                    {"fieldname":"calendar_event_id","fieldtype":"Data","label":"Calendar Event ID"},
                    {"fieldname":"status","fieldtype":"Select","label":"Status","options":"Booked\nCompleted\nCancelled","default":"Booked"}],
            permissions=[{"role":"System Manager","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Mentor","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Udaan Student","read":1,"create":1}])
def create_portal_bits():
    content = '<div class="container" style="padding:32px 0"><h2>Book a Free Advisory Call (25 min)</h2></div>'
    upsert("Web Page", "book_call", title="Book a Call", route="book_call", published=1, content=content)
    ps_name = frappe.db.exists("Portal Settings")
    if ps_name:
        ps = frappe.get_doc("Portal Settings", ps_name)
        exists = any((i.route or "") == "/book_call" for i in (ps.get("menu_items") or []))
        if not exists:
            ps.append("menu_items", {"title":"Book a Call","route":"/book_call","enabled":1})
            ps.save(ignore_permissions=True)
def seed_defaults():
    if not frappe.db.exists("Sirjna Appointment Type", {"title": "Free Advisory Call"}):
        frappe.get_doc({"doctype":"Sirjna Appointment Type","title":"Free Advisory Call","duration":25,"active":1}).insert(ignore_permissions=True)
    atype = frappe.db.get_value("Sirjna Appointment Type", {"title":"Free Advisory Call"}, "name")
    if atype:
        for day_offset in (0, 1):
            base = now_datetime().replace(hour=10, minute=0, second=0, microsecond=0)
            start_base = add_to_date(base, days=day_offset)
            for hour_add in (0, 1, 2):
                start = add_to_date(start_base, hours=hour_add)
                end = add_to_date(start, minutes=25)
                key = dict(appointment_type=atype, start=start, end=end)
                exists = frappe.db.exists("Sirjna Appointment Slot", key)
                if not exists:
                    frappe.get_doc({"doctype":"Sirjna Appointment Slot", **key, "capacity":1, "status":"Available"}).insert(ignore_permissions=True)
@frappe.whitelist()
def bootstrap():
    ensure_module_def()
    ensure_roles()
    create_doctypes()
    seed_defaults()
    create_portal_bits()
    frappe.db.commit()
