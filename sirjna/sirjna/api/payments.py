import frappe
from .config import payments_enabled, stripe_keys

@frappe.whitelist()
def start_checkout(student: str, purpose: str):
    if not payments_enabled():
        frappe.throw("Payments are not configured yet.")
    sk, _ = stripe_keys()
    try:
        import stripe
    except Exception:
        frappe.throw("Stripe library missing. Ask admin to add 'stripe' to the environment.")
    stripe.api_key = sk
    amount_map = {"Advisory_25": 25_00, "Mentorship_349": 349_00, "Mentorship_499": 499_00}
    if purpose not in amount_map:
        frappe.throw("Invalid purpose.")
    pr = frappe.get_doc({"doctype":"Payment Record",
                         "student": student,
                         "purpose": purpose,
                         "amount_usd": float(str(amount_map[purpose]/100.0)),
                         "status": "Created"})
    pr.insert(ignore_permissions=True)
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price_data": {"currency":"usd","unit_amount": amount_map[purpose],
                                    "product_data":{"name": purpose.replace("_"," ")}},
                     "quantity": 1}],
        success_url=f"{frappe.utils.get_url('/apply?paid=1')}",
        cancel_url=f"{frappe.utils.get_url('/apply?cancel=1')}",
        metadata={"payment_record": pr.name}
    )
    pr.db_set("stripe_payment_intent", session.get("payment_intent"))
    return {"url": session.get("url")}

@frappe.whitelist(allow_guest=True)
def webhook():
    sk, whsec = stripe_keys()
    import stripe
    payload = frappe.safe_decode(frappe.request.data or b"")
    sig = frappe.get_request_header("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig, whsec)
    except Exception as e:
        frappe.local.response.http_status_code = 400
        return {"error": str(e)}
    if event.get("type") == "checkout.session.completed":
        meta = event["data"]["object"].get("metadata") or {}
        pr_name = meta.get("payment_record")
        if pr_name and frappe.db.exists("Payment Record", pr_name):
            frappe.db.set_value("Payment Record", pr_name, "status", "Paid")
    return {"ok": True}

def on_payment_update(doc, method=None):
    return
