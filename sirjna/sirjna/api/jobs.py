import frappe

def send_webinar_reminders():
    try:
        regs = frappe.get_all("Webinar Registration",
                              fields=["name","email","webinar"],
                              filters={"status":["in",["Registered"]]},
                              limit=200)
        for r in regs:
            join = None
            try:
                join = frappe.db.get_value("Webinar", r["webinar"], "zoom_join_url")
            except Exception:
                pass
            frappe.sendmail(
                recipients=[r["email"]],
                subject="Reminder: Your Sirjna webinar",
                message=f"Your webinar is coming up. Join: {join or 'Link will be emailed separately.'}"
            )
    except Exception:
        pass

def auto_unlock_next_phase():
    return
