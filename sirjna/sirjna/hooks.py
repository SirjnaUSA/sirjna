from . import __version__ as app_version

app_name = "sirjna"
app_title = "Sirjna"
app_publisher = "Parinda LLC"
app_description = "Honest, data-based mentorship portal (Frappe v15)"
app_email = "contact@sirjna.com"
app_license = "MIT"

app_include_css = ["/assets/sirjna/css/sirjna.css"]

fixtures = []

scheduler_events = {
    "daily": ["sirjna.sirjna.api.jobs.send_webinar_reminders"],
    "hourly": ["sirjna.sirjna.api.jobs.auto_unlock_next_phase"],
}

after_install = [
    "sirjna.sirjna.api.insights_bootstrap.ensure_insights_assets",
    "sirjna.sirjna.api.wiki_bootstrap.ensure_student_wiki",
]
