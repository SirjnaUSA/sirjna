import frappe

def get_setting(key):
    val = frappe.conf.get(key)
    if val: return val
    try:
        return frappe.db.get_single_value("Sirjna Settings", key)
    except Exception:
        return None

def get_mode():
    try:
        return (frappe.db.get_single_value("Sirjna Settings", "mode") or "Test").strip()
    except Exception:
        return "Test"

def stripe_keys():
    mode = (get_mode() or "test").lower()
    if mode == "live":
        return (get_setting("stripe_secret_key_live"), get_setting("stripe_webhook_secret_live"))
    return (get_setting("stripe_secret_key_test") or get_setting("stripe_secret_key"),
            get_setting("stripe_webhook_secret_test") or get_setting("stripe_webhook_secret"))

def payments_enabled():
    sk, _ = stripe_keys()
    return bool(sk)

def zoom_enabled():
    return all([get_setting("zoom_account_id"), get_setting("zoom_client_id"), get_setting("zoom_client_secret")])
