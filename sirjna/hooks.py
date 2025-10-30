
from . import __version__ as app_version
app_name = "sirjna"
app_title = "Sirjna"
app_publisher = "Sirjna Mentorship"
app_description = "Automated mentorship portal for US/Canada engineering programs"
app_email = "support@sirjna.com"
app_license = "MIT"
app_include_css = ["/assets/sirjna/css/sirjna.css"]
after_install = "sirjna.install.after_install"
fixtures = ["Website Theme","Web Template","Web Page","Top Bar Item","Footer Item","Website Settings"]
doc_events = {"Payment Request":{"on_update":"sirjna.integrations.payments.handle_payment_request_update"}}
after_migrate = ["sirjna.sirjna_appointments.install.bootstrap"]
app_include_js = ["/assets/sirjna/sirjna_appointments/js/book_call.js"]
