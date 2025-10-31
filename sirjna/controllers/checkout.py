import frappe
@frappe.whitelist()
def create_payment_request(amount=499, currency="USD"):
    """Create Payment Request if 'payments' app exists; else return Stripe link.
    Also creates an Udaan Order with Pending status.
    """
    order = frappe.new_doc("Udaan Order")
    order.amount = float(amount)
    order.currency = currency
    order.status = "Pending"
    if frappe.session.user != "Guest":
        order.owner = frappe.session.user
    order.insert(ignore_permissions=True)
    try:
        if "payments" in frappe.get_installed_apps() and frappe.db.exists("DocType", "Payment Request"):
            pr = frappe.new_doc("Payment Request")
            pr.party_type = "User"
            pr.party = frappe.session.user
            pr.currency = currency
            pr.grand_total = float(amount)
            pr.mode_of_payment = "Stripe"
            pr.insert(ignore_permissions=True)
            pr.submit()
            url = pr.get("payment_url") or f"/app/payment-request/{pr.name}"
            order.payment_gateway = "Stripe"
            order.payment_request = url
            order.save(ignore_permissions=True)
            return {"mode":"payment_request","url": url}
    except Exception:
        pass
    stripe = frappe.db.get_single_value("Sirjna Settings", "stripe_payment_link") or "#"
    order.payment_gateway = "Stripe"
    order.payment_request = stripe
    order.save(ignore_permissions=True)
    return {"mode":"stripe_link","url": stripe}