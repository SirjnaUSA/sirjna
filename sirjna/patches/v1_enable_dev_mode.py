# sirjna/patches/v1_enable_dev_mode.py
import frappe

def execute():
    try:
        frappe.utils.install.set_config("developer_mode", 1)
        frappe.db.commit()
        frappe.logger().info("Developer Mode Enabled via Sirjna patch.")
    except Exception as e:
        frappe.log_error(f"Failed to enable developer_mode: {e}")
