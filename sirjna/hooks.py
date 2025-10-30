from . import __version__ as app_version

app_name = "sirjna"
app_title = "Sirjna"
app_publisher = "Parinda LLC"
app_description = "Automated mentorship portal for US/Canada engineering programs"
app_email = "contact@sirjna.com"
app_license = "MIT"

app_include_css = ["/assets/sirjna/css/sirjna.css"]

after_install = "sirjna.install.after_install"
after_migrate = ["sirjna.sirjna_appointments.install.bootstrap"]

doc_events = {
    "Payment Request": {
        "on_update": "sirjna.integrations.payments.handle_payment_request_update"
    }
}

fixtures = [
    "Website Theme",
    "Web Template",
    "Web Page",
    "Top Bar Item",
    "Footer Item",
    "Website Settings",
]
