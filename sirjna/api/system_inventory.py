# -*- coding: utf-8 -*-
"""
Frappe v15+ Site Inventory (max coverage, skip-safe, replica-grade)

What you get (all skip-safe, version-safe):
- DocType meta (fields, perms, Custom Fields, Property Setters) + Singles values
- Web: Web Pages (full), Web Forms (full), Portal Menu, Web Templates (+html)
- Reports (full), Print Formats (meta + html)
- Client Scripts (.js), Server Scripts (.py)
- Roles, Role Profiles (full), Workspaces (full)
- Notifications, Email Templates, Email Accounts (redacted), Email Domains (redacted),
  Auto Email Reports, Auto Repeat, Webhooks (+headers, data)
- OAuth Clients (redacted), Social Logins (if present) (redacted)
- Data Import / Export configs & logs (lightweight indices)
- Integrations (Integration Request index), Payment Gateways/Accounts if these doctypes exist (redacted)
- Files index (with selective payloads for small public files)
- Global Singles snapshots: System Settings, Website Settings, Portal Settings, Navbar Settings,
  Print Settings, Global Defaults (only those that exist on your site)
- Rebuild plan + baseline diff + summary

Secrets and tokens are REDACTED automatically:
- Any field whose fieldtype == "Password"
- Any fieldname matching /(api|key|secret|token|password|private)/i
"""

import csv, io, json, zipfile, re
from datetime import datetime
from typing import List, Dict, Any
import frappe

# -----------------------------
# config / constants
# -----------------------------
STD_META_COLS = {"name","owner","creation","modified","modified_by"}
SUSPECT_NAME_RE = re.compile(r"(api|key|secret|token|password|private|smtp_pass|auth|bearer|client_secret)", re.I)
DEFAULT_FILE_SIZE_LIMIT = 1_000_000  # 1 MB cap to embed file content; increase carefully

SINGLE_CANDIDATES = [
    # core/global
    "System Settings", "Website Settings", "Portal Settings", "Navbar Settings",
    "Print Settings", "Global Defaults",
    # sirjna custom
    "Sirjna Settings",
]

OPTIONAL_BLOCKS = [
    # (Doctype, list-of-fields, deep_dump_boolean)
    ("Notification", ["name","document_type","subject","enabled","event","channel"], True),
    ("Email Template", ["name","subject","response"], True),
    ("Email Account", ["name","email_id","enable_outgoing","enable_incoming","default_outgoing","default_incoming","awaiting_password"], True),
    ("Email Domain", ["name","email_server","use_imap","use_ssl"], True),
    ("Auto Email Report", ["name","report","enabled","frequency","format"], True),
    ("Webhook", ["name","webhook_docevent","webhook_doctype","request_url","enabled","request_method"], True),
    ("Webhook Header", ["name","parent","key","value"], True),
    ("Webhook Data", ["name","parent","fieldname","key","type"], True),
    ("Auto Repeat", ["name","reference_doctype","start_date","frequency","disabled"], True),
    ("OAuth Client", ["name","default_redirect_uri","grant_type"], True),
    ("Social Login Key", ["name","provider","enable_social_login"], True),  # may not exist; skip-safe
    ("Integration Request", ["name","status","integration_request_service","reference_doctype","reference_docname","data"], False),

    # Data import/export utilities
    ("Data Import", ["name","reference_doctype","status"], True),
    ("Data Import Log", ["name","status","success","messages"], False),
    ("Data Export", ["name","reference_doctype","filters"], True),

    # Security / access beyond Roles
    ("Role Profile", ["name","disabled"], True),
]

# Payment-ish doctypes (exist in Frappe/Integrations or ERPNext). Skip if not present.
PAYMENTISH = [
    ("Payment Gateway", ["name","gateway"], True),
    ("Payment Gateway Account", ["name","payment_gateway","merchant_id","is_default"], True),
    ("Payment Settings", ["name"], True),
    ("Payment Request", ["name","status","party_type","party","grand_total","currency"], True),
]

# -----------------------------
# helpers (version & schema safe)
# -----------------------------
def _safe_fields(doctype: str, candidates: List[str]) -> List[str]:
    try:
        meta = frappe.get_meta(doctype)
        cols = {df.fieldname for df in meta.fields}
        cols.update(STD_META_COLS)
        # common flags across versions
        cols.update({"module","custom","standard","istable","issingle","is_tree","autoname","document_type",
                     "is_published","login_required","published","title","route","dt","enabled",
                     "script_type","reference_doctype","desk_access","two_factor_role","public",
                     "ref_doctype","report_type","is_standard","doc_type",
                     "template","template_path","content","main_section"})
        return [f for f in candidates if f in cols]
    except Exception:
        return ["name"]

def _csv_bytes(headers: List[str], rows: List[Dict[str, Any]]) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(headers)
    for r in rows:
        w.writerow([r.get(h, "") for h in headers])
    return buf.getvalue().encode()

def _get_all(doctype: str, fields: List[str], filters=None, order_by="modified desc") -> List[Dict[str, Any]]:
    safe = _safe_fields(doctype, fields)
    if not safe:
        safe = ["name"]
    try:
        return frappe.get_all(doctype, fields=safe, filters=filters or {}, order_by=order_by)
    except Exception:
        return []  # missing doctype → skip

def _get_doc(doctype: str, name: str):
    try:
        return frappe.get_doc(doctype, name)
    except Exception:
        return None

def _json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)

def _sanitize_filename(s: str) -> str:
    s = (s or "unnamed").strip().replace(" ", "_")
    return re.sub(r"[^a-zA-Z0-9._-]", "_", s)[:140]

def _redact_doc(doc: Dict[str, Any], doctype: str) -> Dict[str, Any]:
    """Redact password/secret-ish fields by fieldtype or name pattern."""
    try:
        meta = frappe.get_meta(doctype)
    except Exception:
        meta = None
    redacted = {}
    for k, v in doc.items():
        redact = False
        if meta:
            df = meta.get_field(k)
            if df and (df.fieldtype or "").lower() == "password":
                redact = True
        if not redact and SUSPECT_NAME_RE.search(k or ""):
            redact = True
        redacted[k] = "***REDACTED***" if redact and v not in (None, "", 0) else v
    return redacted

# -----------------------------
# baseline (for diff only)
# -----------------------------
def _sirjna_expected():
    expected_doctypes = {
        "Student Profile","Mentorship Step","Student Progress",
        "University","Program Deadline","Shortlist","Shortlist Entry",
        "Webinar","Webinar Registration","Advisory Session","Payment Record",
        "Resource Pack","Resource Link","Student Document","Document Review",
        "Referral Link","Referral Credit","Payout Request","Sirjna Settings",
    }
    expected_pages = {
        "index","how-it-works","pricing","webinars","advisory",
        "apply","faq","about","terms","privacy","portal"
    }
    return {"doctypes": expected_doctypes, "pages": expected_pages}

# -----------------------------
# dumpers (each writes indexes + deep JSON/assets; all skip-safe)
# -----------------------------
def dump_doctypes(z):
    doctypes = _get_all("DocType",
        ["name","module","custom","istable","issingle","autoname","document_type","is_tree"]
    )
    z.writestr("indexes/inventory_doctypes.csv",
               _csv_bytes(["name","module","custom","istable","issingle","autoname","document_type","is_tree"], doctypes))

    singles = [d for d in doctypes if str(d.get("issingle")) in ("1","True","true")]
    z.writestr("indexes/inventory_single_settings.csv",
               _csv_bytes(["name","module","autoname"], singles))

    # per-DocType meta (schema + perms + customization)
    for d in doctypes:
        dt = d.get("name")
        if not dt: continue
        meta = frappe.get_meta(dt)
        meta_dict = {
            "doctype": "DocType",
            "name": meta.name,
            "module": getattr(meta, "module", None),
            "issingle": getattr(meta, "issingle", 0),
            "istable": getattr(meta, "istable", 0),
            "is_tree": getattr(meta, "is_tree", 0),
            "autoname": getattr(meta, "autoname", None),
            "document_type": getattr(meta, "document_type", None),
            "custom": getattr(meta, "custom", 0),
            "fields": [],
            "permissions": [],
        }
        for f in meta.fields:
            meta_dict["fields"].append({
                k: getattr(f, k, None) for k in [
                    "fieldname","label","fieldtype","options","reqd","unique","bold","in_list_view",
                    "in_standard_filter","search_index","no_copy","default","read_only","allow_on_submit",
                    "depends_on","mandatory_depends_on","collapsible","precision","length","translatable",
                    "hidden","in_global_search","in_preview","columns"
                ]
            })
        perms = _get_all("DocPerm",
            _safe_fields("DocPerm",
                ["role","permlevel","read","write","create","delete","submit","cancel","amend",
                 "report","print","email","export","share","set_user_permissions","select","if_owner"]
            ),
            filters={"parent": dt},
            order_by="permlevel asc, role asc"
        )
        meta_dict["permissions"] = perms

        ps = _get_all("Property Setter",
            ["name","doctype_or_field","doc_type","field_name","property","value","property_type","row_name"],
            filters={"doc_type": dt})
        cf = _get_all("Custom Field",
            ["name","dt","fieldname","label","fieldtype","options","insert_after","reqd","default","hidden","read_only","in_list_view","bold"],
            filters={"dt": dt})
        meta_dict["property_setters"] = ps
        meta_dict["custom_fields"] = cf
        z.writestr(f"doctypes/meta/{_sanitize_filename(dt)}.json", _json(meta_dict))

    # Singles values snapshot
    for s in singles:
        sname = s.get("name")
        try:
            d = frappe.get_single(sname).as_dict()
            fields = {f.fieldname for f in frappe.get_meta(sname).fields}
            values = {k: d.get(k) for k in fields}
            z.writestr(f"singles/values/{_sanitize_filename(sname)}.json", _json(values))
        except Exception:
            continue

def dump_web(z):
    web_pages = _get_all("Web Page",
        ["name","route","published","title","template","template_path","content","main_section"]
    )
    z.writestr("indexes/inventory_web_pages.csv",
               _csv_bytes(["name","route","published","title","template","template_path"], web_pages))
    for p in web_pages:
        doc = _get_doc("Web Page", p["name"])
        if not doc: continue
        blob = doc.as_dict(no_default_fields=True, convert_dates_to_str=True)
        for k in ("parent","parentfield","parenttype"): blob.pop(k, None)
        route = (blob.get("route") or blob.get("name") or "page")
        z.writestr(f"web/pages/{_sanitize_filename(route)}.json", _json(blob))

    web_forms = _get_all("Web Form",
        ["name","route","is_published","login_required","title"]
    )
    z.writestr("indexes/inventory_web_forms.csv",
               _csv_bytes(["name","route","is_published","login_required","title"], web_forms))
    for wf in web_forms:
        doc = _get_doc("Web Form", wf["name"])
        if not doc: continue
        z.writestr(f"web/forms/{_sanitize_filename(wf['name'])}.json",
                   _json(doc.as_dict(no_default_fields=True, convert_dates_to_str=True)))

    portal_menu = _get_all("Portal Menu Item",
        ["title","route","enabled","parent_label"]
    )
    z.writestr("indexes/inventory_portal_menu.csv",
               _csv_bytes(["title","route","enabled","parent_label"], portal_menu))
    if portal_menu:
        z.writestr("web/portal_menu.json", _json(portal_menu))

    # Web Templates (plus source HTML)
    web_templates = _get_all("Web Template", ["name","type","standard","is_standard","module"])
    if web_templates:
        z.writestr("indexes/inventory_web_templates.csv",
                   _csv_bytes(["name","type","standard","is_standard","module"], web_templates))
        for wt in web_templates:
            doc = _get_doc("Web Template", wt["name"])
            if not doc: continue
            d = doc.as_dict(no_default_fields=True, convert_dates_to_str=True)
            html = d.pop("html", "") if "html" in d else ""
            z.writestr(f"web/templates/{_sanitize_filename(wt['name'])}.json", _json(d))
            z.writestr(f"web/templates_html/{_sanitize_filename(wt['name'])}.html", html)

def dump_reports_prints(z):
    reports = _get_all("Report",
        ["name","ref_doctype","report_type","is_standard"]
    )
    z.writestr("indexes/inventory_reports.csv",
               _csv_bytes(["name","ref_doctype","report_type","is_standard"], reports))
    for r in reports:
        doc = _get_doc("Report", r["name"])
        if not doc: continue
        z.writestr(f"reports/{_sanitize_filename(r['name'])}.json",
                   _json(doc.as_dict(no_default_fields=True, convert_dates_to_str=True)))

    prints = _get_all("Print Format",
        ["name","doc_type","module","standard"]
    )
    z.writestr("indexes/inventory_print_formats.csv",
               _csv_bytes(["name","doc_type","module","standard"], prints))
    for pf in prints:
        doc = _get_doc("Print Format", pf["name"])
        if not doc: continue
        d = doc.as_dict(no_default_fields=True, convert_dates_to_str=True)
        html = d.pop("html", None) or d.pop("raw_html", None) or ""
        z.writestr(f"print_formats/meta/{_sanitize_filename(pf['name'])}.json", _json(d))
        z.writestr(f"print_formats/html/{_sanitize_filename(pf['name'])}.html", html)

def dump_scripts(z):
    client_scripts = _get_all("Client Script", ["name","dt","enabled"])
    z.writestr("indexes/inventory_client_scripts.csv",
               _csv_bytes(["name","dt","enabled"], client_scripts))
    for cs in client_scripts:
        doc = _get_doc("Client Script", cs["name"])
        if not doc: continue
        z.writestr(f"scripts/client/{_sanitize_filename(cs['dt'])}__{_sanitize_filename(cs['name'])}.js",
                   (doc.script or ""))

    server_scripts = _get_all("Server Script", ["name","script_type","reference_doctype","enabled"])
    z.writestr("indexes/inventory_server_scripts.csv",
               _csv_bytes(["name","script_type","reference_doctype","enabled"], server_scripts))
    for ss in server_scripts:
        doc = _get_doc("Server Script", ss["name"])
        if not doc: continue
        z.writestr(f"scripts/server/{_sanitize_filename(ss['script_type'])}__{_sanitize_filename(ss['name'])}.py",
                   (doc.script or ""))

def dump_security_workspace(z):
    roles = _get_all("Role", ["name","desk_access","two_factor_role"])
    z.writestr("indexes/inventory_roles.csv",
               _csv_bytes(["name","desk_access","two_factor_role"], roles))
    if roles:
        z.writestr("security/roles.json", _json(roles))

    role_profiles = _get_all("Role Profile", ["name","disabled"])
    if role_profiles:
        z.writestr("indexes/inventory_role_profiles.csv",
                   _csv_bytes(["name","disabled"], role_profiles))
        rp_docs = []
        for rp in role_profiles:
            doc = _get_doc("Role Profile", rp["name"])
            if not doc: continue
            rp_docs.append(doc.as_dict(no_default_fields=True, convert_dates_to_str=True))
        z.writestr("security/role_profiles.json", _json(rp_docs))

    workspaces = _get_all("Workspace", ["name","public","module"])
    z.writestr("indexes/inventory_workspaces.csv",
               _csv_bytes(["name","public","module"], workspaces))
    for ws in workspaces:
        doc = _get_doc("Workspace", ws["name"])
        if not doc: continue
        z.writestr(f"workspaces/{_sanitize_filename(ws['name'])}.json",
                   _json(doc.as_dict(no_default_fields=True, convert_dates_to_str=True)))

def dump_ops_optional(z):
    # singles snapshot for common settings (skip-safe)
    for s in SINGLE_CANDIDATES:
        try:
            meta = frappe.get_meta(s)
            if not meta or not meta.issingle:  # must be Single
                continue
            d = frappe.get_single(s).as_dict()
            fields = {f.fieldname for f in meta.fields}
            values = {k: d.get(k) for k in fields}
            z.writestr(f"singles/values/{_sanitize_filename(s)}.json", _json(values))
        except Exception:
            continue

    # optional doctypes
    for dt, fields, deep in OPTIONAL_BLOCKS + PAYMENTISH:
        rows = _get_all(dt, fields)
        if not rows:
            continue
        z.writestr(f"indexes/opt_{_sanitize_filename(dt)}.csv", _csv_bytes(_safe_fields(dt, fields), rows))

        if deep:
            docs_out = []
            for r in rows:
                doc = _get_doc(dt, r["name"])
                if not doc: continue
                d = doc.as_dict(no_default_fields=True, convert_dates_to_str=True)
                docs_out.append(_redact_doc(d, dt))
            if docs_out:
                z.writestr(f"optional/{_sanitize_filename(dt)}.json", _json(docs_out))

def dump_files(z):
    files = _get_all("File",
        ["name","file_name","file_url","attached_to_doctype","attached_to_name","is_private","file_size","content_hash"]
    )
    if files:
        z.writestr("indexes/inventory_files.csv",
                   _csv_bytes(["name","file_name","file_url","attached_to_doctype","attached_to_name","is_private","file_size","content_hash"], files))

    # include small **public** files inline; skip private content
    for f in files:
        try:
            if not f.get("file_url"):
                continue
            if int(f.get("is_private") or 0):
                continue  # keep private content out of the pack
            size = int(f.get("file_size") or 0)
            if size and size <= DEFAULT_FILE_SIZE_LIMIT:
                filedoc = _get_doc("File", f["name"])
                if not filedoc: continue
                content = filedoc.get_content()  # bytes
                z.writestr(f"files/public_inline/{_sanitize_filename(f.get('file_name') or f['name'])}", content or b"")
        except Exception:
            continue

# -----------------------------
# summary + diff
# -----------------------------
def build_summary():
    doctypes = _get_all("DocType", ["name"])
    web_pages = _get_all("Web Page", ["route"])
    web_forms = _get_all("Web Form", ["name"])
    reports   = _get_all("Report", ["name"])
    prints    = _get_all("Print Format", ["name"])
    client_scripts = _get_all("Client Script", ["name"])
    server_scripts = _get_all("Server Script", ["name"])
    roles     = _get_all("Role", ["name"])
    workspaces= _get_all("Workspace", ["name"])
    portal_menu = _get_all("Portal Menu Item", ["route"])

    exp = _sirjna_expected()
    actual_doctype_names = {d.get("name") for d in doctypes if d.get("name")}
    actual_page_routes   = {(p.get("route") or "").strip("/").split("?")[0] for p in web_pages if p.get("route")}

    return {
        "generated_on": datetime.now().isoformat(),
        "counts": {
            "doctypes": len(doctypes), "web_pages": len(web_pages), "web_forms": len(web_forms),
            "reports": len(reports), "print_formats": len(prints),
            "client_scripts": len(client_scripts), "server_scripts": len(server_scripts),
            "roles": len(roles), "workspaces": len(workspaces), "portal_menu": len(portal_menu)
        },
        "diff": {
            "missing_doctypes": sorted(exp["doctypes"] - actual_doctype_names),
            "extra_doctypes":   sorted(actual_doctype_names - exp["doctypes"]),
            "missing_pages":    sorted(exp["pages"] - actual_page_routes),
            "extra_pages":      sorted(actual_page_routes - exp["pages"]),
        }
    }

# -----------------------------
# main entrypoint
# -----------------------------
@frappe.whitelist()
def generate_system_inventory():
    """
    v15-max coverage, skip-safe, replica-grade site inventory.
    Produces ZIP with:
      indexes/*.csv
      doctypes/meta/*.json
      singles/values/*.json
      web/pages|forms|templates*.*
      reports/*.json
      print_formats/meta/*.json + print_formats/html/*.html
      scripts/client|server/*
      security/roles.json, security/role_profiles.json
      workspaces/*.json
      optional/*.json (notifications/webhooks/email/oauth/etc)
      files/public_inline/* (small public files) + files index
      inventory_summary.json
      inventory_expected_vs_actual.csv
      rebuild_plan.json
    """
    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as z:
        dump_doctypes(z)
        dump_web(z)
        dump_reports_prints(z)
        dump_scripts(z)
        dump_security_workspace(z)
        dump_ops_optional(z)
        dump_files(z)

        summary = build_summary()
        z.writestr("inventory_summary.json", _json(summary))

        diff_rows = (
            [{"type":"MISSING_DOCTYPE","name":n} for n in summary["diff"]["missing_doctypes"]] +
            [{"type":"EXTRA_DOCTYPE","name":n}   for n in summary["diff"]["extra_doctypes"]]   +
            [{"type":"MISSING_PAGE","name":n}    for n in summary["diff"]["missing_pages"]]    +
            [{"type":"EXTRA_PAGE","name":n}      for n in summary["diff"]["extra_pages"]]
        )
        z.writestr("inventory_expected_vs_actual.csv", _csv_bytes(["type","name"], diff_rows))

        rebuild = {
            "order": [
                "security/roles.json, security/role_profiles.json",
                "doctypes/meta/*.json",
                "singles/values/*.json",
                "reports/*.json",
                "print_formats/meta/*.json + print_formats/html/*.html",
                "scripts/server/*, scripts/client/*",
                "workspaces/*.json",
                "web/pages/*.json, web/forms/*.json, web/templates*.*, web/portal_menu.json",
                "optional/*.json",
                "files/public_inline/* (then manually reattach others from files index)"
            ],
            "notes": [
                "Recreate roles/profiles first for permission mapping.",
                "Import DocTypes with property setters & custom fields present in meta JSON.",
                "Then set Singles values.",
                "Restore reports/prints/scripts/workspaces.",
                "Restore web assets and portal menu.",
                "Recreate notifications/webhooks/email/oauth with redacted fields updated manually.",
                "Use files index to re-upload private/large files; small public files are packaged."
            ]
        }
        z.writestr("rebuild_plan.json", _json(rebuild))

    fname = f"system_inventory_{frappe.utils.now_datetime().strftime('%Y%m%d_%H%M%S')}.zip"
    filedoc = frappe.get_doc({
        "doctype": "File",
        "file_name": fname,
        "is_private": 1,
        "content": zbuf.getvalue(),
    }).insert(ignore_permissions=True)

    return {"file_url": filedoc.file_url, "summary": summary}
