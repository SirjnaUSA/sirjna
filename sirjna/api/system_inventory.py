import csv, io, json, zipfile
from datetime import datetime
import frappe

def _csv_bytes(headers, rows):
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(headers)
    for r in rows:
        w.writerow([r.get(h, "") for h in headers])
    return buf.getvalue().encode()

def _get_all(doctype, fields, filters=None):
    return frappe.get_all(doctype, fields=fields, filters=filters or {}, order_by="modified desc")

def _sirjna_expected():
    # Baseline from Sirjna handbooks (DocTypes + public pages)
    expected_doctypes = [
        # Core mentorship and progress
        "Phase", "Student Profile", "Mentorship Step", "Student Progress",
        # University data & deadlines
        "University", "Program Deadline", "Shortlist", "Shortlist Entry",
        # Sessions & webinars & payments
        "Webinar", "Webinar Registration", "Advisory Session", "Payment Record",
        # Resources & originality
        "Resource Pack", "Resource Link", "Student Document", "Document Review",
        # Referrals & settings
        "Referral Link", "Referral Credit", "Payout Request", "Sirjna Settings",
    ]
    expected_pages = [
        "index", "how-it-works", "pricing", "webinars", "advisory",
        "apply", "faq", "about", "terms", "privacy", "portal"
    ]
    return {"doctypes": set(expected_doctypes), "pages": set(expected_pages)}

@frappe.whitelist()
def generate_system_inventory():
    """Build a ZIP of CSVs + a JSON summary and return a File URL."""
    # 1) Collect data
    doctypes = _get_all("DocType", ["name","module","custom","istable","autoname","document_type","issingle"])
    singles  = [d for d in doctypes if d.get("issingle")]
    web_pages = _get_all("Web Page", ["name","route","published","template_path"])
    web_forms = _get_all("Web Form", ["name","route","is_published","login_required"])
    reports   = _get_all("Report", ["name","ref_doctype","report_type","is_standard"])
    prints    = _get_all("Print Format", ["name","doc_type","module","standard"])
    client_scripts = _get_all("Client Script", ["name","dt","enabled"])
    server_scripts = _get_all("Server Script", ["name","script_type","reference_doctype","enabled"])
    roles     = _get_all("Role", ["name","desk_access","two_factor_role"])
    workspaces= _get_all("Workspace", ["name","public","module"])
    portal_menu = _get_all("Portal Menu Item", ["title","route","enabled","parent_label"])

    # 2) Expected vs actual (Sirjna baseline)
    exp = _sirjna_expected()
    actual_doctype_names = {d["name"] for d in doctypes}
    actual_page_routes   = {p["route"].strip("/").split("?")[0] for p in web_pages if p.get("route")}
    missing_doctypes = sorted(exp["doctypes"] - actual_doctype_names)
    extra_doctypes   = sorted(actual_doctype_names - exp["doctypes"])
    missing_pages    = sorted(exp["pages"] - actual_page_routes)
    extra_pages      = sorted(actual_page_routes - exp["pages"])

    # 3) ZIP it
    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("inventory_doctypes.csv",
                   _csv_bytes(["name","module","custom","is_table","autoname","document_type","issingle"], doctypes))
        z.writestr("inventory_single_settings.csv",
                   _csv_bytes(["name","module","autoname"], singles))
        z.writestr("inventory_web_pages.csv",
                   _csv_bytes(["name","route","published","template_path"], web_pages))
        z.writestr("inventory_web_forms.csv",
                   _csv_bytes(["name","route","is_published","login_required"], web_forms))
        z.writestr("inventory_reports.csv",
                   _csv_bytes(["name","ref_doctype","report_type","is_standard"], reports))
        z.writestr("inventory_print_formats.csv",
                   _csv_bytes(["name","doc_type","module","standard"], prints))
        z.writestr("inventory_client_scripts.csv",
                   _csv_bytes(["name","dt","enabled"], client_scripts))
        z.writestr("inventory_server_scripts.csv",
                   _csv_bytes(["name","script_type","reference_doctype","enabled"], server_scripts))
        z.writestr("inventory_roles.csv",
                   _csv_bytes(["name","desk_access","two_factor_role"], roles))
        z.writestr("inventory_workspaces.csv",
                   _csv_bytes(["name","public","module"], workspaces))
        z.writestr("inventory_portal_menu.csv",
                   _csv_bytes(["title","route","enabled","parent_label"], portal_menu))

        summary = {
            "generated_on": datetime.now().isoformat(),
            "counts": {
                "doctypes": len(doctypes), "singles": len(singles),
                "web_pages": len(web_pages), "web_forms": len(web_forms),
                "reports": len(reports), "print_formats": len(prints),
                "client_scripts": len(client_scripts), "server_scripts": len(server_scripts),
                "roles": len(roles), "workspaces": len(workspaces), "portal_menu": len(portal_menu),
            },
            "diff": {
                "missing_doctypes": missing_doctypes,
                "extra_doctypes": extra_doctypes,
                "missing_pages": missing_pages,
                "extra_pages": extra_pages,
            }
        }
        z.writestr("inventory_summary.json", json.dumps(summary, indent=2))
        z.writestr("inventory_expected_vs_actual.csv",
                   _csv_bytes(["type","name"], 
                    ([{"type":"MISSING_DOCTYPE","name":n} for n in missing_doctypes] +
                     [{"type":"EXTRA_DOCTYPE","name":n}   for n in extra_doctypes]   +
                     [{"type":"MISSING_PAGE","name":n}    for n in missing_pages]    +
                     [{"type":"EXTRA_PAGE","name":n}      for n in extra_pages])))

    # 4) Save as File and return URL
    fname = f"system_inventory_{frappe.utils.now_datetime().strftime('%Y%m%d_%H%M%S')}.zip"
    filedoc = frappe.get_doc({
        "doctype": "File",
        "file_name": fname,
        "is_private": 1,
        "content": zbuf.getvalue(),
    }).insert(ignore_permissions=True)
    return {"file_url": filedoc.file_url, "summary": summary}
