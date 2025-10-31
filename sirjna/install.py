import frappe
from frappe.utils import now_datetime, add_to_date

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
    for r in ["Udaan Student", "Mentor", "Website Manager", "Program Manager"]:
        if not frappe.db.exists("Role", r):
            frappe.get_doc({"doctype":"Role","role_name":r}).insert(ignore_permissions=True)

def ensure_role_profiles():
    if not frappe.db.exists("Role Profile", "Udaan Student Basic"):
        rp = frappe.get_doc({"doctype":"Role Profile","role_profile":"Udaan Student Basic"})
        rp.append("roles", {"role":"Udaan Student"})
        rp.insert(ignore_permissions=True)

def ensure_users_demo():
    users = [
        dict(email="mentor@sirjna.com", first_name="Mentor", roles=["System Manager","Mentor"]),
        dict(email="admin@sirjna.com", first_name="Admin", roles=["System Manager"]),
        dict(email="student@sirjna.com", first_name="Student", roles=["Udaan Student"]),
    ]
    for u in users:
        if not frappe.db.exists("User", u["email"]):
            doc = frappe.get_doc({
                "doctype":"User",
                "email":u["email"],
                "first_name":u["first_name"],
                "send_welcome_email":0,
                "new_password":"ChangeMe123!"
            }).insert(ignore_permissions=True)
            for r in u["roles"]:
                doc.append("roles", {"role": r})
            doc.save(ignore_permissions=True)

def ensure_settings_and_website():
    if not frappe.db.exists("DocType", "Sirjna Settings"):
        upsert("DocType",
            name="Sirjna Settings",
            module="Sirjna",
            custom=1, is_single=1,
            fields=[
                {"fieldname":"brand_primary","fieldtype":"Data","label":"Brand Primary"},
                {"fieldname":"brand_accent","fieldtype":"Data","label":"Brand Accent"},
                {"fieldname":"brand_bg","fieldtype":"Data","label":"Brand Background"},
                {"fieldname":"portal_banner_text","fieldtype":"Small Text","label":"Portal Banner Text"},
                {"fieldname":"stripe_payment_link","fieldtype":"Data","label":"Stripe Payment Link"},
                {"fieldname":"calendly_url","fieldtype":"Data","label":"Calendly URL"},
                {"fieldname":"tally_intake_url","fieldtype":"Data","label":"Tally Intake Form URL"},
                {"fieldname":"ga4_measurement_id","fieldtype":"Data","label":"GA4 Measurement ID"},
                {"fieldname":"support_email","fieldtype":"Data","label":"Support Email"},
                {"fieldname":"support_phone","fieldtype":"Data","label":"Support Phone"},
            ],
            permissions=[{"role":"System Manager","read":1,"write":1}]
        )
    if not frappe.db.exists("Sirjna Settings"):
        s = frappe.new_doc("Sirjna Settings")
        s.brand_primary = "#0A2342"
        s.brand_accent = "#D4AF37"
        s.brand_bg = "#FFFFFF"
        s.portal_banner_text = "Welcome to Udaan – your guided path to US/Canada engineering programs."
        s.support_email = "support@sirjna.com"
        s.support_phone = "+91-00000-00000"
        s.insert(ignore_permissions=True)
    try:
        ps = frappe.get_single("Portal Settings")
        ps.default_portal_home = "/portal"
        ps.allow_guest = 0
        ps.allow_signup = 0
        exists = any((i.route or "") == "/book_call" for i in (ps.get("menu_items") or []))
        if not exists:
            ps.append("menu_items", {"title":"Book a Call","route":"/book_call","enabled":1})
        ps.save()
    except Exception:
        pass

def ensure_core_doctypes():
    if not frappe.db.exists("DocType", "University Program"):
        upsert("DocType",
            name="University Program", module="Sirjna", custom=1,
            fields=[
                {"fieldname":"university_name","fieldtype":"Data","label":"University Name","reqd":1},
                {"fieldname":"program_name","fieldtype":"Data","label":"Program Name","reqd":1},
                {"fieldname":"degree","fieldtype":"Data","label":"Degree"},
                {"fieldname":"specialization","fieldtype":"Data","label":"Specialization"},
                {"fieldname":"country","fieldtype":"Data","label":"Country"},
                {"fieldname":"city","fieldtype":"Data","label":"City"},
                {"fieldname":"tuition_estimate","fieldtype":"Currency","label":"Tuition Estimate"},
                {"fieldname":"deadline","fieldtype":"Date","label":"Deadline"},
                {"fieldname":"risk_bucket","fieldtype":"Select","label":"Risk Bucket","options":"Safe\nTarget\nReach"},
                {"fieldname":"program_url","fieldtype":"Data","label":"Program URL"},
            ],
            permissions=[{"role":"System Manager","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Mentor","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Udaan Student","read":1}]
        )
    if not frappe.db.exists("DocType", "Shortlist"):
        upsert("DocType",
            name="Shortlist", module="Sirjna", custom=1,
            fields=[
                {"fieldname":"owner_user","fieldtype":"Link","options":"User","label":"Owner User","reqd":1},
                {"fieldname":"university_name","fieldtype":"Data","label":"University Name","reqd":1},
                {"fieldname":"program_name","fieldtype":"Data","label":"Program Name"},
                {"fieldname":"risk_bucket","fieldtype":"Select","label":"Risk Bucket","options":"Safe\nTarget\nReach"},
                {"fieldname":"status","fieldtype":"Select","label":"Status","options":"Draft\nApplied\nAdmit\nReject\nWaitlist","default":"Draft"},
            ],
            permissions=[{"role":"System Manager","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Mentor","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Udaan Student","read":1,"create":1,"write":1}]
        )
    if not frappe.db.exists("DocType", "Student Profile"):
        upsert("DocType",
            name="Student Profile", module="Sirjna", custom=1,
            fields=[
                {"fieldname":"user","fieldtype":"Link","options":"User","label":"User","reqd":1},
                {"fieldname":"full_name","fieldtype":"Data","label":"Full Name"},
                {"fieldname":"email","fieldtype":"Data","label":"Email"},
                {"fieldname":"phone","fieldtype":"Data","label":"Phone"},
                {"fieldname":"target_term","fieldtype":"Data","label":"Target Term"},
                {"fieldname":"target_year","fieldtype":"Int","label":"Target Year"},
            ],
            permissions=[{"role":"System Manager","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Mentor","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Udaan Student","read":1,"write":1}]
        )
    if not frappe.db.exists("DocType", "Application Step"):
        upsert("DocType",
            name="Application Step", module="Sirjna", custom=1,
            fields=[
                {"fieldname":"owner_user","fieldtype":"Link","options":"User","label":"Owner User","reqd":1},
                {"fieldname":"title","fieldtype":"Data","label":"Title","reqd":1},
                {"fieldname":"status","fieldtype":"Select","label":"Status","options":"Planned\nIn Progress\nCompleted","default":"Planned"},
                {"fieldname":"due_date","fieldtype":"Date","label":"Due Date"},
                {"fieldname":"notes","fieldtype":"Small Text","label":"Notes"},
            ],
            permissions=[{"role":"System Manager","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Mentor","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Udaan Student","read":1,"write":1,"create":1}]
        )
    if not frappe.db.exists("DocType", "Udaan Order"):
        upsert("DocType",
            name="Udaan Order", module="Sirjna", custom=1,
            fields=[
                {"fieldname":"owner","fieldtype":"Link","options":"User","label":"Owner"},
                {"fieldname":"amount","fieldtype":"Currency","label":"Amount","reqd":1},
                {"fieldname":"currency","fieldtype":"Data","label":"Currency","default":"USD"},
                {"fieldname":"status","fieldtype":"Select","label":"Status","options":"Pending\nPaid\nFailed","default":"Pending"},
                {"fieldname":"payment_gateway","fieldtype":"Data","label":"Payment Gateway"},
                {"fieldname":"payment_request","fieldtype":"Data","label":"Payment Request URL"},
            ],
            permissions=[{"role":"System Manager","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Mentor","read":1,"write":1,"create":1,"delete":1},
                         {"role":"Udaan Student","read":1}]
        )

def ensure_workflow():
    if not frappe.db.exists("Workflow", "Application Step Flow"):
        frappe.get_doc({
            "doctype":"Workflow",
            "workflow_name":"Application Step Flow",
            "document_type":"Application Step",
            "is_active":1,
            "workflow_state_field":"status",
            "states":[
                {"state":"Planned","doc_status":0,"allow_edit":"Udaan Student"},
                {"state":"In Progress","doc_status":0,"allow_edit":"Udaan Student"},
                {"state":"Completed","doc_status":1,"allow_edit":"Udaan Student"}
            ],
            "transitions":[
                {"state":"Planned","action":"Start","next_state":"In Progress","allow":"Udaan Student"},
                {"state":"In Progress","action":"Complete","next_state":"Completed","allow":"Udaan Student"},
                {"state":"In Progress","action":"Back to Planned","next_state":"Planned","allow":"Udaan Student"}
            ]
        }).insert(ignore_permissions=True)

def ensure_workspace():
    if not frappe.db.exists("Workspace", {"label":"Sirjna"}):
        frappe.get_doc({
            "doctype":"Workspace",
            "label":"Sirjna",
            "module":"Sirjna",
            "public":1,
            "sequence_id":1,
            "content":"""
# Sirjna
## Quick Links
- List/Student Profile
- List/Application Step
- List/Shortlist
- List/University Program
"""
        }).insert(ignore_permissions=True)

def ensure_demo_data():
    count = frappe.db.count("University Program") if frappe.db.exists("DocType","University Program") else 0
    if count == 0:
        for uni, city, cc in [("Arizona State University","Tempe","US"),("University of Toronto","Toronto","CA"),("UC Berkeley","Berkeley","US")]:
            upsert("University Program", None,
                   university_name=uni, program_name="MS in Civil Engineering",
                   degree="MS", specialization="Transportation",
                   country=cc, city=city, tuition_estimate=45000.00, risk_bucket="Target",
                   deadline=add_to_date(now_datetime(), months=3).date(), program_url="https://example.com")

def bootstrap_everything():
    ensure_module_def()
    ensure_roles()
    ensure_role_profiles()
    ensure_users_demo()
    ensure_settings_and_website()
    ensure_core_doctypes()
    ensure_workflow()
    ensure_workspace()
    ensure_demo_data()
    frappe.db.commit()