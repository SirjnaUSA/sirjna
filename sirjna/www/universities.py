
import frappe
def get_context(context):
    records = frappe.get_all("University Program",
        fields=["university_name","program_name","country","city","tuition_estimate","deadline","risk_bucket","degree","specialization","program_url"],
        order_by="risk_bucket asc, university_name asc", limit_page_length=500)
    by_bucket = {"Safe": [], "Target": [], "Reach": []}
    for r in records:
        by_bucket.setdefault(r.get("risk_bucket") or "Target", []).append(r)
    context.by_bucket = by_bucket
    context.no_cache = 1
