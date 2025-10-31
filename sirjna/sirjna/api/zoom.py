import base64, json, requests
import frappe
from .config import zoom_enabled, get_setting

def _get_zoom_token():
    if not zoom_enabled():
        frappe.throw("Zoom is not configured")
    acct = get_setting("zoom_account_id")
    cid = get_setting("zoom_client_id")
    cs = get_setting("zoom_client_secret")
    auth = base64.b64encode(f"{cid}:{cs}".encode()).decode()
    resp = requests.post("https://zoom.us/oauth/token",
                         params={"grant_type": "account_credentials", "account_id": acct},
                         headers={"Authorization": f"Basic {auth}"})
    resp.raise_for_status()
    return resp.json()["access_token"]

def create_zoom_meeting(topic: str, start_time_iso: str, duration_min: int = 30):
    if not zoom_enabled():
        return {"id": None, "join_url": None, "start_url": None}
    token = _get_zoom_token()
    payload = {"topic": topic, "type": 2, "start_time": start_time_iso, "duration": duration_min}
    r = requests.post("https://api.zoom.us/v2/users/me/meetings",
                      headers={"Authorization": f"Bearer {token}",
                               "Content-Type":"application/json"},
                      data=json.dumps(payload))
    r.raise_for_status()
    return r.json()
